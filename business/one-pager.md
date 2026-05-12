# One-pager — Secure Age Verification for Regulated Automated Retail

## Working title

**Secure Age Verification System for Automated Sales in Regulated Sectors**

## Positioning

A privacy-by-design verification layer for automated retail environments where legal age, identity assurance and auditable compliance are required before purchase.

Initial use case: **licensed tobacco retail premises in Spain (estancos)**.  
Broader opportunity: alcohol, regulated vending, pharmacies/parapharmacies, access control and other age-restricted or identity-sensitive services.

## Problem

Automated sales in regulated sectors face three simultaneous barriers:

1. **Age verification** — ensuring only legally eligible adults can complete the purchase.
2. **Identity assurance** — reducing fraud, document misuse and unattended access risk.
3. **Regulatory traceability** — proving that the verification process happened without storing unnecessary personal data.

Traditional vending or self-service flows are not enough where regulation, sanctions and reputational risk are high.

## Solution

A modular verification system that can be integrated into kiosks, vending machines or self-service terminals.

The system verifies majority of age through a controlled flow:

- Document chip reading concept via NFC/ICAO 9303-style interface.
- Cryptographic validation concept against trusted certificate authorities.
- Liveness and 1:1 biometric matching concept.
- Legal-age calculation.
- Privacy-safe audit token using HMAC and rotating daily salt.
- No PII stored in audit logs.
- Secure wiping of sensitive buffers after each session.

## Why now

- Retail automation is expanding.
- Regulators increasingly demand stronger age controls.
- Businesses need compliant self-service without assuming unnecessary data protection risk.
- Biometric and digital identity technologies are becoming more accessible, but need careful privacy-by-design implementation.

## Target customers

- Licensed tobacco retailers and estanco networks.
- Vending manufacturers and operators.
- Self-service kiosk integrators.
- Regulated retail chains.
- Compliance-focused software integrators.

## Business model options

1. **Software licensing** per kiosk/device.
2. **SaaS compliance dashboard** for audit logs, status and reporting.
3. **Integration project fee** for pilots and custom deployments.
4. **Hardware partner model** with vending/kiosk manufacturers.
5. **Maintenance and support contract** for regulated operators.

## Current status

- Functional Python proof-of-concept for verification workflow.
- 51 automated tests with 94% coverage.
- Simulated demo session.
- Touchscreen mockup.
- Architecture and regulatory framing documented.
- Hardware integration and legal validation are explicitly out of scope at this stage.

## Next milestone

Build a pilot-ready validation package:

- Legal feasibility consultation.
- 10–20 customer discovery interviews.
- Hardware integration plan.
- Data protection impact assessment outline.
- Pilot budget and partner map.

## Key message

This is not just a kiosk concept. It is a **compliance layer for automated regulated sales**, designed around privacy, auditability and operational reliability from the start.
