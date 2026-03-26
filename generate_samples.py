from fpdf import FPDF
import os

os.makedirs("sample_docs", exist_ok=True)

def make_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, content)
    pdf.output(f"sample_docs/{filename}")
    print(f"Created: {filename}")

make_pdf("private_placement_memo.pdf", "PRIVATE PLACEMENT MEMORANDUM",
"""NovaTech LLC
Delaware Limited Liability Company

OFFERING OF SERIES A PREFERRED UNITS
Up to $5,000,000 at $4.50 per unit
Minimum Investment: $25,000

This offering is made pursuant to Rule 506(c) of Regulation D under the Securities Act of 1933. Securities are offered exclusively to accredited investors.

COMPANY OVERVIEW
NovaTech LLC is a Delaware limited liability company formed January 2024, developing an AI-powered carbon credit verification platform. The platform reduces audit time by 70% using machine learning and blockchain-based verification.

MANAGEMENT
Javier Martinez, CEO - 12 years climate tech, VP Product CarbonTrack (acquired by Salesforce 2022), MBA Stanford GSB
Sarah Chen, CTO - 15 years distributed systems, Principal Engineer AWS, MS CS MIT
Raj Patel, CFO - 10 years venture finance, Controller at two Series B startups, CPA, MBA Wharton

OFFERING TERMS
Total Raise: $5,000,000
Price Per Unit: $4.50
Units Offered: 1,111,111
Pre-money Valuation: $18,000,000
Post-money Valuation: $23,000,000
Minimum Investment: $25,000
Lockup Period: 12 months
Investor Qualification: Accredited investors only (Rule 506(c))

USE OF PROCEEDS
40% - Platform development
25% - Sales and marketing
20% - Operations
15% - Reserve

TOKENIZATION
NovaTech LLC intends to tokenize the Series A Preferred Units via tZERO's regulated infrastructure following closing. Tokens will be issued as ERC-1400 security tokens on the Ethereum blockchain.

LEGAL COUNSEL
Kirkland & Ellis LLP

RISK FACTORS
1. Market risk - carbon credit markets are subject to regulatory change
2. Technology risk - AI platform may not achieve projected accuracy
3. Key person risk - dependence on founding team
4. Liquidity risk - no established secondary market prior to tZERO ATS listing
5. Regulatory risk - securities regulations may change
6. Early-stage risk - company has limited operating history

THIS IS NOT A PUBLIC OFFERING. THIS DOCUMENT IS CONFIDENTIAL.""")

make_pdf("series_a_subscription_agreement.pdf", "SERIES A SUBSCRIPTION AGREEMENT",
"""NovaTech LLC
Series A Preferred Units Subscription Agreement

ISSUER: NovaTech LLC, a Delaware limited liability company
GOVERNING LAW: State of Delaware

SUBSCRIPTION TERMS
Price Per Unit: $4.50
Lockup Period: 12 months from closing
Anti-dilution Protection: Weighted average broad-based
Drag-Along Rights: Triggered at 67% majority vote
Pro-Rata Rights: Included for future rounds

REPRESENTATIONS AND WARRANTIES
Subscriber hereby represents and warrants that:
1. Subscriber is an accredited investor as defined under Rule 501 of Regulation D
2. Subscriber has received and reviewed the Private Placement Memorandum
3. Subscriber understands the securities have not been registered under the Securities Act
4. Subscriber can bear the economic risk of this investment

CURRENT SUBSCRIPTION STATUS
Aggregate subscriptions received to date: approximately $1,800,000

TRANSFER RESTRICTIONS
Units may not be transferred without manager consent and compliance with applicable securities laws. Units are subject to a 12-month lockup period from the date of closing.

ACCREDITED INVESTOR CERTIFICATION
Subscriber certifies they meet accredited investor standards under Rule 501(a).

Signatures required from both Subscriber and NovaTech LLC authorized representative.

Counsel: Kirkland & Ellis LLP""")

