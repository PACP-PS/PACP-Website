# PACP — Governance and Membership Rules Mapped from the Supplied Bylaws

**Source:** `النظام الأساسي لجمعية النهائي.doc` (12 pages), supplied in this project conversation.  
**Use:** Product configuration reference only. This is not a legal opinion and does not certify that this is the currently registered/amended version. The association should confirm the approved current copy before production configuration.

## 1. Identity and institutional scope

The supplied bylaws state:
- Name: Palestinian Association of Clinical Psychology Specialists / Charitable Association (PACP), using the Arabic name as written in Article 1.
- Established in Bethlehem under Palestinian Associations and Non-Governmental Organizations Law No. 1 of 2000.
- Main office: Bethlehem, Jerusalem–Hebron Street, Milano Restaurant Building, first floor.
- Geographic scope: Palestine.
- Field: Health.
- The association has a separate legal personality and financial liability (Article 4).

The exact legal Arabic/English naming should be confirmed against the current registration certificate before being fixed in the website footer, contracts, receipts, or payment merchant account.

## 2. Stated objectives (Article 6)

The bylaws list these objectives:
1. Raise awareness of the importance of psychological services in healthcare and improve mental-health service quality through training and supervision programs.
2. Improve access to mental-health services for marginalized groups and strengthen community awareness.
3. Support inclusion of people with disabilities in society and improve quality of life through psychological and rehabilitation programs based on actual needs.

These objectives should inform public website copy, training themes, research calls, and professional initiatives. Do not expand them into unapproved statutory objectives.

## 3. Membership rules (Articles 7–13)

### Application and eligibility
- Membership is personal, non-transferable by proxy/representation, and does not pass by inheritance (Article 7).
- Article 8 allows a legally competent natural or legal person to join when statutory/legal conditions are met.
- Article 9 requires an application to the Board containing: full four-part name, address, date of birth, profession, identity number, and nationality, together with an undertaking to comply with the bylaws and Board decisions.
- The Board decides whether to accept or reject an application. An applicant may object to rejection at the next General Assembly meeting.
- Article 10 states minimum age 18 and no conviction for a felony or a misdemeanor involving dishonour or integrity.

**Important product implication:** The supplied text does not state a requirement that every member must hold a clinical psychology degree or professional license. Do not silently impose that as an eligibility condition. If PACP intends professional-only membership, obtain an approved policy/bylaw amendment or formal authoritative interpretation before configuring eligibility checks.

### Member rights and obligations
- Members may participate and vote personally at General Assembly meetings, with one vote per vote; they may elect and stand for election to the Board.
- Members may participate in association activities and use its services.
- Article 11 states a membership fee of 100 NIS, while also stating that the amount is set by the Board with General Assembly approval. Verify the currently approved amount before showing a live amount or collecting payment.
- Ending membership does not waive outstanding financial obligations.

### Membership categories
The supplied text lists:
1. Active member (عضو عامل)
2. Honorary member (عضو شرف)
3. Supporting member (عضو مؤازر)

The supplied text does not fully specify category-specific eligibility, voting rights, fees, or approval procedures. The application and admin portal should therefore allow configuration only after these details are confirmed; do not assume all categories have identical voting rights.

### Termination and due process (Article 12)
Membership may end through death (or liquidation of a legal entity), withdrawal with written notice to the Board 30 days in advance, or General Assembly decision to dismiss on stated grounds following a Board proposal. The article lists non-payment, failure to comply with the bylaws/decisions, conduct contrary to association objectives, and conviction for an offence involving dishonour or integrity. For specified grounds, written warning, reasonable time to correct, and an opportunity to present a defence are required.

**Product implication:** Membership status changes need reason, supporting record, authorized decision, notice history, and an auditable appeal/defence pathway. Do not implement automatic expulsion solely from an overdue payment flag.

Article 13 states that notices, requests, warnings, and notifications to members are delivered personally in writing or by registered mail to the address in the membership register. Digital notifications can supplement this, but should not silently replace the formal notice method without legal approval.

## 4. Board and roles (Articles 14–18 and related provisions)

- Board consists of seven members elected by the General Assembly for a two-year term (Article 14); the first Board was for one year.
- The Board manages association affairs, prepares internal regulations and instructions, appoints staff, forms committees, prepares financial statements/budgets and annual reports, convenes the General Assembly, and follows up with the competent ministry (Article 15).
- The Board selects from among its members a Chair, Vice-Chair, Secretary, and Treasurer (Article 16).
- The Chair (or Vice-Chair in absence) represents the association and signs correspondence/contracts/agreements approved by the Board; certain financial instruments require joint signatures with the Treasurer.
- The Secretary maintains minutes and records, reports membership movements/changes to the competent authorities within the stated period, oversees administrative affairs, and handles membership applications.
- The Treasurer oversees financial resources, receipts, deposits, records, supporting documents, financial reporting, and execution of Board financial decisions.

