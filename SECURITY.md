# Security Policy

## Reporting a vulnerability

Thank you for taking the time to responsibly disclose any security issues you may find.

This project handles concepts directly relevant to personal data protection — biometric data, cryptographic validation, anonymised audit logging — even if the current scope is a proof-of-concept without physical hardware. Security reports are taken seriously.

**Preferred reporting channel:** email to `security.kiosk-biometric@proton.me` with the subject line `SECURITY` followed by a brief one-line description.

Please include in your report:

- A clear description of the issue and the file(s) and line(s) involved.
- Steps to reproduce, including any relevant input, environment details and expected vs. actual behaviour.
- An assessment of the potential impact (confidentiality, integrity, availability, regulatory exposure).
- Any suggested remediation, if you have one.
- Whether you wish to be credited and, if so, under which name.

Please **do not** open public GitHub issues for security vulnerabilities. Public issues are appropriate for functional bugs and feature requests, not for security disclosures.

## What to expect

- **Acknowledgement** within 5 business days of your report.
- **Initial assessment** within 15 business days (severity, scope, planned remediation).
- **Remediation** in a timeframe proportional to severity. Critical issues are prioritised.
- **Public disclosure** is coordinated with the reporter, normally after a fix is available. Credit is given in the changelog and, where appropriate, in the commit message.

## Scope

In scope:

- The Python module under `src/`.
- The test suite under `tests/`.
- The HTML mockups under `mockups/`.
- The CI workflow definitions under `.github/workflows/`.

Out of scope (not because they are unimportant, but because they are not part of this repository):

- Vulnerabilities in upstream dependencies (please report those to the corresponding maintainers; we will update the dependency on receipt of a fix).
- The forthcoming hardware integration (NFC readers, depth cameras), which is not yet present in the code base.
- Hypothetical issues in production deployments built on top of this code by third parties: this repository is a proof-of-concept and production deployments must undergo their own security review.

## What is *not* a vulnerability

- Reports based on configuration choices in `demo_session.py` (the demo is intentionally permissive for inspection purposes).
- Reports based on outdated forks of this repository.
- Theoretical reports without reproducible steps or impact assessment.

## Acknowledgements

Responsible reporters who comply with this policy and act in good faith are eligible to be acknowledged in the project changelog, unless they request anonymity.

---

This policy is provided in good faith and is subject to revision. The latest version is always the one present on the `main` branch of this repository.