make_pdf("operating_agreement_v3.pdf", "AMENDED AND RESTATED OPERATING AGREEMENT OF NOVATECH INC.",
"""Amended and Restated Operating Agreement of NovaTech Inc.
(A Delaware Limited Liability Company)

NOTE: This agreement governs the operations of the company.

MANAGEMENT
Manager-managed structure. Javier Martinez serves as Managing Member with authority to bind the company.

VOTING
Major decisions require 67% approval of outstanding units. This includes:
- Sale of substantially all assets
- Merger or acquisition
- Issuance of new unit classes
- Amendment of this agreement

DISTRIBUTION WATERFALL
1. Return of capital to all members (pro-rata)
2. 8% preferred return to Series A holders
3. Remaining distributions pro-rata to all members

TRANSFER RESTRICTIONS
Right of first refusal applies to all proposed unit transfers. Manager consent required for any transfer. Transfers must comply with applicable securities laws.

NON-COMPETE
Members holding more than 5% of units agree to a 24-month non-compete following departure.

GOVERNING LAW
State of Delaware""")

make_pdf("investor_questionnaire_template.pdf", "ACCREDITED INVESTOR QUESTIONNAIRE",
"""NovaTech LLC
Accredited Investor Questionnaire
Rule 506(c) Offering

ACCREDITATION CRITERIA (check all that apply)

Individual Standards:
[ ] Annual income exceeding $200,000 in each of the two most recent years ($300,000 joint with spouse)
[ ] Net worth exceeding $1,000,000 (excluding primary residence)
[ ] Holds in good standing a Series 7, 65, or 82 license

Entity Standards:
[ ] Entity with total assets exceeding $5,000,000
[ ] All equity owners are accredited investors

SUITABILITY ASSESSMENT
Investment experience: [ ] None [ ] Limited [ ] Moderate [ ] Extensive
Risk tolerance: [ ] Conservative [ ] Moderate [ ] Aggressive
Time horizon: [ ] Less than 3 years [ ] 3-5 years [ ] 5+ years
Can sustain total loss: [ ] Yes [ ] No

REPRESENTATIONS
I have received and carefully reviewed the Private Placement Memorandum.
I understand this investment involves substantial risk.
I understand the securities are illiquid and subject to transfer restrictions.
I am making this investment for my own account.

SIGNATURE
Investor Name: _______________________
Signature: _______________________
Date: _______________________

NOTE: Rule 506(c) requires THIRD-PARTY VERIFICATION of accredited investor status. Self-certification alone is not sufficient. Please provide verification through VerifyInvestor.com or equivalent service.""")

make_pdf("side_letter_anchor.pdf", "SIDE LETTER AGREEMENT - ANCHOR INVESTOR",
"""CONFIDENTIAL - INTERNAL ONLY

Side Letter Agreement
Between NovaTech LLC and Meridian Ventures Fund II, LP

ANCHOR INVESTMENT
Investor: Meridian Ventures Fund II, LP
Investment Amount: $750,000
Price Per Unit: $4.50

MOST FAVORED NATION
NovaTech LLC agrees to provide Meridian Ventures Fund II, LP with any terms more favorable than those in this agreement that are subsequently offered to other investors in this round.

BOARD OBSERVER RIGHTS
Meridian Ventures Fund II, LP is entitled to appoint one non-voting board observer for as long as they hold at least 50% of their initial investment.

REPORTING REQUIREMENTS
NovaTech LLC shall provide quarterly financial reports within 45 days of quarter end and annual audited financials within 90 days of fiscal year end.

INFORMATION RIGHTS
Meridian Ventures Fund II, LP shall have access to financial statements, budgets, and material business information upon reasonable request.

CO-INVESTMENT RIGHTS
Meridian Ventures Fund II, LP has the right to co-invest up to $2,000,000 in NovaTech LLC's next financing round on the same terms.

CONFIDENTIALITY
This side letter is confidential. Terms are not to be disclosed to other investors or third parties.

Executed as of the date signed below.
Counsel: Kirkland & Ellis LLP""")

make_pdf("cap_table_march_2026.pdf", "CAP TABLE - MARCH 2026",
"""NovaTech LLC
Capitalization Table
As of March 2026

PRE-MONEY VALUATION: $18,000,000
POST-MONEY VALUATION: $23,000,000

UNIT SUMMARY
Total Units Outstanding (pre-Series A): 4,000,000
Series A Units Offered: 1,111,111
Price Per Unit: $4.50

OWNERSHIP BREAKDOWN (Pre-Series A)
FOUNDERS:
Javier Martinez (CEO): 1,400,000 units - 35.0%
Sarah Chen (CTO): 720,000 units - 18.0%
Raj Patel (CFO): 360,000 units - 9.0%
Founder Total: 2,480,000 units - 62.0%

SEED INVESTORS:
Meridian Ventures Fund II, LP: 480,000 units - 12.0%
Angel Investors (pool): 440,000 units - 11.0%
Seed Total: 920,000 units - 23.0%

EMPLOYEE STOCK OPTION POOL:
Granted: 320,000 units - 8.0%
Available: 280,000 units - 7.0%
ESOP Total: 600,000 units - 15.0%

SERIES A STATUS
Subscriptions received to date: $2,100,000
Units subscribed: 466,667 units

NOTES
All units are subject to applicable transfer restrictions.
Meridian Ventures Fund II anchor investment of $750,000 confirmed per Form D.""")

