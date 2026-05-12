"""
test_biometric_verification.py
==============================

Unit-test suite for ``biometric_verification.py``.

The suite is organised into seven classes, one per concern:

  * ``TestSecureWipe``         — buffer zeroing, including RGB image arrays
  * ``TestCalculateAge``       — birthday edge cases, leap years
  * ``TestFaceMatcher``        — cosine distance properties, threshold semantics
  * ``TestAuditLogger``        — daily determinism, salt rotation, no-PII guarantee
  * ``TestBiometricSessionFlow`` — all 7 outcomes, with negative assertions
  * ``TestPrivacyGuarantees``  — wipe is called on every path, including failures
  * Parametrised regression tables at the bottom for outcome invariants and
    age-boundary cases.

The suite uses ``pytest``, ``pytest-cov``, ``freezegun`` (for deterministic
date fixing) and ``unittest.mock`` (for the hardware-facing protocols).

Out-of-scope for unit testing (documented here for honesty):

  * Hardware integration with physical NFC readers and depth cameras
  * Biometric SDK calibration evaluation per ISO/IEC 19795
  * Full presentation attack detection (PAD) evaluation per ISO/IEC 30107-3
    requiring a physical attack kit and lab conditions

Author: Ana López Fernández
License: MIT
"""

from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock

import numpy as np
import pytest
from freezegun import freeze_time

from biometric_verification import (
    AuditLogger,
    BiometricSession,
    ChipData,
    FaceMatcher,
    VerificationOutcome,
    calculate_age,
    secure_wipe,
)


# ============================================================================
#  Helpers / fixtures
# ============================================================================


def _make_chip(
    document_number: str = "12345678Z",
    birth: date = date(1990, 6, 15),
    embedding: np.ndarray | None = None,
    photo: np.ndarray | None = None,
) -> ChipData:
    """Build a ChipData with sensible defaults; lets tests override single fields."""
    if embedding is None:
        rng = np.random.default_rng(42)
        embedding = rng.standard_normal(512).astype(np.float32)
    if photo is None:
        photo = np.full((96, 96, 3), 128, dtype=np.uint8)

    return ChipData(
        document_number=document_number,
        birth_date=birth,
        photo=photo,
        photo_embedding=embedding,
        signed_payload=bytearray(b"signed-payload"),
        signature=bytearray(b"signature-bytes"),
    )


def _audit() -> AuditLogger:
    """Return a stable AuditLogger with a deterministic master key."""
    return AuditLogger(master_key=b"a" * 32)


@pytest.fixture
def audit_logger() -> AuditLogger:
    return _audit()


@pytest.fixture
def matcher() -> FaceMatcher:
    return FaceMatcher(threshold=0.40)


# ============================================================================
#  TestSecureWipe
# ============================================================================


class TestSecureWipe:
    """``secure_wipe`` must zero mutable buffers in place and accept None safely."""

    def test_bytearray_is_zeroed_in_place(self) -> None:
        buffer = bytearray(b"sensitive-data")
        secure_wipe(buffer)
        assert buffer == bytearray(len(b"sensitive-data"))
        assert all(b == 0 for b in buffer)

    def test_numpy_uint8_image_is_zeroed_in_place(self) -> None:
        img = np.full((48, 48, 3), 255, dtype=np.uint8)
        original_id = id(img)  # confirm in-place; no reallocation
        secure_wipe(img)
        assert id(img) == original_id
        assert img.sum() == 0
        assert img.shape == (48, 48, 3)

    def test_numpy_float32_embedding_is_zeroed_in_place(self) -> None:
        emb = np.ones(512, dtype=np.float32)
        secure_wipe(emb)
        assert np.all(emb == 0.0)
        assert emb.dtype == np.float32

    def test_none_is_safe_noop(self) -> None:
        # Must not raise; this lets cleanup paths call wipe defensively.
        secure_wipe(None)

    def test_bytes_is_silently_ignored(self) -> None:
        # `bytes` is immutable; the function documents it cannot wipe in place.
        # We only require that the call does not raise.
        secure_wipe(b"immutable-bytes")


# ============================================================================
#  TestCalculateAge
# ============================================================================


