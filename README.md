# Kiosk Biometric Verification

[![Tests](https://github.com/Ana-lopez-web/kiosk-biometric-verification/actions/workflows/tests.yml/badge.svg)](https://github.com/Ana-lopez-web/kiosk-biometric-verification/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)](https://github.com/Ana-lopez-web/kiosk-biometric-verification)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success)](#roadmap)

> 🇪🇸 También disponible en [español](README.es.md).

End-to-end design and proof-of-concept implementation of a biometric identity verification module intended for integration into a **homologable model of tobacco vending machine** under Spain's regulatory framework — namely, [Circular 1/2025](https://www.boe.es/diario_boe/) of the *Comisionado para el Mercado de Tabacos* (entry into force: 2 January 2026) — for deployment in the venues authorised by Article 25.Two of [Royal Decree 1199/1999](https://www.boe.es/buscar/act.php?id=BOE-A-1999-15028) (hospitality, hotels, service-station convenience stores, gaming establishments and press kiosks).

The project covers the core design of a regulated, age-restricted automated retail solution: a Python verification workflow with mockable interfaces for cryptographic and biometric checks, a unit-test suite with pytest, and documented regulatory, GDPR/RGPD and project-planning considerations.

> **Status**: Personal end-to-end project, in active regulatory engagement. Software components are functional; hardware integration with physical NFC readers and depth cameras is out of scope at this stage. See [Roadmap](#roadmap).

---

## Why this project

Spain's tobacco retail is heavily regulated. Manual sale is reserved to licensed tobacconists (*estancos*), but automated sale through vending machines is permitted — under strict conditions — in a closed list of venues set by Article 25.Two of RD 1199/1999. Those machines must be authorised on a model-by-model basis, following the procedure that *Circular 1/2025* (15 December 2025) consolidates and modernises.

This project explores what a compliant, technology-forward model of vending machine could look like: secure age verification through DNIe NFC reading and 1:1 facial biometrics, full GDPR compliance, traceable anonymised audit logs, and a clear regulatory framing aligned with the current procedure for authorising a new model.

The goal was not just to write code, but to walk the full path from concept to a deliverable that could realistically be presented to regulators — reflecting how I work in technical roles: ownership, attention to detail, and rigorous documentation.

---

## Deployment scenarios

### Primary scenario — Authorised vending venues (Article 25.Two RD 1199/1999)

A homologated model installed in establishments where Spanish law currently permits tobacco vending machines: hospitality (bars, restaurants), hotels and similar accommodation, service-station convenience stores, gaming venues and press kiosks. The biometric verification system is positioned as a **technical reinforcement** of the existing legal obligation that the venue holder controls and supervises the machine, reducing the risk of inadvertent sales to minors.

### Secondary scenario — Compliance tool inside tobacconists (*estancos*)

As a variant, the same software module could be deployed as a **compliance assistance tool** inside *estancos*, supporting (not replacing) the human tobacconist's existing duty to verify the buyer's age. This is positioned as an internal tool, not as a vending machine, and its admissibility is part of the open regulatory consultation (see [`docs/regulatory/`](docs/regulatory)).

---

## What's inside

### `src/biometric_verification.py`

Python module implementing a testable verification workflow:

- **Mockable NFC chip reading interface** designed around ICAO 9303 MRTD concepts
- **Mockable cryptographic signature validation interface** intended for FNMT-RCM trust-anchor validation in a production implementation
- **Mockable liveness detection interface** aligned with ISO/IEC 30107-3 concepts
- **1:1 facial matching** using cosine distance against the chip-extracted photo
- **Age calculation** with leap-year edge cases
- **Anonymised audit logging** with HMAC and daily salt rotation (no PII stored)
- **Secure memory wiping** using `bytearray` overwrite and `numpy` zeroing on every code path, including exception paths

### `tests/test_biometric_verification.py`

Unit test suite using `pytest`, `pytest-cov`, `freezegun`, and `unittest.mock`. **51 tests, 94% line coverage**, organised in seven test classes:

- `TestSecureWipe` — buffer zeroing including full RGB image arrays
- `TestCalculateAge` — birthday edge cases, leap years, deterministic date fixing
- `TestFaceMatcher` — cosine distance properties, zero-vector safety, threshold boundaries
- `TestAuditLogger` — daily determinism, salt rotation, PII absence verification
- `TestBiometricSessionFlow` — all seven session outcome transitions with negative assertions
- `TestPrivacyGuarantees` — wipe called on every path, resource release on failure
- Parametrised regression tables for outcome invariants and age boundary cases

To run:

```bash
pip install -r requirements.txt
pytest --cov=src
```

> Out of scope (explicitly noted): hardware integration tests, biometric SDK calibration per ISO/IEC 19795, full presentation attack detection (PAD) evaluation per ISO/IEC 30107-3 (requires a physical attack kit and accredited laboratory).

### `demo_session.py`

Small simulated demo that runs approved and rejected verification sessions without physical hardware.

```bash
python demo_session.py
```

### `mockups/kiosk-flow.html`

Single-file touchscreen concept mockup covering the customer flow: welcome, catalog, biometric verification, payment and confirmation. No frameworks, no build step — open in any browser.

### `docs/architecture.md`

Technical architecture note explaining the verification flow, implemented components, out-of-scope items and production hardening checklist.

### `docs/regulatory/`

Regulatory engagement materials:

- Mapping of the technical design against Article 4 of Law 28/2005, Article 25.Two of RD 1199/1999 and Circular 1/2025 of the *Comisionado para el Mercado de Tabacos*.
- Anonymised version of the formal consultation submitted to the *Comisionado*.

### `.github/workflows/tests.yml`

GitHub Actions workflow that runs the test suite automatically on Python 3.11 and 3.12.

### `business/`

Business validation package positioning the project as a secure age-verification system for automated sales in regulated sectors. Includes one-pager, pitch deck outline, regulatory dossier, contact map, demo video plan and MVP budget.

---

## Regulatory framework

The project is anchored in the following Spanish and EU norms:

- **Law 13/1998**, of 4 May, on the organisation of the tobacco market.
- **Law 28/2005**, of 26 December, on health measures against tobacco use (Article 4 — vending machines; Article 9 — advertising prohibitions; Article 19 — sanctions).
- **Royal Decree 1199/1999**, of 9 July, implementing Law 13/1998 (Article 25.Two — list of venues where tobacco vending machines are permitted, in the wording given by RD 1676/2011).
- **Circular 1/2025**, of 15 December, of the *Comisionado para el Mercado de Tabacos*, on the procedure for authorising, modifying or altering vending-machine models and the operation of the Vending Machine Registry (BOE, 17 December 2025; in force from 2 January 2026).
- **Royal Decree-Law 17/2017**, of 17 November, transposing Directive 2014/40/EU on tobacco products.
- **Regulation (EU) 2016/679** (GDPR) and **Organic Law 3/2018** on data protection — in particular Article 9 (special categories of personal data, including biometric data) and Article 36 (prior consultation with the supervisory authority).
- **Commission Delegated Regulation (EU) 2018/574** on tobacco product traceability.

---

## Roadmap

| Milestone | Status |
|---|---|
| POC software module + 94% test coverage | ✅ Done |
| Mockups of customer flow | ✅ Done |
| Architecture and regulatory framing docs | ✅ Done |
| Formal consultation to *Comisionado para el Mercado de Tabacos* | 🟡 In preparation |
| Data Protection Impact Assessment (DPIA / EIPD) draft | ⏳ Planned |
| Prior consultation with AEPD (Article 36 GDPR), if applicable | ⏳ Planned |
| Hardware MVP (NFC reader + depth camera + dispensation) | ⏳ Planned |
| Model authorisation procedure under Circular 1/2025 | ⏳ Planned |
| Pilot deployment in authorised venue | ⏳ Planned |

---

## Tech stack

- **Language**: Python 3.11+
- **Testing**: pytest, pytest-cov, freezegun, unittest.mock
- **NFC reading concept**: PC/SC-style interface (`pyscard` dependency retained for intended integration)
- **Cryptography concept**: standard library + `cryptography` package for intended X.509 validation against FNMT-RCM
- **Image processing**: numpy, Pillow
- **UI prototypes**: HTML5 + CSS single-file concept mockup
- **CI**: GitHub Actions on Python 3.11 and 3.12

---

## Design decisions worth noting

- **Privacy by design, not by addition.** Biometric data is wiped on every path, including exceptions. Audit logs use HMAC with daily-rotating salts and store no PII. The consent flow is multi-layer and withdrawable.
- **Cryptographic validation designed against an authoritative source.** The production design targets validation against FNMT-RCM root certificates rather than self-checking only.
- **Standards-based, not improvised.** Liveness detection is framed around ISO/IEC 30107-3 and NFC reading around ICAO 9303. Where hardware testing is out of scope, it is documented explicitly rather than glossed over.
- **Regulatory engagement as a first-class deliverable.** The regulatory consultation covers licensing implications, age-verification standards, fiscal stamping, traceability, post-incident protocols, and GDPR interactions, and is structured to align with the procedure of Circular 1/2025.

---

## What this project demonstrates

- End-to-end technical autonomy on a non-trivial scope.
- Comfort working across the full delivery chain: requirements analysis, prototyping, implementation, testing, regulatory framing, compliance documentation and early business validation.
- Rigour in privacy and security choices, applied throughout the codebase and not as an afterthought.
- Clear documentation habits — the kind that translate directly into operational support, incident management and procedural work.
- Ability to translate a technical prototype into a business validation package for regulated markets.

---

## Security

Please refer to [SECURITY.md](SECURITY.md) for the responsible disclosure policy and reporting channel.

---

## License

Released under the [MIT License](LICENSE) for portfolio and educational purposes. Code is provided "as is" without warranty of any kind. Regulatory and GDPR documentation is illustrative and **must not** be relied upon for actual deployment without consulting qualified legal counsel.

---

## Author

**Ana López Fernández** — IT Support Technician, CFGS ASIR (Cybersecurity specialty).
[LinkedIn](https://www.linkedin.com/in/ana-lopez-fernandez-evanda/) · Madrid, Spain.