make_pdf("financial_statements_2025.pdf", "FINANCIAL STATEMENTS FY2025",
"""NovaTech LLC
Unaudited Financial Statements
Fiscal Year Ending December 31, 2025

INCOME STATEMENT

Revenue:
  SaaS Subscription Revenue: $1,200,000
  
Cost of Goods Sold:
  Cloud infrastructure and delivery: $280,000
  
Gross Profit: $920,000
Gross Margin: 76.7%

Operating Expenses:
  Research & Development: $520,000
  Sales & Marketing: $380,000
  General & Administrative: $360,000
  Total OpEx: $1,260,000

Net Loss: ($340,000)

BALANCE SHEET (December 31, 2025)

Assets:
  Cash and Cash Equivalents: $890,000
  Accounts Receivable: $165,000
  Other Current Assets: $45,000
  Property and Equipment (net): $320,000
  Total Assets: $1,420,000

Liabilities:
  Accounts Payable: $95,000
  Accrued Liabilities: $115,000
  Total Liabilities: $210,000

Members' Equity: $1,210,000

KEY METRICS
Monthly Burn Rate: approximately $50,000
Cash Runway: approximately 18 months
Annual Recurring Revenue: $1,200,000

NOTE: These financial statements are unaudited and prepared by management.""")

make_pdf("business_plan_2026.pdf", "BUSINESS PLAN 2026",
"""NovaTech LLC
Business Plan and Growth Strategy 2026

MARKET OPPORTUNITY
The voluntary carbon credit market is projected to reach $50 billion by 2030, growing from approximately $2 billion in 2022. Regulatory pressure and ESG mandates are accelerating enterprise adoption of carbon accounting solutions.

THE PLATFORM
NovaTech's AI-powered verification platform reduces carbon credit audit time by 70% compared to manual processes. The platform uses machine learning to detect fraudulent credits and blockchain for immutable audit trails.

TRACTION
Current Enterprise Customers: 14
Annual Recurring Revenue: $1,200,000
Net Revenue Retention: 118%

REVENUE PROJECTIONS
2026: $3,200,000
2027: $8,500,000
2028: $18,000,000

GO-TO-MARKET STRATEGY
Primary: Direct enterprise sales targeting Fortune 500 sustainability teams
Secondary: Channel partnerships with Big 4 accounting firms

USE OF PROCEEDS FROM SERIES A
40% - Platform development (ML model improvement, API expansion)
25% - Sales and marketing (enterprise sales team expansion)
20% - Operations (infrastructure, compliance, customer success)
15% - Reserve (working capital and contingency)

MANAGEMENT TEAM
Javier Martinez, CEO - 12 years climate tech, Stanford MBA
Sarah Chen, CTO - 15 years distributed systems, MIT MS CS
Raj Patel, CFO - 10 years venture finance, Wharton MBA, CPA

COMPETITIVE ADVANTAGE
First-mover in AI-native carbon credit verification
Blockchain integration creates switching costs
Network effects from verification database""")

make_pdf("term_sheet_final.pdf", "TERM SHEET - SERIES A",
"""NovaTech LLC
Series A Preferred Units - Term Sheet
FINAL - NON-BINDING SUMMARY OF TERMS

OFFERING TERMS
Security: Series A Preferred Units
Amount: $5,000,000
Pre-money Valuation: $18,000,000
Price Per Unit: $4.50
Units: 1,111,111

INVESTOR RIGHTS
Liquidation Preference: 1x non-participating preferred
Anti-dilution: Weighted average broad-based
Pro-Rata Rights: Investors may participate in future rounds
Drag-Along: Triggered at 67% majority vote of all units

GOVERNANCE
Board of Managers: 3 seats total
  2 seats: Founders
  1 seat: Investor (qualifying investment of $2,000,000+)

CLOSING CONDITIONS
1. Completion of tZERO tokenization setup and token issuance agreement
2. Satisfactory completion of legal due diligence
3. Execution of definitive agreements
4. Investor accreditation verification per Rule 506(c)

COUNSEL
Company Counsel: Kirkland & Ellis LLP

This term sheet is non-binding and subject to execution of definitive agreements.""")