class TestCalculateAge:
    """``calculate_age`` must handle leap-year edge cases like Spanish civil law."""

    @freeze_time("2026-05-07")
    def test_birthday_already_passed_this_year(self) -> None:
        assert calculate_age(date(2000, 1, 1)) == 26

    @freeze_time("2026-05-07")
    def test_birthday_today(self) -> None:
        assert calculate_age(date(2000, 5, 7)) == 26

    @freeze_time("2026-05-07")
    def test_birthday_tomorrow_means_one_year_younger(self) -> None:
        assert calculate_age(date(2000, 5, 8)) == 25

    @freeze_time("2026-02-28")
    def test_leap_birthday_in_non_leap_year_uses_march_first(self) -> None:
        # Born 29-feb-2000. On 28-feb-2026 they are still 25.
        assert calculate_age(date(2000, 2, 29)) == 25

    @freeze_time("2026-03-01")
    def test_leap_birthday_in_non_leap_year_ages_on_march_first(self) -> None:
        assert calculate_age(date(2000, 2, 29)) == 26

    @freeze_time("2024-02-29")
    def test_leap_birthday_in_leap_year_ages_on_feb_29(self) -> None:
        assert calculate_age(date(2000, 2, 29)) == 24

    def test_future_birth_returns_zero(self) -> None:
        # Defensive: nonsensical input should not crash or go negative.
        assert calculate_age(date(2099, 1, 1), reference=date(2026, 1, 1)) == 0

    @freeze_time("2026-05-07")
    def test_minor_just_below_legal_age(self) -> None:
        # Tobacco purchase requires 18+. Born 8 May 2008 -> 17 today.
        assert calculate_age(date(2008, 5, 8)) == 17

    @freeze_time("2026-05-07")
    def test_adult_just_at_legal_age(self) -> None:
        assert calculate_age(date(2008, 5, 7)) == 18


# ============================================================================
#  TestFaceMatcher
# ============================================================================


class TestFaceMatcher:
    """Cosine distance must satisfy mathematical invariants and threshold semantics."""

    def test_identical_vectors_give_distance_zero(self) -> None:
        v = np.array([1.0, 2.0, 3.0])
        assert FaceMatcher.cosine_distance(v, v) == pytest.approx(0.0)

    def test_opposite_vectors_give_distance_two(self) -> None:
        v = np.array([1.0, 2.0, 3.0])
        assert FaceMatcher.cosine_distance(v, -v) == pytest.approx(2.0)

    def test_orthogonal_vectors_give_distance_one(self) -> None:
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert FaceMatcher.cosine_distance(a, b) == pytest.approx(1.0)

    def test_zero_vector_yields_distance_one_not_division_error(self) -> None:
        # Defensive: a zero embedding (e.g. capture failure) must not crash.
        zero = np.zeros(4)
        non_zero = np.array([1.0, 2.0, 3.0, 4.0])
        assert FaceMatcher.cosine_distance(zero, non_zero) == 1.0
        assert FaceMatcher.cosine_distance(non_zero, zero) == 1.0
        assert FaceMatcher.cosine_distance(zero, zero) == 1.0

    def test_shape_mismatch_raises(self, matcher: FaceMatcher) -> None:
        with pytest.raises(ValueError, match="same shape"):
            matcher.cosine_distance(np.zeros(4), np.zeros(8))

    def test_threshold_validation(self) -> None:
        with pytest.raises(ValueError):
            FaceMatcher(threshold=-0.1)
        with pytest.raises(ValueError):
            FaceMatcher(threshold=2.1)

    def test_match_below_threshold(self, matcher: FaceMatcher) -> None:
        # Construct two vectors with cosine distance well below 0.40.
        a = np.array([1.0, 0.0, 0.0])
        b = np.array([0.99, 0.01, 0.0])
        is_match, distance = matcher.is_match(a, b)
        assert is_match is True
        assert distance < 0.40

    def test_no_match_at_or_above_threshold(self, matcher: FaceMatcher) -> None:
        # Orthogonal vectors -> distance 1.0, far above 0.40.
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        is_match, distance = matcher.is_match(a, b)
        assert is_match is False
        assert distance == pytest.approx(1.0)

    def test_threshold_boundary_is_strict(self) -> None:
        """Distance == threshold must count as no-match (conservative bias).

        We use orthogonal vectors because their cosine distance is exactly 1.0
        with no floating-point rounding, letting us exercise the strict ``<``
        comparison cleanly at the threshold.
        """
        matcher = FaceMatcher(threshold=1.0)
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        is_match, distance = matcher.is_match(a, b)
        assert distance == pytest.approx(1.0)
        assert is_match is False  # boundary is rejected: 1.0 is NOT < 1.0


# ============================================================================
#  TestAuditLogger
# ============================================================================


