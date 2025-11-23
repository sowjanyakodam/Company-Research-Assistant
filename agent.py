# agent.py
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
MOCK = not API_KEY

if not MOCK:
    client = Groq(api_key=API_KEY)

# ------------------------------------------------------
# Section Titles (fixed sequence)
# ------------------------------------------------------
SECTION_TITLES = [
    "Company Overview",
    "Recent News",
    "Products / Services",
    "Competitors",
    "Key Opportunities / Signals",
    "Suggested Next Steps",
]


# ------------------------------------------------------
# Utility: Split HTML plan into sections
# ------------------------------------------------------
def split_into_sections(plan_text: str):
    sections = {}
    for title in SECTION_TITLES:
        pattern = rf"<div class='section-title'>{title}</div>(.*?)(?=<div class='section-title'>|$)"
        match = re.search(pattern, plan_text, re.S)
        if match:
            sections[title] = match.group(1).strip()
    return sections


# ------------------------------------------------------
# LLM: Generate Full Account Plan
# ------------------------------------------------------
def generate_plan(company: str):

    if MOCK:
        # simplified mock version
        return f"""
<div class='section-title'>Company Overview</div>
Mock overview for {company}.

<div class='section-title'>Recent News</div>
Mock news data.

<div class='section-title'>Products / Services</div>
Mock product details.

<div class='section-title'>Competitors</div>
Mock competitors list.

<div class='section-title'>Key Opportunities / Signals</div>
Mock opportunities.

<div class='section-title'>Suggested Next Steps</div>
Mock strategic actions.
""".strip()

    prompt = f"""
Generate a professional company account plan for **{company}**.
Return in HTML format ONLY with the following EXACT headings:

<div class='section-title'>Company Overview</div>
<div class='section-title'>Recent News</div>
<div class='section-title'>Products / Services</div>
<div class='section-title'>Competitors</div>
<div class='section-title'>Key Opportunities / Signals</div>
<div class='section-title'>Suggested Next Steps</div>

Rules:
- STRICT: Use ONLY these headings and use EXACT HTML formatting.
- NO asterisks, NO markdown, NO extra sections.
- Provide concise, factual content.
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
    )

    return resp.choices[0].message.content.strip()


# ------------------------------------------------------
# LLM: Regenerate Specific Section
# ------------------------------------------------------
def regenerate_section(section_name: str, company: str):

    if MOCK:
        return f"Mock regenerated content for {section_name}."

    prompt = f"""
Regenerate ONLY the section '{section_name}' for company {company}.
Return ONLY the rewritten content. DO NOT return title or formatting.
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    return resp.choices[0].message.content.strip()


# ------------------------------------------------------
# Main Natural Language Handler
# ------------------------------------------------------
def process_user_message(text: str, current_plan: str = ""):

    text_lower = text.lower().strip()

    # --------------------------------------------------
    # 1️⃣ Detect: “create/generate/make account plan for X”
    # --------------------------------------------------
    match = re.search(r"(?:create|make|build|generate).*account plan.*for (.+)", text_lower)
    if match:
        company = match.group(1).strip().title()
        new_plan = generate_plan(company)
        return (f"Generated account plan for {company}.", new_plan)

    # --------------------------------------------------
    # 2️⃣ Detect simple query: user typing only company name
    # --------------------------------------------------
    if len(text.split()) <= 3 and text.replace(" ", "").isalpha():
        company = text.strip().title()
        new_plan = generate_plan(company)
        return (f"Generated account plan for {company}.", new_plan)

    # --------------------------------------------------
    # 3️⃣ Detect update request for specific section
    # --------------------------------------------------
    for section in SECTION_TITLES:
        sec_lower = section.lower()

        if sec_lower in text_lower and any(
            cmd in text_lower for cmd in ["update", "change", "regenerate", "rewrite"]
        ):
            extracted = split_into_sections(current_plan)

            # try finding company name from overview section
            company_guess = "the company"
            if "Company Overview" in extracted:
                match_company = re.search(r"\b([A-Z][A-Za-z0-9]+)\b", extracted["Company Overview"])
                if match_company:
                    company_guess = match_company.group(1)

            new_section_text = regenerate_section(section, company_guess)

            # merge updated section back into plan
            updated = extracted
            updated[section] = new_section_text

            rebuilt = ""
            for title in SECTION_TITLES:
                rebuilt += f"<div class='section-title'>{title}</div>\n"
                rebuilt += updated.get(title, "") + "\n\n"

            return (f"Updated {section} section.", rebuilt)

    # --------------------------------------------------
    # 4️⃣ Default response
    # --------------------------------------------------
    return ("Okay, I processed your request.", None)