make_pdf("form_d_filing.pdf", "SEC FORM D FILING",
"""SECURITIES AND EXCHANGE COMMISSION
FORM D - NOTICE OF EXEMPT OFFERING OF SECURITIES

ISSUER INFORMATION
Name: NovaTech LLC
Jurisdiction: Delaware
Entity Type: Limited Liability Company
Year of Incorporation: 2024

OFFERING INFORMATION
Date of First Sale: January 20, 2026
Date of Filing: January 15, 2026
Type of Securities: LLC Interests
Exemption: Rule 506(c) of Regulation D
Aggregate Offering Amount: $5,000,000
Amount Sold: $750,000
Number of Investors: 1

RELATED PERSONS
Javier Martinez - Executive Officer and Director
Sarah Chen - Executive Officer
Raj Patel - Executive Officer

STATES OF SALE
California, New York, Texas, Florida, Illinois, Massachusetts,
Washington, Colorado, Georgia, North Carolina, Virginia, New Jersey
Total: 12 states

This filing constitutes notice of an exempt offering of securities pursuant to Regulation D under the Securities Act of 1933, as amended.""")

make_pdf("blue_sky_memo.pdf", "BLUE SKY MEMORANDUM",
"""KIRKLAND & ELLIS LLP
Blue Sky Compliance Memorandum

TO: NovaTech LLC
FROM: Kirkland & Ellis LLP
DATE: January 12, 2026
RE: State Securities Law Compliance - Series A Offering

CONCLUSION
The Series A Preferred Units offering of NovaTech LLC qualifies for exemption from state securities registration requirements in the following twelve states:

QUALIFYING STATES
1. California - Section 25102(f) exemption
2. New York - NYSA Section 359-ff exemption
3. Texas - Texas Securities Act Section 5.F exemption
4. Florida - Florida Securities Act Section 517.061(11) exemption
5. Illinois - Illinois Securities Act Section 4(G) exemption
6. Massachusetts - MGL Chapter 110A Section 402(b)(9) exemption
7. Washington - RCW 21.20.320(9) exemption
8. Colorado - CRS 11-51-308(1)(p) exemption
9. Georgia - OCGA 10-5-12(13) exemption
10. North Carolina - NCGS 78A-17(9) exemption
11. Virginia - VA Code 13.1-514(B)(13) exemption
12. New Jersey - NJSA 49:3-50(b)(11) exemption

All exemptions are conditioned on the offering being conducted in compliance with Rule 506(c) of Regulation D, including the requirement that all purchasers be verified accredited investors.

FILING REQUIREMENTS
Notice filings required in: California, New York, Texas, Florida, Illinois

This memorandum is confidential attorney-client communication.
Kirkland & Ellis LLP""")

make_pdf("articles_of_incorporation.pdf", "CERTIFICATE OF FORMATION",
"""CERTIFICATE OF FORMATION
NovaTech LLC
State of Delaware

Filed with the Secretary of State of the State of Delaware
Date of Filing: January 15, 2024

FIRST: The name of the limited liability company is NovaTech LLC.

SECOND: The address of the registered office and the name of the registered agent is:
Corporation Service Company
251 Little Falls Drive
Wilmington, Delaware 19808

THIRD: The purpose of the company is carbon credit verification services and all related and ancillary activities.

FOURTH: The company is authorized to issue Common Units and Preferred Units in such amounts and with such rights as determined by the Board of Managers from time to time.

ORGANIZER
Javier Martinez
NovaTech LLC

Executed as of January 15, 2024
Filed with the Delaware Secretary of State""")

