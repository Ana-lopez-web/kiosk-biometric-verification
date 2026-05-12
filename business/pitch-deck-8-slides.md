# Pitch deck — 8-slide structure

## Slide 1 — Title

**Secure Age Verification for Automated Regulated Retail**

Privacy-by-design verification of legal age and identity for self-service sales in regulated sectors.

Initial use case: licensed tobacco retail premises in Spain.  
Founder/project lead: Ana López Fernández.

---

## Slide 2 — The problem

Automated retail is difficult in regulated sectors because businesses must prove that they do not sell restricted products to minors.

Current pain points:

- Manual age checks create friction and operational cost.
- Basic vending controls are weak for high-risk regulated products.
- Businesses need auditability without storing excessive personal data.
- Regulation creates uncertainty for unattended or semi-attended sales.

**Core problem:** automated sale requires age, identity and traceability to be solved together.

---

## Slide 3 — The solution

A modular verification layer for kiosks and self-service terminals.

The system performs:

- Document-based identity verification concept.
- Biometric liveness and 1:1 face match concept.
- Legal-age decision.
- Audit-safe logging without PII.
- Privacy-first session cleanup.

The result is a simple business decision:

**Approved / rejected / auditable outcome — without keeping unnecessary personal data.**

---

## Slide 4 — Why it matters

For regulated retailers:

- Lower compliance risk.
- Better customer flow.
- Stronger proof of responsible sale.
- Potential for controlled self-service.

For regulators:

- Traceable process.
- Privacy-by-design architecture.
- Clear failure modes.
- No uncontrolled retention of identity or biometric data.

For hardware partners:

- Differentiated compliance feature.
- B2B integration opportunity.
- Reusable module across sectors.

---

## Slide 5 — Product concept

The product can be packaged in three layers:

1. **Verification engine**  
   Age decision, matching logic, audit token, session lifecycle.

2. **Integration layer**  
   NFC reader, camera/liveness SDK, kiosk software, payment and dispenser systems.

3. **Compliance layer**  
   Audit dashboard, logs, reporting, consent/privacy flow, incident records.

Initial pilot: kiosk/self-service terminal inside a licensed retail environment.

---

## Slide 6 — Current proof of concept

Current assets:

- Python verification workflow.
- Mockable interfaces for NFC, certificate validation, liveness and face capture.
- 51 pytest tests, 94% coverage.
- Privacy-safe HMAC audit logging.
- Secure wiping of sensitive buffers.
- Demo script.
- Touchscreen mockup.
- Architecture documentation.

This proves technical ownership and validates the core decision flow before hardware integration.

---

## Slide 7 — Business model and market entry

Recommended entry strategy:

1. Validate legal feasibility.
2. Interview estancos and vending operators.
3. Partner with kiosk/vending hardware provider.
4. Build a controlled pilot.
5. Package software as a licensing/SaaS compliance module.

Possible revenue:

- Setup/integration fee.
- Monthly software license per device.
- Compliance dashboard subscription.
- Maintenance/support contract.
- Custom regulatory integration services.

---

## Slide 8 — Funding ask / next step

Next objective: move from proof of concept to pilot validation.

Funding needed for:

- Legal/regulatory consultation.
- DPIA/RGPD review.
- Hardware prototype.
- Biometric SDK evaluation.
- Pilot integration.
- Customer discovery and business development.

Target funding path:

- ENISA Emprendedoras Digitales.
- Madrid startup/emprendimiento programs.
- CDTI/NEOTEC if technological innovation is strengthened.
- Hardware partner co-development.
- Accelerator or business angel after validation.

**Ask:** support to validate legal feasibility and build a pilot-ready MVP with one industry partner.
