# PrimarySources — AI reading map

Use this file first when working from `PrimarySources/`. It tells you **what each document is**, **which copy to open**, and **in what order**. It does not interpret the case.

**Facts-only digest (no analysis):** [`CORE-INFORMATION.md`](CORE-INFORMATION.md)  
**Human-readable conversions:** [`readable/`](readable/)  
**Originals (authoritative if anything conflicts):** this folder’s `.htm`, `.pdf`, `.docx`

---

## Rules for agents

1. **Prefer SEC HTML originals** (`CHTR-10-K-*.htm`, `CHTR-10-Q-*.htm`, `*-Ex99.1.htm`) when a number is in dispute. Readable markdown in `readable/` has been cleaned for scanning (tables, headings, less boilerplate); it is still a conversion.
2. **Do not mix customer-count bases.** In Q4 2025 Charter restated customer statistics to include all mobile customers (including mobile-only) and added “total connectivity customers.” FY2024 figures in the FY2025 10-K are restated. FY2023 figures in the FY2024 10-K use the prior methodology.
3. **Trending schedules** (`CHTR-*-Trending-Schedule.md`) are **unofficial** MarketScreener extracts. Charter IR PDFs 404’d. Cross-check any trending number against Exhibit 99.1 or the 10-K/10-Q.
4. **Do not treat [`CORE-INFORMATION.md`](CORE-INFORMATION.md) as analysis.** It restates disclosed figures and quoted statements only.
5. Course Word files describe the **assignment**. Interpretive language in the Team Case Brief is the brief’s language, not a filing fact.
6. Books and HBR are not in this folder.

---

## Suggested reading order

| Step | Open | Why |
|---|---|---|
| 1 | [`CORE-INFORMATION.md`](CORE-INFORMATION.md) | Disclosed identity, customers, financials, deals, Q1 2026, Q2 2026 |
| 2 | [`readable/FoC-Team-Case-Brief.md`](readable/FoC-Team-Case-Brief.md) | Mandate, dates, rubric |
| 3 | [`readable/CHTR-Q1-2026-Earnings-Release-Ex99.1.md`](readable/CHTR-Q1-2026-Earnings-Release-Ex99.1.md) | Q1 2026 operating and financial tables (assignment anchor) |
| 4 | [`readable/CHTR-Q2-2026-Earnings-Release-Ex99.1.md`](readable/CHTR-Q2-2026-Earnings-Release-Ex99.1.md) | Q2 2026 operating and financial tables (later public facts) |
| 5 | [`readable/CHTR-FY2025-Earnings-Release-Ex99.1.md`](readable/CHTR-FY2025-Earnings-Release-Ex99.1.md) | FY2025 operating and financial tables |
| 6 | [`readable/CHTR-10-K-FY2025.md`](readable/CHTR-10-K-FY2025.md) | Item 1 Business, Item 1A Risk Factors, Item 7 MD&A, financial statements |
| 7 | [`readable/CHTR-10-Q-Q1-2026.md`](readable/CHTR-10-Q-Q1-2026.md) | Q1 MD&A, leverage, capex, deal updates |
| 8 | [`readable/CHTR-10-Q-Q2-2026.md`](readable/CHTR-10-Q-Q2-2026.md) | Q2 MD&A, leverage 4.18x, updated Cox cash terms |
| 9 | [`readable/CHTR-Cox-Announcement-Press-Release.md`](readable/CHTR-Cox-Announcement-Press-Release.md) | Cox transaction as announced May 16, 2025 |
| 10 | [`readable/CHTR-10-K-FY2024.md`](readable/CHTR-10-K-FY2024.md) | FY2023 comparatives; **old** customer methodology |
| 11 | Originals in this folder | Verify a specific figure |

Course narrative (secondary to filings): [`readable/FoC-CHTR-Background.md`](readable/FoC-CHTR-Background.md)

---

## Catalog