make_pdf("board_resolution_jan2026.pdf", "BOARD RESOLUTION - JANUARY 2026",
"""NovaTech LLC
UNANIMOUS WRITTEN CONSENT OF THE BOARD OF MANAGERS
January 10, 2026

The undersigned, constituting all of the Managers of NovaTech LLC, hereby adopt the following resolutions by unanimous written consent:

RESOLUTION 1 - SERIES A AUTHORIZATION
RESOLVED, that the company is authorized to offer and sell up to $5,000,000 of Series A Preferred Units pursuant to Rule 506(c) of Regulation D at a price of $4.50 per unit.

RESOLUTION 2 - TZERO TOKENIZATION
RESOLVED, that the company is authorized to tokenize the Series A Preferred Units using the ERC-1400 security token standard on the Ethereum blockchain through tZERO's regulated infrastructure.

RESOLUTION 3 - TZERO AGREEMENTS
RESOLVED, that the company is authorized to enter into agreements with:
- tZERO Securities, LLC
- tZERO Transfer Services, LLC
- tZERO Digital Asset Securities, LLC

RESOLUTION 4 - LEGAL COUNSEL
RESOLVED, that Kirkland & Ellis LLP is hereby engaged as legal counsel for the Series A offering.

EXECUTED as of January 10, 2026

/s/ Javier Martinez - Managing Member
/s/ Sarah Chen - Manager
/s/ Raj Patel - Manager""")

make_pdf("tokenization_spec.pdf", "TOKENIZATION SPECIFICATION",
"""NovaTech LLC
Tokenization Technical Specification
Series A Preferred Units

BLOCKCHAIN PARAMETERS
Blockchain: Ethereum
Token Standard: ERC-1400 (Security Token Standard)
Total Supply: 1,111,111 tokens
Price Per Token: $4.50
Token Name: NVTK-A

SMART CONTRACT PARAMETERS
Whitelist Enforcement: Accredited investors only (on-chain credential required)
Geographic Restrictions: United States and EMEA (excluding sanctioned jurisdictions)
Lockup Enforcement: 12-month transfer restriction enforced at contract level
Dividend Distribution: Automated pro-rata distribution via smart contract

CUSTODY AND TRANSFER
Custodian: tZERO Digital Asset Securities, LLC (SEC-registered SPBD)
Transfer Agent: tZERO Transfer Services, LLC
Transfer Restrictions: Manager consent + whitelist verification required for all transfers

SECONDARY TRADING
Trading Venue: tZERO Securities ATS (Alternative Trading System)
Trading Model: Central Limit Order Book (CLOB)
Settlement: On-chain, near-instant settlement
Eligibility: Accredited investors with valid on-chain credentials only

KYC/AML COMPLIANCE
Verification Provider: VerifyInvestor.com (planned)
On-Chain Credential: On-ChainPass (planned)
AML Screening: Required prior to whitelist addition

NOTE: KYC/AML documentation and third-party accreditation verification letters
are required prior to ATS listing and secondary trading enablement.""")

make_pdf("management_bios.pdf", "MANAGEMENT TEAM BIOGRAPHIES",
"""NovaTech LLC
Management Team and Advisory Board

EXECUTIVE TEAM

JAVIER MARTINEZ - Chief Executive Officer
Javier Martinez has 12 years of experience in climate technology and sustainability. He served as VP of Product at CarbonTrack, which was acquired by Salesforce in 2022. He holds an MBA from Stanford Graduate School of Business. Javier founded NovaTech LLC in January 2024 with the vision of making carbon credit markets more transparent and efficient through AI-powered verification.

SARAH CHEN - Chief Technology Officer
Sarah Chen brings 15 years of distributed systems experience to NovaTech. She served as Principal Engineer at Amazon Web Services, leading infrastructure for high-availability data processing systems. She holds an MS in Computer Science from MIT. Sarah architected NovaTech's AI verification engine and blockchain integration layer.

RAJ PATEL - Chief Financial Officer
Raj Patel has 10 years of venture finance experience, having served as Controller at two Series B-stage startups through successful exits. He is a Certified Public Accountant and holds an MBA from The Wharton School. Raj manages NovaTech's financial operations, investor relations, and compliance functions.

ADVISORY BOARD

DR. LISA HUANG - Carbon Markets Advisor
Professor of Environmental Economics at UC Berkeley. Former advisor to the California Air Resources Board. Author of three peer-reviewed papers on voluntary carbon market efficiency.

MARK THOMPSON - Capital Markets Advisor
Former Managing Director, Goldman Sachs ESG and Sustainable Finance. 20 years of structured finance experience. Currently advises three climate tech companies on capital markets strategy.""")

print("\nAll 15 sample documents generated successfully in sample_docs/")


