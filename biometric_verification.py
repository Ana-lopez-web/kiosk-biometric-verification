"""
biometric_verification.py
=========================

Biometric identity verification module for the automated tobacco retail kiosk.

This module implements the full server-side verification pipeline:

  1. NFC reading of the Spanish DNIe chip via PC/SC, following ICAO 9303 MRTD
  2. Cryptographic validation of the document signature against FNMT-RCM
     (Spanish National Mint) trust anchors
  3. Liveness detection per ISO/IEC 30107-3 on the live camera capture
  4. 1:1 facial matching against the chip-extracted photo using cosine distance
  5. Legal age calculation with correct leap-year handling
  6. HMAC-based anonymised audit logging (daily-rotated salt, no PII stored)
  7. Secure memory wiping on every code path, including exception paths

The module is purposefully self-contained in a single file to make the verification
flow readable end-to-end. Hardware integration (physical NFC readers, depth cameras)
is mocked behind clean interfaces so the logic can be tested in isolation.

Standards followed
------------------
- ICAO Doc 9303 (Machine Readable Travel Documents) for NFC chip data structures
- ISO/IEC 30107-3 for presentation attack detection / liveness scoring
- ISO/IEC 19794-5 for facial image data
- RGPD / GDPR (EU 2016/679) for personal data handling

Out of scope (explicitly)
-------------------------
- Real hardware integration tests with physical NFC readers and depth cameras
- Biometric SDK calibration evaluation per ISO/IEC 19795
- Full presentation attack detection (PAD) evaluation per ISO/IEC 30107-3 (requires
  a physical attack kit and lab conditions)

Author: Ana López Fernández
License: MIT (see LICENSE)
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import secrets
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum, auto
from typing import Optional, Protocol

import numpy as np

# ============================================================================
#  Constants and configuration
# ============================================================================

#: Minimum legal age for tobacco purchase in Spain (Ley 28/2005)
LEGAL_AGE_TOBACCO_ES: int = 18

#: Cosine-distance threshold below which two face embeddings are considered a match.
#: 0.40 is a reasonable starting point for a 512-d FaceNet/ArcFace embedding.
#: Production deployments must calibrate against ISO/IEC 19794-5 reference datasets.
FACE_MATCH_THRESHOLD: float = 0.40

#: Liveness score threshold (0.0 = obvious spoof, 1.0 = certain live capture).
#: Below this value the session is rejected per ISO/IEC 30107-3 risk policy.
LIVENESS_THRESHOLD: float = 0.85

#: FNMT-RCM root certificate path (Spanish National Mint trust anchor for DNIe).
#: In production this should point to the deployed certificate bundle.
FNMT_ROOT_CERT_PATH: str = "/etc/kiosk/trust/fnmt-rcm-root.pem"

#: HMAC algorithm used for anonymised audit logging.
AUDIT_HMAC_ALGORITHM: str = "sha256"


logger = logging.getLogger("kiosk.biometric")


# ============================================================================
#  Outcome enum and result dataclass
# ============================================================================


class VerificationOutcome(Enum):
    """All possible terminal states of a single verification session.

    These outcomes are mutually exclusive and exhaustive: every session must
    end in exactly one of them.
    """

    APPROVED = auto()
    REJECTED_NFC_READ_FAILED = auto()
    REJECTED_SIGNATURE_INVALID = auto()
    REJECTED_LIVENESS_FAILED = auto()
    REJECTED_FACE_MISMATCH = auto()
    REJECTED_UNDER_AGE = auto()
    ERROR_INTERNAL = auto()


@dataclass
class VerificationResult:
    """Summary of a verification session, safe to surface in audit logs.

    Importantly, this object never contains personally identifiable data.
    The ``audit_token`` is an HMAC over a one-day-salted hash of the document
    number; it cannot be reversed to recover the original number.
    """

    outcome: VerificationOutcome
    audit_token: str
    timestamp_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    liveness_score: Optional[float] = None
    face_distance: Optional[float] = None


# ============================================================================
#  Secure memory wiping
# ============================================================================


def secure_wipe(buffer: bytearray | bytes | np.ndarray | None) -> None:
    """Overwrite a sensitive buffer in place to limit how long PII lives in RAM.

    Python does not give us deterministic memory deallocation, so the best we
    can do is reduce the window in which sensitive bytes are recoverable from
    a process dump or a swapped-out page.

    - ``bytearray``: overwritten byte by byte with zeros.
    - ``np.ndarray``: filled with zeros in place.
    - ``bytes`` (immutable): cannot be overwritten; we just discard the reference
      and rely on GC. The caller is encouraged to keep PII in ``bytearray``.
    - ``None``: no-op (safe to call defensively).

    Parameters
    ----------
    buffer
        The sensitive buffer to wipe. Accepts ``None`` to make defensive calls
        on every cleanup path easy and lint-friendly.
    """
    if buffer is None:
        return

    if isinstance(buffer, bytearray):
        for i in range(len(buffer)):
            buffer[i] = 0
        return

    if isinstance(buffer, np.ndarray):
        buffer.fill(0)
        return

    # `bytes` is immutable; nothing to wipe in place.


# ============================================================================
#  Age calculation
# ============================================================================


def calculate_age(birth: date, reference: date | None = None) -> int:
    """Return whole years elapsed between ``birth`` and ``reference``.

    Handles leap-year edge cases correctly: someone born on 29 February only
    "ages" on 1 March in non-leap years (the interpretation used by Spanish
    civil law for age-of-majority calculations).

    Parameters
    ----------
    birth
        Date of birth as read from the DNIe chip.
    reference
        Reference date (defaults to today, UTC).

    Returns
    -------
    int
        Whole years of age. Always ``>= 0``.
    """
    if reference is None:
        reference = datetime.now(timezone.utc).date()

    if birth > reference:
        return 0  # Defensive: future birth dates are nonsensical here.

    years = reference.year - birth.year
    # Adjust if the birthday has not yet happened this year.
    if (reference.month, reference.day) < (birth.month, birth.day):
        years -= 1

    return max(0, years)


# ============================================================================
#  Face matching
# ============================================================================


class FaceMatcher:
    """1:1 face verification using cosine distance between embeddings.

    The matcher does not produce embeddings itself; it expects pre-computed
    fixed-length float vectors (e.g. from a pre-trained ArcFace or FaceNet
    model). This keeps the module independent of any specific ML framework and
    makes it straightforward to test the math in isolation.
    """

    def __init__(self, threshold: float = FACE_MATCH_THRESHOLD) -> None:
        if not 0.0 <= threshold <= 2.0:
            raise ValueError(
                f"Cosine distance threshold must be in [0, 2]; got {threshold!r}."
            )
        self.threshold = threshold

    @staticmethod
    def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
        """Return the cosine distance ``1 - cos(a, b)`` in ``[0, 2]``.

        Defensive against zero vectors: if either vector has zero magnitude
        the result is ``1.0`` (i.e. "no information; do not match"), never a
        ZeroDivisionError.
        """
        if a.shape != b.shape:
            raise ValueError(
                f"Embeddings must have the same shape; got {a.shape} vs {b.shape}."
            )

        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 1.0

        cos_sim = float(np.dot(a, b) / (norm_a * norm_b))
        # Clamp for numerical stability; cosine similarity is in [-1, 1].
        cos_sim = max(-1.0, min(1.0, cos_sim))
        return 1.0 - cos_sim

    def is_match(self, chip_embedding: np.ndarray, live_embedding: np.ndarray) -> tuple[bool, float]:
        """Return ``(is_match, distance)`` for the pair of embeddings.

        ``is_match`` is True iff the distance is *strictly less than* the
        threshold. A distance equal to the threshold counts as a non-match
        (conservative bias appropriate for an age-restricted retail kiosk).
        """
        distance = self.cosine_distance(chip_embedding, live_embedding)
        return distance < self.threshold, distance


# ============================================================================
#  Audit logging (HMAC + daily salt rotation)
# ============================================================================


class AuditLogger:
    """Append-only logger for verification outcomes that records *no* PII.

    We never log the document number. Instead we log an HMAC over the document
    number, keyed by a salt that rotates every day. This means:

    - Within the same day, the same document gives the same audit token, so
      we can detect duplicates / abuse.
    - Across different days, the same document gives different audit tokens,
      so an attacker stealing a year of logs cannot trivially correlate them.
    - The original document number cannot be recovered without the salt.

    The salt is derived deterministically from a long-lived master key plus
    the current UTC date, so the system is stateless across restarts.
    """

    def __init__(self, master_key: bytes) -> None:
        if len(master_key) < 32:
            raise ValueError(
                "Master key must be at least 32 bytes for adequate HMAC security."
            )
        self._master_key = bytes(master_key)  # immutable copy

    def _daily_salt(self, when: date | None = None) -> bytes:
        """Derive the salt for a given UTC date (default: today)."""
        when = when or datetime.now(timezone.utc).date()
        date_token = when.isoformat().encode("ascii")
        return hashlib.sha256(self._master_key + date_token).digest()

    def audit_token(self, document_number: str, when: date | None = None) -> str:
        """Return a stable per-day HMAC token for the given document number."""
        salt = self._daily_salt(when)
        digest = hmac.new(
            salt, document_number.encode("utf-8"), AUDIT_HMAC_ALGORITHM
        ).hexdigest()
        return digest

    def log_outcome(
        self,
        document_number: str,
        outcome: VerificationOutcome,
        liveness_score: Optional[float] = None,
        face_distance: Optional[float] = None,
    ) -> VerificationResult:
        """Build and emit a ``VerificationResult`` for ``document_number``."""
        result = VerificationResult(
            outcome=outcome,
            audit_token=self.audit_token(document_number),
            liveness_score=liveness_score,
            face_distance=face_distance,
        )
        logger.info(
            "verification.outcome",
            extra={
                "outcome": outcome.name,
                "audit_token": result.audit_token,
                "liveness_score": liveness_score,
                "face_distance": face_distance,
                "timestamp_utc": result.timestamp_utc.isoformat(),
            },
        )
        return result


# ============================================================================
#  Hardware-facing interfaces (mockable for tests)
# ============================================================================


@dataclass
class ChipData:
    """Mutable container for data extracted from the DNIe chip.

    Held in a dataclass with ``bytearray`` / ``np.ndarray`` fields where
    possible so we can wipe them in place after the session ends.
    """

    document_number: str
    birth_date: date
    photo: np.ndarray  # shape (H, W, 3) uint8 face crop
    photo_embedding: np.ndarray  # shape (D,) float32 embedding
    signed_payload: bytearray  # raw signed bytes for cryptographic validation
    signature: bytearray  # detached signature


class NfcReader(Protocol):
    """Hardware-facing protocol for the NFC chip reader (PC/SC, ICAO 9303)."""

    def read_chip(self) -> ChipData: ...


class CertificateValidator(Protocol):
    """Validates the chip's signed payload against the FNMT-RCM trust anchor."""

    def is_signature_valid(self, payload: bytes, signature: bytes) -> bool: ...


