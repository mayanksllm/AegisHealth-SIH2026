# AegisHealth: Sensor-Verified, Append-Only Patient Case-Taking System
> **Smart India Hackathon 2026** | **Problem Statement ID:** SIH26047  
> **Ministry:** Ministry of Ayush | **Category:** Software (with Hardware-Attested Data Feeds)

---

## 1. Executive Summary
Ayush clinical documentation often suffers from subjective retrospective charting and lack of verifiable, tamper-evident physiological baselines. **AegisHealth** is an end-to-end digital case-taking and repertorization suite paired with **AegisNode**—an open, opto-isolated capture-layer tap. 

AegisNode non-invasively connects to clinical diagnostic interfaces, cryptographically attests each vital sign packet in dedicated silicon (Microchip ATECC608A) at the exact millisecond of capture, and anchors batches into an append-only cryptographic ledger. 

Every case record in AegisHealth is compliant with the **Digital Personal Data Protection (DPDP) Act 2023** and natively interoperates with the **Ayushman Bharat Digital Mission (ABDM)** via HL7 FHIR R4.

---

## 2. System Architecture
[Diagnostic Device / Ayush Exam]
│ RS-232 / UART / Bluetooth
▼
[AegisNode Hardware Tap] ──► ATECC608A (ECDSA P-256 Signature + Monotonic Counter)
│ Encrypted BLE 5.0 / Wi-Fi
▼
[AegisHealth Clinical Gateway] ──► FHIR R4 Conversion + Ayush Case-Taking Database (TimescaleDB)
│ 5-Minute Batch Merkle Aggregation
▼
[Cryptographic Notarization Layer] ──► Append-Only Merkle Roots (KSI Model / RFC 3161)
│
▼
[Clinical Frontends] ──► Ayush Case-Taking UI & ABDM M1/M2/M3 Bridge

---

## 3. Core Capabilities
* **Objective Ayush Case-Taking:** Integrates subjective symptomatology with verified physical telemetry.
* **Silicon-Rooted Non-Repudiation:** Cryptographic signatures generated on-chip; the private key never leaves the ATECC608A secure element.
* **"Logged, Not Blocked" Safety:** Emergency procedures bypass validation locks with a single action; overrides are cryptographically logged for auditability.
* **Offline Store-and-Forward:** 72-hour circular flash buffer (W25Q256) retains records during network dropouts; monotonic counters prevent reordering or insertion.
* **DPDP-2023 Native Privacy:** Raw Protected Health Information (PHI) stays strictly on-premises; only mathematical SHA-256 Merkle roots leave the hospital boundary.

---

## 4. Hardware Bill of Materials (BOM)
| Component | Part Model | Functional Role | Cost (Proto / Prod) |
| :--- | :--- | :--- | :--- |
| Microcontroller | ESP32-S3-WROOM-1 | Dual-core compute, FreeRTOS, BLE/Wi-Fi | ₹380 / ₹270 |
| Secure Element | Microchip ATECC608A | ECDSA P-256 signing, monotonic counters | ₹85 / ₹62 |
| Isolation Barrier | MAX3232 + 6N137 | 2.5 kV galvanic isolation (IEC 60601-1) | ₹110 / ₹75 |
| Flash Memory | Winbond W25Q256 (32MB) | 72-hour circular offline FIFO storage | ₹45 / ₹32 |
| Enclosure & DC-DC | Medical-grade ABS + PSU | Isolated power tap and durable casing | ₹160 / ₹95 |
| **Total BOM** | — | — | **₹780 / ₹534** |

---

## 5. Live Jury Evaluation Quickstart
```bash
cd verification
python3 verify_merkle_proof.py --proof sample_proof.json
python3 verify_merkle_proof.py --proof sample_proof.json --tamper
```
