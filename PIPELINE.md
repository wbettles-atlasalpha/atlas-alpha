# Operational Pipeline: NSW Liquor License Lead Harvester

## Step 1: Ingestion
- Trigger: Daily `cron` job scans `Liquor & Gaming NSW` Noticeboard.
- Scraper: `scripts/liquor_scraper.py`
- Output: `leads.json` (Structured: Business Name, License Type, Address, Submission Date).

## Step 2: Enrichment & Asset Generation
- Processing: AI matches leads to subscribed "Business DNA" profiles.
- Asset: Auto-generate 3-paragraph personalized pitch (Case Study + Testimonial + CTA).
- Delivery: Email notification to customer: "New lead in your area: [Business Name]."

## Step 3: Outreach Execution
- Interface: Simple Streamlit dashboard (or email button link).
- Customer Action: Click "Generate Pitch."
- Output: Pre-filled draft pitch in their email client (or direct copy-paste to CRM).

## Step 4: Closed-Loop Tracking
- Feedback: Customers flag leads as "Responded" / "Won" / "Lost" in the dashboard.
- Analytics: Feed "Won" data back into the "Business DNA" profile to strengthen future pitches.
