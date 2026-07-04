# Regulatory framework mapping

This note maps the technical design of the project against the Spanish and EU norms that govern it. It is intended as a working reference for technical and legal reviewers, not as a substitute for qualified legal counsel.

> **Disclaimer.** This document reflects the author's interpretation of the applicable regulatory framework as of May 2026, after the entry into force of Circular 1/2025 of the *Comisionado para el Mercado de Tabacos* (2 January 2026). It is part of an active regulatory engagement and may be updated as the consultation with the regulator progresses.

---

## 1. Why a vending-machine model, and not a kiosk for tobacconist premises

Under Article 4 of Law 28/2005 and Article 25.Two of Royal Decree 1199/1999 (in the wording given by Royal Decree 1676/2011), automated sale of tobacco products in Spain is only permitted through vending machines installed in a closed list of venue types: hospitality establishments (bars, restaurants and similar), hotels and analogous accommodation, convenience stores in service stations, gaming venues and press kiosks. Tobacconist premises (*estancos*) operate under a manual-sale regime carried out by the licensed *expendedor*.

For this reason, the project is positioned in two complementary scenarios:

- **Primary scenario** — a *homologable model of vending machine* under Circular 1/2025, to be installed in the venues authorised by Article 25.Two RD 1199/1999.
- **Secondary scenario** — a *compliance assistance tool* deployed inside tobacconist premises, supporting (not replacing) the human age check by the *expendedor*. This is a subsidiary line of inquiry, currently part of the open regulatory consultation.

The biometric verification module is the same in both cases; what changes is the legal qualification of the product (vending machine vs. internal compliance tool) and the corresponding procedure.

---

## 2. Norm-by-norm mapping

### 2.1 Law 13/1998, on the organisation of the tobacco market

Establishes the licensing regime for the Spanish tobacco market. Relevant insofar as it provides the institutional framework within which the *Comisionado para el Mercado de Tabacos* acts as the authorising authority for vending-machine models.

### 2.2 Law 28/2005 — Article 4

Defines vending machines and lays down the foundational rules for their operation: prohibition of sale to minors, requirement of direct supervision by the venue holder, restriction to the venues listed in the implementing regulation. The biometric verification system is designed as a **technical reinforcement** of the legal duty of the venue holder, not as a replacement for it. The system blocks dispensation when:

- The DNIe cannot be read or the signature does not validate against FNMT-RCM.
- The liveness check is below the configured threshold per ISO/IEC 30107-3 principles.
- The 1:1 facial match between the DNIe photo and the live capture is below the configured cosine-distance threshold.
- The calculated age, derived from the date of birth read from the chip, is below 18.

### 2.3 Law 28/2005 — Article 9

Prohibits advertising, promotion and sponsorship of tobacco products. The project addresses this by:

- Limiting the on-screen product representation to the strictly informational minimum (product reference, format and price), with no promotional language, animation, sound or imagery designed to incite consumption.
- Treating the screen as a sales surface and not an advertising surface — a point on which the regulatory consultation explicitly asks for guidance from the *Comisionado*.

### 2.4 Law 28/2005 — Article 19

Governs the sanction regime. The project's design proactively considers the attribution of sanctioning responsibility between the venue holder, the authorised manufacturer of the model and, where applicable, the technical operator of the verification solution. The consultation to the *Comisionado* requests guidance on this point.

### 2.5 Royal Decree 1199/1999 — Article 25.Two (as amended by RD 1676/2011)

Lists the venues where tobacco vending machines may be installed. The project's primary scenario is anchored on this list. The project does **not** propose vending in venues outside this list.

### 2.6 Circular 1/2025 of the Comisionado para el Mercado de Tabacos

This is the procedural anchor for the project. Published on 15 December 2025 and in force since 2 January 2026, the Circular consolidates the procedure for authorising, modifying or altering vending-machine models and regulates the operation of the Vending Machine Registry. The project's roadmap follows this procedure step by step: technical documentation, ENAC-accredited testing where applicable, model authorisation, registry inscription.

The Circular replaces the previous Resolution of 20 September 2006 of the *Comisionado*. The consultation requests guidance on which technical criteria, in particular regarding the activation mechanism at a distance by the venue holder, are now applicable in lieu of those previously set out.

### 2.7 RDL 17/2017, transposing Directive 2014/40/EU

Governs labelling, health warnings and the presentation of tobacco products. The project takes the health warnings on the product packaging as given and addresses the question of whether additional on-screen warnings are required as part of the regulatory consultation.

### 2.8 Regulation (EU) 2016/679 (GDPR) and Organic Law 3/2018

The biometric processing is a Special Category of personal data under Article 9 GDPR. The project's design implements:

- **Lawful basis**: explicit consent (Article 9(2)(a) GDPR), reinforced by the legal duty of age verification.
- **Data minimisation**: biometric data is processed in volatile memory only; no facial images, embeddings or DNIe data are persisted.
- **Storage limitation**: audit records contain only an HMAC-based anonymised token derived from the document number, with a daily-rotating salt. No PII is stored.
- **Security of processing** (Article 32): secure memory wiping on every code path; cryptographic validation against the FNMT-RCM trust chain.
- **DPIA / EIPD** (Article 35): planned, given the systematic processing of biometric data and the involvement of minors-related controls.
- **Prior consultation with AEPD** (Article 36): under consideration depending on the DPIA outcome.

### 2.9 Commission Delegated Regulation (EU) 2018/574 — Traceability

The project's design contemplates reading the Unique Identifier (UI) of each package dispensed and reporting it to the European traceability system through the existing operator channels. The consultation requests guidance on the specifics applicable to the automated dispensation cycle.

---

## 3. What the consultation to the Comisionado asks

The formal consultation submitted to the *Comisionado para el Mercado de Tabacos* — see [`consultation-cmt.md`](consultation-cmt.md) for the anonymised version — articulates 16 questions across seven thematic blocks plus one subsidiary block, covering:

1. Whether the model fits the legal concept of "vending machine".
2. The relationship between automated biometric activation and the legal duty of activation at a distance by the venue holder.
3. The documentation required in the authorisation file under Circular 1/2025.
4. On-screen information, health warnings and the prohibition of advertising.
5. Fiscal traceability and excise stamps in automated dispensation.
6. Coordination with the AEPD.
7. Attribution of sanctioning responsibility.
8. *Subsidiary*: use of the system as a compliance assistance tool inside tobacconist premises.

---

## 4. What this document is **not**

- A legal opinion. It is a working note prepared by the author of the project.
- A guarantee that a model built along the lines described here will be authorised. The procedure of Circular 1/2025 is the only authoritative path.
- A substitute for the DPIA that must be carried out before any real processing of biometric data.

For real-world deployment, qualified legal counsel specialised in the Spanish tobacco regulatory framework and in data protection is required.
