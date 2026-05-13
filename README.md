# Kiosk Biometric Verification

End-to-end design and proof-of-concept implementation of a robotized self-service kiosk with biometric identity verification, intended for deployment in Spanish licensed tobacco retail premises (estancos).

The project covers the core design of a regulated, age-restricted automated retail solution: a Python verification workflow with mockable interfaces for cryptographic and biometric checks, a unit-test suite with pytest, and documented regulatory, GDPR/RGPD and project-planning considerations.

> **Status**: Personal end-to-end project. Software components are functional; hardware integration with physical NFC readers and depth cameras is out of scope at this stage.

---

## Why this project

Spain's tobacco retail is heavily regulated and currently restricted to physical premises operated by licensed tobacconists. This project explores what a compliant automated retail solution would look like: secure age verification through biometric identity checks, full GDPR compliance, traceable audit logs, and clear regulatory framing.

The goal was not just to write code, but to walk the full path from concept to a deliverable that could realistically be presented to regulators — reflecting how I work in technical roles: ownership, attention to detail, and rigorous documentation.

---

## What's inside

### `src/biometric_verification.py`
Python module implementing a testable verification workflow:

- **Mockable NFC chip reading interface** designed around ICAO 9303 MRTD concepts
- **Mockable cryptographic signature validation interface** intended for FNMT-RCM trust-anchor validation in a production implementation
- **Mockable liveness detection interface** aligned with ISO/IEC 30107-3 concepts
- **1:1 facial matching** using cosine distance against the chip-extracted photo
- **Age calculation** with leap-year edge cases
- **Minimized audit logging** with HMAC and daily salt rotation (no direct PII stored; treated prudently as pseudonymized until legal/anonymization review)
- **Secure memory wiping** using `bytearray` overwrite and `numpy` zeroing on every code path, including exception paths

### `tests/test_biometric_verification.py`
Unit test suite using `pytest`, `pytest-cov`, `freezegun`, and `unittest.mock`. **51 tests, 94% line coverage**, organised in seven test classes:

- `TestSecureWipe` — buffer zeroing including full RGB image arrays
- `TestCalculateAge` — birthday edge cases, leap years, deterministic date fixing
- `TestFaceMatcher` — cosine distance properties, zero-vector safety, threshold boundaries
- `TestAuditLogger` — daily determinism, salt rotation, PII absence verification
- `TestBiometricSessionFlow` — all seven session outcome transitions with negative assertions
- `TestPrivacyGuarantees` — wipe called on every path, resource release on failure
- Parametrized regression tables for outcome invariants and age boundary cases

> Out of scope (explicitly noted): hardware integration tests, biometric SDK calibration per ISO/IEC 19795, presentation attack detection (PAD) evaluation requiring a physical attack kit.

### `demo_session.py`
Small simulated demo that runs approved and rejected verification sessions without physical hardware.

```bash
python demo_session.py
```

### `mockups/kiosk-flow.html`
Single-file touchscreen concept mockup covering the customer flow: welcome, catalog, biometric verification, payment and confirmation.

### `docs/architecture.md`
Technical architecture note explaining the verification flow, implemented components, out-of-scope items and production hardening checklist.

### `.github/workflows/tests.yml`
GitHub Actions workflow that runs the test suite automatically on Python 3.11 and 3.12.

### `business/`
Business validation package positioning the project as a secure age-verification system for automated sales in regulated sectors. It includes a one-pager, pitch deck outline, regulatory dossier, contact map, demo video plan, MVP budget, Spanish launch plan, RGPD data matrix, legal-product memo, discovery interview guide, Comisionado consultation questions, DPO/legal review notes and funding shortlist.

---

## Tech stack

- **Language**: Python 3.11+
- **Testing**: pytest, pytest-cov, freezegun, unittest.mock
- **NFC reading concept**: PC/SC-style interface (`pyscard` dependency retained for intended integration)
- **Cryptography concept**: standard library + `cryptography` package for intended X.509 validation
- **Image processing**: numpy, Pillow
- **UI prototypes**: HTML5 + CSS single-file concept mockup
- **Documentation**: Markdown architecture notes plus regulatory, GDPR/RGPD and project-planning considerations

---

## Design decisions worth noting

- **Privacy by design, not by addition.** Biometric data is wiped on every path, including exceptions. Audit logs use HMAC with daily-rotating salts, store no direct PII, and are treated prudently as pseudonymized unless a formal anonymization review concludes otherwise. The consent flow is multi-layer and withdrawable.
- **Cryptographic validation designed against an authoritative source.** The production design targets validation against FNMT-RCM root certificates rather than self-checking only.
- **Standards-based, not improvised.** Liveness detection is framed around ISO/IEC 30107-3 and NFC reading around ICAO 9303. Where hardware testing is out of scope, it is documented explicitly rather than glossed over.
- **Regulatory engagement as a first-class deliverable.** The regulatory consultation work covers licensing implications, age-verification standards, fiscal stamping, traceability, post-incident protocols, and RGPD interactions.

---

## What this project demonstrates

- End-to-end technical autonomy on a non-trivial scope.
- Comfort working across the full delivery chain: requirements analysis, prototyping, implementation, testing, regulatory framing, compliance documentation and early business validation.
- Rigor in privacy and security choices, applied throughout the codebase and not as an afterthought.
- Clear documentation habits — the kind that translate directly into operational support, incident management and procedural work.
- Ability to translate a technical prototype into a business validation package for regulated markets.

---

## License

This project is released for portfolio and educational purposes. Code is provided "as is" without warranty of any kind. Regulatory and GDPR documentation is illustrative; do not rely on it for actual deployment without consulting qualified legal counsel.

---

## Author

**Ana López Fernández** — IT Support Technician, CFGS ASIR (Cybersecurity specialty).
[LinkedIn](https://www.linkedin.com/in/ana-lopez-fernandez-evanda/) · Madrid, Spain.