**Product implication:** These statutory offices should be represented in governance records, but application-processing and day-to-day platform roles (membership officer, finance officer, content editor, etc.) are operational permissions and must be assigned by the Board; they are not statutory offices in themselves.

## 5. General Assembly (Articles 26–35)

- The General Assembly consists of active members whose membership has been accepted and who have paid financial obligations in accordance with the bylaws and deadlines set by the Board (Article 26).
- It meets at least once per year; members entitled to attend receive written notice with place, date, and agenda at least ten days before the meeting (Article 27).
- Ordinary meeting matters include Board activity report, financial report, auditor report, appointment of auditor, election of a new Board, and general policy direction (Article 29).
- Extraordinary meeting matters include bylaw amendments, removal of Board members/no-confidence, dissolution, and merger/union (Article 30).
- Quorum and voting thresholds are specified in Articles 31 and 33 and should be encoded only after legal review of the supplied wording and applicable law.
- Minutes are required for General Assembly meetings and signed by the Secretary and Chair (Article 34).

**Product implication:** A future member portal may support meeting notices, agenda documents, attendance, minutes, and voting records, but electronic voting should not be activated until its legal validity, identity verification, secrecy, quorum calculation, and audit requirements are formally approved.

## 6. Finance (Articles 36–40)

The bylaws identify membership subscriptions, unconditional donations/grants with approved receipts, lawful proceeds from association activities, and other Board-determined resources as financial sources (Article 36). They require an annual budget/financial year and accounting oversight (Article 37), deposit of funds with approved banks and notice to the competent authorities (Article 38), use of funds for association objectives (Article 39), and annual submission of accounting books and financial report within the stated period (Article 40).

**Payment product implication:** Online payments remain a verification-and-contracting workstream. Before activation, the Board/Treasurer must approve the payment provider, bank settlement destination, receipt format, accounting reconciliation, refunds, fee treatment, and reporting. The website must not present online payment as available before these controls are operational.

## 7. Committees and other provisions

- Article 44 permits the association to form working committees to achieve its objectives.
- Article 45 prohibits political activity and secret associations.
- Other legal and regulatory provisions in the supplied bylaws must be considered in public content and governance workflows.

## 8. Configuration decisions and items requiring confirmation

| Area | Supported by supplied bylaws | Confirmation required before production |
|---|---|---|
| Legal name and registration details | Arabic name and legal basis appear in Article 1 | Exact current registered Arabic/English name and registration certificate |
| Geographic scope / field | Palestine / Health | No additional geographic or practice claims |
| Objectives | Three objectives in Article 6 | Board-approved public wording/translation |
| Eligibility | Legal competence; minimum age 18; specified conviction exclusion | Whether professional qualification is additionally required |
| Application fields | Name, address, DOB, profession, ID number, nationality, undertaking | Which fields are essential, secure collection/retention, privacy notice |
| Approval authority | Board | Delegation to Secretary/membership officer and Board decision workflow |
| Categories | Active, honorary, supporting | Category-specific rights, eligibility, dues, voting |
| Fee | 100 NIS stated; Board sets amount with General Assembly approval | Current approved fee and any category-specific fee |
| Renewal | Financial obligations and membership termination rules are addressed | Renewal period, grace period, reminder cadence, reactivation policy |
| Notices | Written personal delivery or registered mail | Legal approval for digital notice as supplementary or substitute |
| Board | Seven elected members, two-year term | Current board names/terms and public disclosure consent |
| Payment | Membership subscriptions and other financial sources | Providers, merchant approval, bank, currencies, receipts, refunds |
| Online voting | General Assembly voting rights and quorum provisions | Legal approval and secure voting protocol |

## 9. Required governance sign-off before launch

Request Board/Secretary/Treasurer confirmation of:
1. Whether this is the current approved and registered bylaws version, including all amendments.
2. Exact legal name, registration number, and official English name.
3. Whether membership is open to any legally competent person/entity or limited by an approved professional qualification rule.
4. Current membership fee, fee categories, due date, renewal period, and grace period.
5. Rights and duties of active, honorary, and supporting members, especially voting and candidacy.
6. Whether membership application decisions may be delegated and what appeal route applies.
7. Whether digital notices, electronic signatures, and electronic General Assembly participation/voting are legally accepted.
8. Approved payment and accounting workflow before any online collection is enabled.

