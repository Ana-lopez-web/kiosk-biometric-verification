"""Run a small simulated kiosk verification demo.

This script does not use real NFC readers or cameras. It exercises the public
verification workflow with mock hardware adapters so recruiters can see the
project behaviour without special devices.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from biometric_verification import (
    AuditLogger,
    BiometricSession,
    ChipData,
    FaceMatcher,
    VerificationOutcome,
)


class DemoNfcReader:
    def __init__(self, birth_date: date, embedding: np.ndarray) -> None:
        self.birth_date = birth_date
        self.embedding = embedding

    def read_chip(self) -> ChipData:
        return ChipData(
            document_number="DEMO123456",
            birth_date=self.birth_date,
            photo=np.full((96, 96, 3), 128, dtype=np.uint8),
            photo_embedding=self.embedding.copy(),
            signed_payload=bytearray(b"demo-signed-payload"),
            signature=bytearray(b"demo-signature"),
        )


class DemoCertificateValidator:
    def is_signature_valid(self, payload: bytes, signature: bytes) -> bool:
        return bool(payload and signature)


class DemoLivenessDetector:
    def __init__(self, score: float) -> None:
        self._score = score

    def score(self, frames: np.ndarray) -> float:
        return self._score


class DemoFaceCapture:
    def __init__(self, embedding: np.ndarray) -> None:
        self.embedding = embedding

    def capture_embedding(self) -> tuple[np.ndarray, np.ndarray]:
        frames = np.full((3, 96, 96, 3), 80, dtype=np.uint8)
        return frames, self.embedding.copy()


def run_case(label: str, birth_date: date, live_score: float, same_face: bool) -> None:
    rng = np.random.default_rng(7)
    chip_embedding = rng.standard_normal(512).astype(np.float32)
    live_embedding = chip_embedding if same_face else rng.standard_normal(512).astype(np.float32)

    session = BiometricSession(
        nfc_reader=DemoNfcReader(birth_date, chip_embedding),
        certificate_validator=DemoCertificateValidator(),
        liveness_detector=DemoLivenessDetector(live_score),
        face_capture=DemoFaceCapture(live_embedding),
        face_matcher=FaceMatcher(),
        audit_logger=AuditLogger(master_key=b"demo-master-key-for-local-demo-123"),
    )
    result = session.run()
    print(f"{label}: {result.outcome.name}")
    print(f"  audit_token={result.audit_token[:16]}... liveness={result.liveness_score} face_distance={result.face_distance}")


if __name__ == "__main__":
    run_case("Approved adult", birth_date=date(1990, 6, 15), live_score=0.97, same_face=True)
    run_case("Rejected under age", birth_date=date(2010, 6, 15), live_score=0.97, same_face=True)
    run_case("Rejected liveness", birth_date=date(1990, 6, 15), live_score=0.40, same_face=True)
