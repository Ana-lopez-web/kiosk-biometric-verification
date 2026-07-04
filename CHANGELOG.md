# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Submission of the formal consultation to the *Comisionado para el Mercado de Tabacos* under the procedure consolidated by Circular 1/2025.
- Draft of the Data Protection Impact Assessment (DPIA / EIPD) for the biometric processing.
- Hardware MVP with physical NFC reader and depth camera.

## [0.2.0] - 2026-05-13

### Changed

- **Strategic repositioning** of the project: from a *kiosk for licensed tobacconist premises* to a **homologable model of tobacco vending machine** under Spain's regulatory framework — Article 25.Two of RD 1199/1999 and Circular 1/2025 of the *Comisionado para el Mercado de Tabacos*.
- README rewritten to reflect the primary deployment scenario (vending machines in authorised venues) and the secondary scenario (compliance assistance tool inside tobacconists).
- Regulatory references corrected and expanded: Law 13/1998, Law 28/2005 (Articles 4, 9 and 19), RD 1199/1999 (Article 25.Two in the wording of RD 1676/2011), Circular 1/2025, RDL 17/2017, GDPR (Articles 9 and 36), Regulation (EU) 2018/574 on traceability.

### Added

- `README.es.md` — Spanish version of the README, cross-linked from the English version.
- `SECURITY.md` — responsible disclosure policy and reporting channel.
- `CHANGELOG.md` — this file.
- Status, coverage, Python and license badges in the README headers.
- "Roadmap" section in both READMEs with the upcoming regulatory and technical milestones.
- "Regulatory framework" section in both READMEs consolidating the applicable Spanish and EU norms.
- Placeholder for `docs/regulatory/` materials (mapping against the regulatory framework and anonymised consultation document).

## [0.1.0] - 2026-04

### Added

- Initial Python verification module (`src/biometric_verification.py`) with mockable interfaces for NFC reading, cryptographic validation, liveness detection and facial capture.
- Test suite with 51 tests and 94% line coverage, organised in seven test classes.
- `demo_session.py` for simulated end-to-end execution without hardware.
- Single-file HTML mockup of the customer flow (welcome, catalog, biometric verification, payment, confirmation).
- `docs/architecture.md` with the technical architecture note.
- `business/` package with one-pager, pitch deck outline, regulatory dossier, contact map, demo video plan and MVP budget.
- GitHub Actions workflow running the test suite on Python 3.11 and 3.12.
- MIT License.

[Unreleased]: https://github.com/Ana-lopez-web/kiosk-biometric-verification/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Ana-lopez-web/kiosk-biometric-verification/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Ana-lopez-web/kiosk-biometric-verification/releases/tag/v0.1.0
