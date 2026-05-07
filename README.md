# Kiosk Biometric Verification

End-to-end design and proof-of-concept implementation of a robotized self-service kiosk with biometric identity verification, intended for deployment in Spanish licensed tobacco retail premises (estancos).

The project covers the full stack of a regulated, age-restricted automated retail solution: touchscreen UI mockups, a Python verification module with cryptographic and biometric checks, a unit-test suite with pytest, a project plan with critical path analysis, formal regulatory consultation documentation for Spain's Comisionado para el Mercado de Tabacos, and a complete GDPR (RGPD) compliance analysis.

> **Status**: Personal end-to-end project. Software components are functional; hardware integration with physical NFC readers and depth cameras is out of scope at this stage.

---

## Why this project

Spain's tobacco retail is heavily regulated and currently restricted to physical premises operated by licensed tobacconists. This project explores what a compliant automated retail solution would look like: secure age verification through biometric identity checks, full GDPR compliance, traceable audit logs, and clear regulatory framing.

The goal was not just to write code, but to walk the full path from concept to a deliverable that could realistically be presented to regulators — reflecting how I work in technical roles: ownership, attention to detail, and rigorous documentation.

---

## What's inside

### `biometric_module/`
Python module (~440 lines) implementing the verification flow:

- **NFC chip reading** via PC/SC, following the ICAO 9303 MRTD protocol
- **Cryptographic signature validation** against FNMT-RCM (Spanish National Mint) certificates
- **Liveness detection** per ISO/IEC 30107-3
- **1:1 facial matching** using cosine distance against the chip-extracted photo
- **Age calculation** with leap-year edge cases
- **Anonymized audit logging** with HMAC and daily salt rotation (no PII stored)
- **Secure memory wiping** using `bytearray` overwrite and `numpy` zeroing on every code path, including exception paths

### `tests/`
Unit test suite (`test_biometric_verification.py`) using `pytest`, `pytest-cov`, `freezegun`, and `unittest.mock`. **51 tests, 94% line coverage**, organised in seven test classes:

- `TestSecureWipe` — buffer zeroing including full RGB image arrays
- `TestCalculateAge` — birthday edge cases, leap years, deterministic date fixing
- `TestFaceMatcher` — cosine distance properties, zero-vector safety, threshold boundaries
- `TestAuditLogger` — daily determinism, salt rotation, PII absence verification
- `TestBiometricSessionFlow` — all seven session outcome transitions with negative assertions
- `TestPrivacyGuarantees` — wipe called on every path, resource release on failure
- Parametrized regression tables for outcome invariants and age boundary cases

> Out of scope (explicitly noted): hardware integration tests, biometric SDK calibration per ISO/IEC 19795, presentation attack detection (PAD) evaluation requiring a physical attack kit.

### `mockups/`
Five interconnected touchscreen mockups in a single navigable HTML file, covering the full customer flow:

1. Welcome screen
2. Product catalog with age-restricted badges
3. Biometric verification (NFC document reading + facial capture)
4. Payment with order summary and method selection
5. Confirmation with robotic dispensation progress

### `docs/`

- **Regulatory consultation document** (`regulatory-consultation.docx`) — formal Word document containing 24 questions across 8 thematic blocks, prepared for submission to Spain's Comisionado para el Mercado de Tabacos at the Ministry of Finance.
- **GDPR (RGPD) compliance analysis** (`gdpr-compliance.docx`) — five-layer compliance approach: permanent footer notice, pre-biometric informational screen, Article 13 GDPR information table, explicit consent clause, complete 10-section privacy policy accessible via QR code, consent withdrawal clause, and notes for the data controller.
- **Project plan** (`project-plan-gantt.pdf`) — 25-week Gantt chart across 7 sequential phases (legal analysis, architecture, software prototype, robotics build, integration, security testing, pilot), with the critical path identified as F1→F2→F3→F5→F7.

---

## Tech stack

- **Language**: Python 3.11+
- **Testing**: pytest, pytest-cov, freezegun, unittest.mock
- **NFC reading**: PC/SC (pyscard)
- **Cryptography**: standard library + cryptography package for X.509 validation
- **Image processing**: numpy, Pillow
- **UI prototypes**: HTML5 + CSS (no frameworks, single-file mockup)
- **Documentation**: Word (docx) for regulatory and GDPR materials

---

## Design decisions worth noting

- **Privacy by design, not by addition.** Biometric data is wiped on every path, including exceptions. Audit logs use HMAC with daily-rotating salts and store no PII. The consent flow is multi-layer and withdrawable.
- **Cryptographic validation against authoritative source.** Document signatures are validated against FNMT-RCM root certificates, not just self-checked.
- **Standards-based, not improvised.** Liveness detection follows ISO/IEC 30107-3. NFC reading follows ICAO 9303. Where hardware testing is out of scope, it's documented explicitly rather than glossed over.
- **Regulatory engagement as a first-class deliverable.** The Comisionado consultation document is not boilerplate — it covers licensing implications, age-verification standards, fiscal stamping, traceability, post-incident protocols, and RGPD interactions across 24 specific questions.

---

## What this project demonstrates

- End-to-end technical autonomy on a non-trivial scope.
- Comfort working across the full delivery chain: requirements analysis, prototyping, implementation, testing, regulatory framing, and compliance documentation.
- Rigor in privacy and security choices, applied throughout the codebase and not as an afterthought.
- Clear documentation habits — the kind that translate directly into operational support, incident management, and procedural work.

---

## License

This project is released for portfolio and educational purposes. Code is provided "as is" without warranty of any kind. Regulatory and GDPR documentation is illustrative; do not rely on it for actual deployment without consulting qualified legal counsel.

---

## Author

**Ana López Fernández** — IT Support Technician, CFGS ASIR (Cybersecurity specialty).
[LinkedIn](https://www.linkedin.com/in/) · Madrid, Spain.
