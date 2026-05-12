# Demo video plan

## Goal

Create a short 90–120 second video that explains the project clearly to recruiters, potential partners, accelerators and early-stage funders.

The video should not claim production readiness. It should present the project as a proof of concept and validation package.

## Core message

> A privacy-by-design verification system for automated sales in regulated sectors, starting with age-restricted retail.

## Recommended structure

### Scene 1 — Problem (0:00–0:15)

Visual: title slide or kiosk mockup.

Narration:

"Automated retail is expanding, but regulated products require more than a normal vending flow. Businesses need to verify legal age, reduce fraud and keep auditable evidence without storing unnecessary personal data."

### Scene 2 — Solution (0:15–0:35)

Visual: `mockups/kiosk-flow.html`, welcome and catalog screens.

Narration:

"This project explores a secure age-verification layer for self-service kiosks and regulated automated sales. The initial use case is a licensed tobacco retail environment in Spain, but the concept can extend to other age-restricted sectors."

### Scene 3 — Verification flow (0:35–0:60)

Visual: architecture diagram from `docs/architecture.md` or simple slide.

Narration:

"The verification workflow is modular: NFC document reading interface, certificate validation interface, liveness detection, 1:1 face matching, legal-age calculation and audit-safe logging. Sensitive buffers are wiped after each session."

### Scene 4 — Technical proof (1:00–1:25)

Visual: terminal running:

```bash
pytest -q
python demo_session.py
```

Narration:

"The current proof of concept includes a Python verification workflow, 51 automated tests, 94 percent coverage, a simulated demo and a touchscreen mockup. Hardware integration is explicitly outside the current scope."

### Scene 5 — Business opportunity (1:25–1:50)

Visual: slide with business model.

Narration:

"The business opportunity is not just a tobacco kiosk. It is a compliance layer for regulated automated sales: licensing per device, SaaS audit dashboard, integration services and hardware-partner deployment."

### Scene 6 — Next step (1:50–2:00)

Visual: final slide.

Narration:

"The next step is legal validation, customer discovery and a pilot-ready MVP with an industry partner."

## Recording checklist

- Open GitHub repository.
- Show README briefly.
- Open mockup HTML.
- Run tests.
- Run demo script.
- Show architecture doc.
- End on one-pager or pitch slide.

## Tone

Professional, calm and factual. Avoid hype. Use phrases like:

- "proof of concept"
- "pilot-ready validation"
- "privacy by design"
- "regulated-sector compliance"
- "hardware integration out of scope at this stage"

## Tools

Simple options:

- OBS Studio for screen recording.
- PowerPoint/Canva for title slides.
- Clipchamp or CapCut for light editing.
- Optional voiceover in Spanish and English versions.

## Suggested title

**Secure Age Verification for Regulated Automated Retail — Proof of Concept**