class LivenessDetector(Protocol):
    """Returns a liveness score in ``[0.0, 1.0]`` per ISO/IEC 30107-3."""

    def score(self, frames: np.ndarray) -> float: ...


class FaceCapture(Protocol):
    """Captures a live face embedding from the depth camera."""

    def capture_embedding(self) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(frames, embedding)``. Frames feed liveness detection."""


# ============================================================================
#  Session orchestration
# ============================================================================


class BiometricSession:
    """Single-shot biometric verification session.

    A session reads the DNIe chip, validates its signature, captures a live
    face, scores liveness, performs 1:1 matching, checks legal age, and emits
    a single ``VerificationResult``. Sensitive buffers are wiped on every
    exit path, including exceptions.

    Each session owns its hardware references but does not own their lifetime;
    callers are responsible for releasing reader handles, etc.
    """

    def __init__(
        self,
        nfc_reader: NfcReader,
        certificate_validator: CertificateValidator,
        liveness_detector: LivenessDetector,
        face_capture: FaceCapture,
        face_matcher: FaceMatcher,
        audit_logger: AuditLogger,
        legal_age: int = LEGAL_AGE_TOBACCO_ES,
        liveness_threshold: float = LIVENESS_THRESHOLD,
    ) -> None:
        self._nfc = nfc_reader
        self._certs = certificate_validator
        self._liveness = liveness_detector
        self._face_capture = face_capture
        self._matcher = face_matcher
        self._audit = audit_logger
        self._legal_age = legal_age
        self._liveness_threshold = liveness_threshold

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------

    def run(self) -> VerificationResult:
        """Execute the full verification flow exactly once."""
        chip: Optional[ChipData] = None
        live_frames: Optional[np.ndarray] = None
        live_embedding: Optional[np.ndarray] = None
        document_number_for_audit: str = ""

        try:
            # ---- 1. NFC read --------------------------------------------------
            try:
                chip = self._nfc.read_chip()
            except Exception:  # noqa: BLE001
                logger.exception("nfc.read_failed")
                return self._audit.log_outcome(
                    document_number_for_audit, VerificationOutcome.REJECTED_NFC_READ_FAILED
                )

            document_number_for_audit = chip.document_number

            # ---- 2. Cryptographic validation ----------------------------------
            if not self._certs.is_signature_valid(
                bytes(chip.signed_payload), bytes(chip.signature)
            ):
                return self._audit.log_outcome(
                    document_number_for_audit,
                    VerificationOutcome.REJECTED_SIGNATURE_INVALID,
                )

            # ---- 3. Live capture & liveness -----------------------------------
            try:
                live_frames, live_embedding = self._face_capture.capture_embedding()
            except Exception:  # noqa: BLE001
                logger.exception("face_capture.failed")
                return self._audit.log_outcome(
                    document_number_for_audit, VerificationOutcome.ERROR_INTERNAL
                )

            liveness_score = self._liveness.score(live_frames)
            if liveness_score < self._liveness_threshold:
                return self._audit.log_outcome(
                    document_number_for_audit,
                    VerificationOutcome.REJECTED_LIVENESS_FAILED,
                    liveness_score=liveness_score,
                )

            # ---- 4. 1:1 face matching -----------------------------------------
            is_match, distance = self._matcher.is_match(
                chip.photo_embedding, live_embedding
            )
            if not is_match:
                return self._audit.log_outcome(
                    document_number_for_audit,
                    VerificationOutcome.REJECTED_FACE_MISMATCH,
                    liveness_score=liveness_score,
                    face_distance=distance,
                )

            # ---- 5. Age check -------------------------------------------------
            age = calculate_age(chip.birth_date)
            if age < self._legal_age:
                return self._audit.log_outcome(
                    document_number_for_audit,
                    VerificationOutcome.REJECTED_UNDER_AGE,
                    liveness_score=liveness_score,
                    face_distance=distance,
                )

            # ---- 6. All checks passed -----------------------------------------
            return self._audit.log_outcome(
                document_number_for_audit,
                VerificationOutcome.APPROVED,
                liveness_score=liveness_score,
                face_distance=distance,
            )

        except Exception:  # noqa: BLE001
            logger.exception("session.unexpected_error")
            return self._audit.log_outcome(
                document_number_for_audit, VerificationOutcome.ERROR_INTERNAL
            )

        finally:
            # ---- 7. Always-wipe cleanup ---------------------------------------
            # Run irrespective of which branch returned above, including
            # exception paths. This is the privacy guarantee that Article 32
            # RGPD ("appropriate technical measures") refers to in our design.
            if chip is not None:
                secure_wipe(chip.photo)
                secure_wipe(chip.photo_embedding)
                secure_wipe(chip.signed_payload)
                secure_wipe(chip.signature)
            secure_wipe(live_frames)
            secure_wipe(live_embedding)


# ============================================================================
#  Convenience factory
# ============================================================================


def build_default_audit_logger() -> AuditLogger:
    """Return an ``AuditLogger`` keyed by the kiosk master key.

    The master key is read from the ``KIOSK_AUDIT_MASTER_KEY`` environment
    variable (hex-encoded, 32+ bytes). For local development a fresh random
    key is generated; this **must not** be used in production because audit
    tokens would not be reproducible across restarts.
    """
    hex_key = os.environ.get("KIOSK_AUDIT_MASTER_KEY")
    if hex_key:
        key = bytes.fromhex(hex_key)
    else:
        logger.warning(
            "KIOSK_AUDIT_MASTER_KEY not set; generating an ephemeral key. "
            "Do not use this in production."
        )
        key = secrets.token_bytes(32)
    return AuditLogger(master_key=key)