Each row: **original** (authoritative) → **readable/** (for humans and models).

### Course documents

| Original | Readable | Contents |
|---|---|---|
| `FoC-Team Case Brief (1).docx` | [`readable/FoC-Team-Case-Brief.md`](readable/FoC-Team-Case-Brief.md) | Role, CEO charge, situation as of Q1 2026, deliverables, timeline, 40-point rubric |
| — | [`readable/CHTR-Critical-Tables.xlsx`](readable/CHTR-Critical-Tables.xlsx) | Critical tables only: snapshot, customers, quarterly trend, revenue, P&L, FCF, capex, balance sheet, Q1 2026, Q2 2026, deals |

### SEC filings

| Original | Readable | Period / accession |
|---|---|---|
| `CHTR-10-K-FY2025.htm` | [`readable/CHTR-10-K-FY2025.md`](readable/CHTR-10-K-FY2025.md) | Year ended 31 Dec 2025; filed 30 Jan 2026; 0001091667-26-000017 |
| `CHTR-10-K-FY2024.htm` | [`readable/CHTR-10-K-FY2024.md`](readable/CHTR-10-K-FY2024.md) | Year ended 31 Dec 2024; 0001091667-25-000034 |
| `CHTR-10-Q-Q1-2026.htm` | [`readable/CHTR-10-Q-Q1-2026.md`](readable/CHTR-10-Q-Q1-2026.md) | Quarter ended 31 Mar 2026; filed 24 Apr 2026; 0001091667-26-000028 |
| `CHTR-8-K-2026-01-30.htm` | [`readable/CHTR-8-K-2026-01-30.md`](readable/CHTR-8-K-2026-01-30.md) | Item 2.02 FY2025 results |
| `CHTR-FY2025-Earnings-Release-Ex99.1.htm` | [`readable/CHTR-FY2025-Earnings-Release-Ex99.1.md`](readable/CHTR-FY2025-Earnings-Release-Ex99.1.md) | Exhibit 99.1 to that 8-K |
| `CHTR-8-K-2026-04-24.htm` | [`readable/CHTR-8-K-2026-04-24.md`](readable/CHTR-8-K-2026-04-24.md) | Item 2.02 Q1 2026 results |
| `CHTR-Q1-2026-Earnings-Release-Ex99.1.htm` | [`readable/CHTR-Q1-2026-Earnings-Release-Ex99.1.md`](readable/CHTR-Q1-2026-Earnings-Release-Ex99.1.md) | Exhibit 99.1 to that 8-K |
| `CHTR-10-Q-Q2-2026.htm` | [`readable/CHTR-10-Q-Q2-2026.md`](readable/CHTR-10-Q-Q2-2026.md) | Quarter ended 30 Jun 2026; filed 24 Jul 2026; 0001091667-26-000052 |
| `CHTR-8-K-2026-07-24.htm` | [`readable/CHTR-8-K-2026-07-24.md`](readable/CHTR-8-K-2026-07-24.md) | Item 2.02 Q2 2026 results |
| `CHTR-Q2-2026-Earnings-Release-Ex99.1.htm` | [`readable/CHTR-Q2-2026-Earnings-Release-Ex99.1.md`](readable/CHTR-Q2-2026-Earnings-Release-Ex99.1.md) | Exhibit 99.1 to that 8-K |

### IR PDFs (same earnings content as Ex 99.1, plus slides / Cox)

| Original | Readable | Contents |
|---|---|---|
| `CHTR-FY2025-Earnings-Release.pdf` | [`readable/CHTR-FY2025-Earnings-Release.md`](readable/CHTR-FY2025-Earnings-Release.md) | IR PDF of FY2025 press release |
| `CHTR-Q1-2026-Earnings-Release.pdf` | [`readable/CHTR-Q1-2026-Earnings-Release.md`](readable/CHTR-Q1-2026-Earnings-Release.md) | IR PDF of Q1 2026 press release |
| `CHTR-FY2025-Results-Presentation.pdf` | [`readable/CHTR-FY2025-Results-Presentation.md`](readable/CHTR-FY2025-Results-Presentation.md) | 19-page results slides, 30 Jan 2026 |
| `CHTR-Cox-Announcement-Press-Release.pdf` | [`readable/CHTR-Cox-Announcement-Press-Release.md`](readable/CHTR-Cox-Announcement-Press-Release.md) | Combination announced 16 May 2025 |
| `CHTR-Cox-Presentation.pdf` | [`readable/CHTR-Cox-Presentation.md`](readable/CHTR-Cox-Presentation.md) | Investor presentation for that announcement |

Charter IR “static-files” links for the Q2 2026 press release and results presentation returned HTML stubs, not PDFs. Use `CHTR-Q2-2026-Earnings-Release-Ex99.1.htm` for Q2 2026. No unofficial Q2 trending extract is in this folder; Ex99.1 / 10-Q are the sources.

### Trending schedules (unofficial)

| File | Readable | Note |
|---|---|---|
| `CHTR-FY2025-Trending-Schedule.md` | [`readable/CHTR-FY2025-Trending-Schedule.md`](readable/CHTR-FY2025-Trending-Schedule.md) | MarketScreener extract of 4Q25 trending schedule |
| `CHTR-Q1-2026-Trending-Schedule.md` | [`readable/CHTR-Q1-2026-Trending-Schedule.md`](readable/CHTR-Q1-2026-Trending-Schedule.md) | MarketScreener extract of 1Q26 trending schedule |

---

## Where numbers live (quick pointers)

| Topic | Primary readable file | Section cue |
|---|---|---|
| What Charter says it is / products / footprint | `readable/CHTR-10-K-FY2025.md` | Item 1. Business |
| YE2025 customer table | same, or Ex 99.1 FY2025 | “Customer statistics” / operating statistics |
| Competition overlap (AT&T / Verizon %) | `readable/CHTR-10-K-FY2025.md` | Item 1 — Competition |
| Cox / Liberty deal terms | 10-K Item 1; Cox press release | “Cox Transactions” / “Liberty Broadband Combination” |
| FY2025 P&L, BS, cash flow | 10-K Item 8 | CONSOLIDATED STATEMENTS |
| FY2025 revenue by product | 10-K Item 7 | “Revenues by service offering” |
| FY2025 capex by NCTA category | 10-K Item 7 | capital expenditures tables |
| Q1 2026 customers and P&L | `readable/CHTR-Q1-2026-Earnings-Release-Ex99.1.md` | bullets + tables |
| Q1 2026 MD&A, leverage 4.15x, capex | `readable/CHTR-10-Q-Q1-2026.md` | Item 2 MD&A / liquidity |
| Q2 2026 customers and P&L | `readable/CHTR-Q2-2026-Earnings-Release-Ex99.1.md` | bullets + tables |
| Q2 2026 MD&A, leverage 4.18x, Cox $650M / $12.4B | `readable/CHTR-10-Q-Q2-2026.md` | Item 2 MD&A / liquidity |
| Assignment constraints | `readable/FoC-Team-Case-Brief.md` | entire brief |

---

## Outside this folder

Repo root [`../CHTR-Case-Background.md`](../CHTR-Case-Background.md) mixes filings with **class notes and framing**. Do not use it as a source of facts without checking this folder. Repo root [`../README.md`](../README.md) is the human entry map.
