# Regulatory dossier — validation plan

## Scope

This dossier frames the project as a **secure age-verification system for automated sales in regulated sectors**, with tobacco retail in Spain as the first regulatory test case.

It is not legal advice. It is a structured validation plan for conversations with regulators, legal counsel, industry associations and potential pilot partners.

## Regulatory thesis

The project should not be presented first as “an unattended tobacco vending machine”. That framing increases resistance.

Recommended framing:

> A privacy-by-design verification and audit layer that could be integrated into authorized retail environments to strengthen age-control compliance for regulated products.

## Key regulatory questions

### 1. Authorization model

- Can a self-service terminal operate inside a licensed estanco if the concession holder remains responsible for the sale?
- Would the device be treated as a tobacco vending machine, a point-of-sale extension, or a new category requiring specific authorization?
- Does the current registry of tobacco vending machines cover this type of terminal?
- Would biometric verification affect the authorization process?

### 2. Location and supervision

- Must the terminal be physically supervised by staff?
- Could it operate only inside licensed premises?
- Are there limits on opening hours or staff presence?
- How should failed verification attempts be handled operationally?

### 3. Age verification standard

- What level of identity assurance is acceptable for automated majority-of-age verification?
- Is document chip reading acceptable or required?
- Are biometric checks permitted or excessive under the principle of data minimization?
- Are there accepted alternatives: wallet identity, Cl@ve, eIDAS wallet, QR credential, manual override?

### 4. Data protection / RGPD

- What lawful basis would apply: legal obligation, legitimate interest, explicit consent, or a combination?
- Is biometric processing legally viable if templates are not stored and processing is transient?
- Would a DPIA be mandatory? Likely yes.
- What audit data can be retained without storing PII?
- What retention period is proportionate?
- How should consent withdrawal work if the sale depends on verification?

### 5. Audit and traceability

- What evidence must the operator keep to prove compliant age verification?
- Is an HMAC-based anonymous token acceptable for audit purposes?
- Should failed attempts be logged?
- How should logs be made available during inspection?

### 6. Fiscal and product-control obligations

- How does the terminal interact with fiscal stamps, pricing rules and stock control?
- Does automated dispensing affect existing obligations for tobacco retailers?
- Are there special reporting requirements for automated transactions?

### 7. Incident handling

- What happens if the system fails open/closed?
- Must the device default to no sale when verification cannot be completed?
- What incident register is required?
- What should be reported to the regulator and within what timeframe?

### 8. Pilot authorization

- Is a limited pilot possible inside a licensed estanco?
- What documentation would be required?
- Could a pilot run without real sales first, using simulated transactions?
- Which authority should be consulted first: Comisionado, AEPD/legal counsel, local authority, sector association?

## Recommended validation sequence

1. Prepare a 2-page neutral concept note.
2. Consult specialized legal counsel on tobacco retail + RGPD.
3. Send structured consultation to the Comisionado para el Mercado de Tabacos.
4. Discuss with an estanco association before contacting individual pilots.
5. Run customer discovery with estancos and vending operators.
6. Only after legal feasibility: design hardware pilot.

## Red lines

- Do not claim the system is legally deployable yet.
- Do not claim production-grade biometric validation yet.
- Do not store biometric templates or document numbers in the MVP.
- Do not frame the project as a way to bypass human supervision.
- Do not approach minors or run real age-verification tests without a formal protocol.

## Compliance principles for the MVP

- Default to no sale if verification fails.
- No PII in audit logs.
- Transient biometric processing only.
- Clear privacy notice before verification.
- Data minimization by design.
- Documented incident handling.
- Human escalation path.
- Full separation between demo/pilot data and production assumptions.

## Recommended legal package

For a serious pilot, prepare:

- Technical architecture.
- Data flow diagram.
- DPIA draft.
- Privacy notice.
- Incident response procedure.
- Audit log specification.
- Vendor/subprocessor map.
- Hardware/security risk assessment.
- Comisionado consultation letter.
