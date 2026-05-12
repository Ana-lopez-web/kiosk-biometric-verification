# Architecture overview

This repository contains a proof-of-concept verification workflow for an automated tobacco retail kiosk intended for licensed Spanish tobacco premises.

The current code focuses on the **server-side verification decision flow**. Hardware-specific integrations are intentionally represented as interfaces so the workflow can be tested without physical NFC readers, cameras or biometric SDKs.

## Components

```text
Customer
  │
  ▼
Touchscreen UI mockup
  │
  ▼
BiometricSession
  ├─ NfcReader interface
  ├─ CertificateValidator interface
  ├─ FaceCapture interface
  ├─ LivenessDetector interface
  ├─ FaceMatcher
  ├─ Age calculation
  └─ AuditLogger
```

## Verification flow

1. Read chip data through the `NfcReader` interface.
2. Validate the signed payload through the `CertificateValidator` interface.
3. Capture live frames and an embedding through the `FaceCapture` interface.
4. Score liveness through the `LivenessDetector` interface.
5. Compare chip and live embeddings with cosine distance.
6. Calculate legal age.
7. Emit a privacy-safe `VerificationResult`.
8. Wipe mutable sensitive buffers on every exit path.

## Implemented in this repository

- Verification orchestration in `src/biometric_verification.py`.
- Cosine-distance face matching.
- Legal-age calculation with leap-year edge cases.
- HMAC-based daily audit token generation without PII in logs.
- Defensive secure wiping for mutable buffers.
- 51 pytest tests covering success, rejection, error and privacy paths.
- A local simulated demo in `demo_session.py`.
- A touchscreen concept mockup in `mockups/kiosk-flow.html`.

## Explicitly out of scope

- Physical NFC reader integration.
- Real DNIe certificate-chain validation in production infrastructure.
- Real camera/depth-camera capture.
- Biometric SDK calibration and PAD testing.
- Payment terminal integration.
- Robotic dispenser integration.
- Legal validation for production deployment.

## Production hardening checklist

Before any real deployment, the following would be required:

- Integrate and test physical NFC readers.
- Implement full certificate-chain validation against deployed trust anchors.
- Select and calibrate a biometric SDK under relevant standards.
- Run PAD/liveness evaluation with real attack scenarios.
- Integrate payment and dispenser systems.
- Complete DPIA/RGPD review with qualified legal counsel.
- Establish incident response, audit retention and operational procedures.