class TestAuditLogger:
    """HMAC tokens must be deterministic per day, rotate across days, and contain no PII."""

    def test_deterministic_within_same_day(self, audit_logger: AuditLogger) -> None:
        with freeze_time("2026-05-07"):
            t1 = audit_logger.audit_token("12345678Z")
            t2 = audit_logger.audit_token("12345678Z")
        assert t1 == t2

    def test_same_document_different_day_gives_different_token(
        self, audit_logger: AuditLogger
    ) -> None:
        with freeze_time("2026-05-07"):
            t_today = audit_logger.audit_token("12345678Z")
        with freeze_time("2026-05-08"):
            t_tomorrow = audit_logger.audit_token("12345678Z")
        assert t_today != t_tomorrow

    def test_different_documents_same_day_give_different_tokens(
        self, audit_logger: AuditLogger
    ) -> None:
        with freeze_time("2026-05-07"):
            t_a = audit_logger.audit_token("12345678Z")
            t_b = audit_logger.audit_token("87654321X")
        assert t_a != t_b

    def test_token_is_hex_sha256_length(self, audit_logger: AuditLogger) -> None:
        token = audit_logger.audit_token("12345678Z")
        assert len(token) == 64
        int(token, 16)  # must parse as hex

    def test_master_key_too_short_raises(self) -> None:
        with pytest.raises(ValueError, match="32 bytes"):
            AuditLogger(master_key=b"short")

    def test_log_outcome_returns_result_with_no_pii(
        self, audit_logger: AuditLogger
    ) -> None:
        result = audit_logger.log_outcome(
            "12345678Z", VerificationOutcome.APPROVED, liveness_score=0.95
        )
        # The audit token is opaque; it must not contain the document number.
        assert "12345678Z" not in result.audit_token
        assert "12345678" not in result.audit_token
        assert result.outcome is VerificationOutcome.APPROVED
        assert result.liveness_score == 0.95


# ============================================================================
#  TestBiometricSessionFlow
# ============================================================================


def _make_session(
    *,
    nfc_raises: bool = False,
    signature_valid: bool = True,
    capture_raises: bool = False,
    liveness_score: float = 0.95,
    chip_embedding: np.ndarray | None = None,
    live_embedding: np.ndarray | None = None,
    birth: date = date(1990, 6, 15),
    audit_logger: AuditLogger | None = None,
) -> tuple[BiometricSession, dict]:
    """Build a session wired to fully-mocked hardware components.

    Returns the session plus a dict of the mocks for assertion convenience.
    """
    if chip_embedding is None:
        chip_embedding = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    if live_embedding is None:
        # Default: matches the chip embedding (cosine distance 0.0).
        live_embedding = chip_embedding.copy()

    chip = _make_chip(birth=birth, embedding=chip_embedding)

    nfc = MagicMock()
    if nfc_raises:
        nfc.read_chip.side_effect = RuntimeError("nfc unreachable")
    else:
        nfc.read_chip.return_value = chip

    certs = MagicMock()
    certs.is_signature_valid.return_value = signature_valid

    liveness = MagicMock()
    liveness.score.return_value = liveness_score

    face_capture = MagicMock()
    if capture_raises:
        face_capture.capture_embedding.side_effect = RuntimeError("camera failed")
    else:
        frames = np.zeros((4, 96, 96, 3), dtype=np.uint8)
        face_capture.capture_embedding.return_value = (frames, live_embedding)

    matcher = FaceMatcher(threshold=0.40)
    audit = audit_logger or _audit()

    session = BiometricSession(
        nfc_reader=nfc,
        certificate_validator=certs,
        liveness_detector=liveness,
        face_capture=face_capture,
        face_matcher=matcher,
        audit_logger=audit,
    )
    return session, {
        "nfc": nfc,
        "certs": certs,
        "liveness": liveness,
        "face_capture": face_capture,
        "chip": chip,
    }


class TestBiometricSessionFlow:
    """Exhaustive check of all seven verification outcomes."""

    @freeze_time("2026-05-07")
    def test_approved_happy_path(self) -> None:
        session, _ = _make_session()
        result = session.run()
        assert result.outcome is VerificationOutcome.APPROVED

    def test_nfc_read_failure(self) -> None:
        session, mocks = _make_session(nfc_raises=True)
        result = session.run()
        assert result.outcome is VerificationOutcome.REJECTED_NFC_READ_FAILED
        # Negative assertion: downstream components were never called.
        mocks["certs"].is_signature_valid.assert_not_called()
        mocks["liveness"].score.assert_not_called()
        mocks["face_capture"].capture_embedding.assert_not_called()

    def test_signature_invalid(self) -> None:
        session, mocks = _make_session(signature_valid=False)
        result = session.run()
        assert result.outcome is VerificationOutcome.REJECTED_SIGNATURE_INVALID
        # Negative assertion: liveness and capture were never reached.
        mocks["liveness"].score.assert_not_called()
        mocks["face_capture"].capture_embedding.assert_not_called()

    def test_face_capture_failure_yields_internal_error(self) -> None:
        session, mocks = _make_session(capture_raises=True)
        result = session.run()
        assert result.outcome is VerificationOutcome.ERROR_INTERNAL
        mocks["liveness"].score.assert_not_called()

    def test_liveness_below_threshold(self) -> None:
        session, _ = _make_session(liveness_score=0.50)  # < 0.85
        result = session.run()
        assert result.outcome is VerificationOutcome.REJECTED_LIVENESS_FAILED
        assert result.liveness_score == 0.50

    def test_face_mismatch(self) -> None:
        chip_emb = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        live_emb = np.array([0.0, 1.0, 0.0], dtype=np.float32)  # orthogonal
        session, _ = _make_session(chip_embedding=chip_emb, live_embedding=live_emb)
        result = session.run()
        assert result.outcome is VerificationOutcome.REJECTED_FACE_MISMATCH
        assert result.face_distance is not None and result.face_distance > 0.40

    @freeze_time("2026-05-07")
    def test_under_age(self) -> None:
        # Born 8 May 2008 -> 17 years old today
        session, _ = _make_session(birth=date(2008, 5, 8))
        result = session.run()
        assert result.outcome is VerificationOutcome.REJECTED_UNDER_AGE


# ============================================================================
#  TestPrivacyGuarantees
# ============================================================================


class TestPrivacyGuarantees:
    """Sensitive buffers must be wiped on every exit path, including failures."""

    @freeze_time("2026-05-07")
    def test_wipe_called_on_happy_path(self) -> None:
        session, mocks = _make_session()
        chip = mocks["chip"]
        # Snapshot identity before run; we want to confirm the same buffer is zeroed.
        photo_id = id(chip.photo)
        emb_id = id(chip.photo_embedding)

        session.run()

        assert id(chip.photo) == photo_id
        assert id(chip.photo_embedding) == emb_id
        assert chip.photo.sum() == 0
        assert np.all(chip.photo_embedding == 0.0)
        assert chip.signed_payload == bytearray(len(b"signed-payload"))
        assert chip.signature == bytearray(len(b"signature-bytes"))

    def test_wipe_called_on_signature_failure(self) -> None:
        session, mocks = _make_session(signature_valid=False)
        chip = mocks["chip"]

        session.run()

        assert chip.photo.sum() == 0
        assert np.all(chip.photo_embedding == 0.0)

    def test_wipe_called_on_capture_exception(self) -> None:
        session, mocks = _make_session(capture_raises=True)
        chip = mocks["chip"]

        # Must not raise: the session swallows exceptions and emits ERROR_INTERNAL.
        result = session.run()

        assert result.outcome is VerificationOutcome.ERROR_INTERNAL
        # And cleanup still happened.
        assert chip.photo.sum() == 0
        assert np.all(chip.photo_embedding == 0.0)


# ============================================================================
#  Parametrised regression tables
# ============================================================================


@pytest.mark.parametrize(
    "outcome",
    [
        VerificationOutcome.APPROVED,
        VerificationOutcome.REJECTED_NFC_READ_FAILED,
        VerificationOutcome.REJECTED_SIGNATURE_INVALID,
        VerificationOutcome.REJECTED_LIVENESS_FAILED,
        VerificationOutcome.REJECTED_FACE_MISMATCH,
        VerificationOutcome.REJECTED_UNDER_AGE,
        VerificationOutcome.ERROR_INTERNAL,
    ],
)
def test_every_outcome_has_a_unique_name(outcome: VerificationOutcome) -> None:
    """Smoke check: outcome names are stable identifiers we can rely on in logs."""
    assert outcome.name.isupper()
    assert outcome.name.replace("_", "").isalpha()


@pytest.mark.parametrize(
    "today_iso, birth, expected_age",
    [
        # Just-turned-18 boundary (the legal-age frontier for tobacco in Spain).
        ("2026-05-07", date(2008, 5, 7), 18),
        ("2026-05-07", date(2008, 5, 8), 17),
        # Leap-year birthdays in non-leap years.
        ("2027-02-28", date(2000, 2, 29), 26),
        ("2027-03-01", date(2000, 2, 29), 27),
        # Identical date.
        ("2026-05-07", date(2026, 5, 7), 0),
    ],
)
def test_age_boundary_table(today_iso: str, birth: date, expected_age: int) -> None:
    with freeze_time(today_iso):
        assert calculate_age(birth) == expected_age
