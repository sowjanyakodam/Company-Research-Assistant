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
# User Context Detection
# ------------------------------------------------------
USER_CONTEXTS = {
    "sales": ["sales", "account executive", "business development", "selling", "sales rep", "account manager", "bdm"],
    "student": ["student", "placement", "interview", "campus", "college", "intern", "graduate", "university"],
    "investor": ["investor", "investment", "funding", "portfolio", "venture", "equity"],
    "partner": ["partner", "vendor", "integration", "collaborate", "partnership"],
    "competitor": ["competitor", "competitive", "versus", "vs", "competing"],
    "recruiter": ["recruiter", "recruiting", "hiring", "hr", "talent"],
}


def detect_user_context(text: str):
    """Detect user role/context from their message"""
    text_lower = text.lower()
    
    for context, keywords in USER_CONTEXTS.items():
        if any(kw in text_lower for kw in keywords):
            return context
    
    return "general"


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
# Utility: Convert Markdown to HTML
# ------------------------------------------------------
def markdown_to_html(text: str) -> str:
    """Convert markdown formatting to HTML"""
    # Convert **bold** to <strong>
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to <em>
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Convert bullet points (- item) to proper list items
    text = re.sub(r'^-\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Convert numbered lists (1. item) to proper list items
    text = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Convert line breaks to <br>
    text = text.replace('\n\n', '<br><br>')
    
    return text


# ------------------------------------------------------
# LLM: Generate Full Account Plan
# ------------------------------------------------------
def generate_plan(company: str, user_context: str = "general"):

    if MOCK:
        return f"""
<div class='section-title'>Company Overview</div>
Mock overview for {company} ({user_context} focused).

<div class='section-title'>Recent News</div>
Mock news data.

<div class='section-title'>Products / Services</div>
Mock product details.

<div class='section-title'>Competitors</div>
Mock competitors list.

<div class='section-title'>Key Opportunities / Signals</div>
Mock opportunities for {user_context}.

<div class='section-title'>Suggested Next Steps</div>
Mock strategic actions for {user_context}.
""".strip()

    # Context-specific instructions
    context_instructions = {
        "sales": "Focus on: pain points, decision makers, buying signals, competitive advantages, pricing intel, sales opportunities",
        "student": "Focus on: company culture, tech stack used, hiring process, growth opportunities, employee reviews, skills needed",
        "investor": "Focus on: financials, market position, growth metrics, risks, competitive moat, revenue streams",
        "partner": "Focus on: integration possibilities, partnership opportunities, procurement process, collaboration areas",
        "competitor": "Focus on: competitive analysis, market positioning, strengths/weaknesses, differentiation",
        "recruiter": "Focus on: company culture, team structure, hiring patterns, employee retention, benefits",
        "general": "Provide a comprehensive overview suitable for general business intelligence"
    }

    prompt = f"""
Generate a professional company account plan for **{company}**.

USER CONTEXT: {user_context}
FOCUS AREAS: {context_instructions.get(user_context, context_instructions["general"])}

Return in HTML format ONLY with the following EXACT headings:

<div class='section-title'>Company Overview</div>
<div class='section-title'>Recent News</div>
<div class='section-title'>Products / Services</div>
<div class='section-title'>Competitors</div>
<div class='section-title'>Key Opportunities / Signals</div>
<div class='section-title'>Suggested Next Steps</div>

Rules:
- STRICT: Use ONLY these headings and use EXACT HTML formatting.
- NO asterisks for bold, use <strong> tags instead
- NO markdown formatting, use HTML tags only
- Use <ul> and <li> for bullet points
- Provide concise, factual content
- Tailor the content based on the USER CONTEXT and FOCUS AREAS provided above
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1400,
    )

    content = resp.choices[0].message.content.strip()
    content = markdown_to_html(content)
    
    return content


# ------------------------------------------------------
# LLM: Regenerate Specific Section
# ------------------------------------------------------
def regenerate_section(section_name: str, company: str, user_context: str = "general"):

    if MOCK:
        return f"Mock regenerated content for {section_name} ({user_context} focused)."

    context_note = f" Keep in mind the user is a {user_context}." if user_context != "general" else ""

    prompt = f"""
Regenerate ONLY the section '{section_name}' for company {company}.
{context_note}
Return ONLY the rewritten content in HTML format. 
DO NOT return title or section heading.
Use <strong> tags for emphasis, NOT asterisks.
Use <ul> and <li> for lists.
"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    content = resp.choices[0].message.content.strip()
    content = markdown_to_html(content)
    
    return content


# ------------------------------------------------------
# LLM: Answer Follow-up Questions
# ------------------------------------------------------
def answer_followup_question(question: str, current_plan: str, user_context: str):
    """Answer specific questions about the generated plan"""
    
    if MOCK:
        return f"Mock answer to your question (from {user_context} perspective)."
    
    sections = split_into_sections(current_plan)
    context_text = "\n".join([f"{k}: {v}" for k, v in sections.items()])
    
    prompt = f"""
Based on this account plan:
{context_text}

User context: {user_context}
Question: {question}

Provide a focused, actionable answer based on the account plan data.
If asking about opportunities, tech stack, or specific insights, extract from relevant sections.
Tailor your response to be relevant for someone in the {user_context} role.
"""
    
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    return resp.choices[0].message.content.strip()


# ------------------------------------------------------
# LLM: Provide Context-Specific Summary
# ------------------------------------------------------
def provide_context_specific_summary(current_plan: str, new_context: str):
    """
    Provide a context-specific summary without full regeneration.
    More efficient for quick context switches.
    """
    
    if MOCK:
        return f"Mock {new_context}-specific insights from the plan."
    
    sections = split_into_sections(current_plan)
    context_text = "\n".join([f"{k}: {v}" for k, v in sections.items()])
    
    context_focus = {
        "sales": "Highlight: competitive advantages, decision makers, pain points, pricing strategies, and sales opportunities",
        "student": "Highlight: tech stack, company culture, hiring process, career growth, and interview preparation insights",
        "investor": "Highlight: financial performance, market position, growth potential, and investment risks",
        "partner": "Highlight: partnership opportunities, integration possibilities, and collaboration potential",
        "competitor": "Highlight: competitive positioning, market share, strengths and weaknesses",
        "recruiter": "Highlight: hiring patterns, company culture, team structure, employee benefits",
    }
    
    prompt = f"""
Based on this account plan:
{context_text}

The user is a {new_context}. 
{context_focus.get(new_context, "Provide relevant insights")}

Provide a brief, focused summary (3-4 key points) explaining how this information is specifically relevant and actionable for them.
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
def process_user_message(text: str, current_plan: str = "", user_context: str = None):
    """
    Process user message with dynamic context switching support.
    
    Args:
        text: User's input message
        current_plan: Existing account plan (if any)
        user_context: Previously detected user context (None = not yet determined)
    
    Returns:
        (response_message, updated_plan, user_context)
    """
    
    text_lower = text.lower().strip()
    
    # --------------------------------------------------
    # 1️⃣ Pattern: User reveals context AFTER plan is generated
    # --------------------------------------------------
    context_reveal_match = re.search(
        r"(?:how|what).*(?:useful|relevant|helpful|mean).*(?:for me|to me).*(?:as a|as an|i'm|i am)\s+(?:a\s+)?(\w+)",
        text_lower
    )
    
    if not context_reveal_match:
        context_reveal_match = re.search(
            r"(?:i'm|i am|as a|as an)\s+(?:a\s+)?(\w+).*(?:what|how|tell me|explain)",
            text_lower
        )
    
    if context_reveal_match and current_plan:
        role_hint = context_reveal_match.group(1)
        new_context = detect_user_context(role_hint)
        
        if new_context != "general" and new_context != user_context:
            extracted = split_into_sections(current_plan)
            company_name = "this company"
            if "Company Overview" in extracted:
                match_company = re.search(r"\b([A-Z][A-Za-z0-9]+)\b", extracted["Company Overview"])
                if match_company:
                    company_name = match_company.group(1)
            
            new_plan = generate_plan(company_name, new_context)
            
            return (
                f"Great question! I've regenerated the account plan for {company_name} with a {new_context} focus. This should now be more relevant to your needs.",
                new_plan,
                new_context
            )
    
    # --------------------------------------------------
    # 2️⃣ Pattern: "As a [role], what opportunities..."
    # --------------------------------------------------
    role_question_match = re.search(
        r"(?:as a|as an|i'm|i am)\s+(?:a\s+)?(\w+).*(?:what|how|which|tell|show)",
        text_lower
    )
    
    if role_question_match and current_plan:
        role_hint = role_question_match.group(1)
        new_context = detect_user_context(role_hint)
        
        if new_context != "general":
            answer = answer_followup_question(text, current_plan, new_context)
            return (answer, None, new_context)
    
    # --------------------------------------------------
    # 3️⃣ Detect context ONLY if not already set
    # --------------------------------------------------
    if user_context is None:
        detected_context = detect_user_context(text)
        if detected_context != "general":
            user_context = detected_context
    
    # --------------------------------------------------
    # 4️⃣ Pattern: Explicit role + company in same message
    # --------------------------------------------------
    match = re.search(
        r"(?:i'm|i am|as a)\s+(?:a\s+)?(\w+).*?(?:create|generate|make|build).*?(?:plan|research).*?(?:for|about|of)\s+(.+)",
        text_lower
    )
    if match:
        role_hint = match.group(1)
        company = match.group(2).strip().title()
        detected_context = detect_user_context(role_hint)
        new_plan = generate_plan(company, detected_context)
        
        context_label = f" ({detected_context}-focused)" if detected_context != "general" else ""
        return (
            f"Generated account plan{context_label} for {company}.", 
            new_plan, 
            detected_context
        )
    
    # --------------------------------------------------
    # 5️⃣ Pattern: Standard "create account plan for X"
    # --------------------------------------------------
    match = re.search(r"(?:account\s+)?plan\s+(?:for|of|about|on)\s+(.+)", text_lower)
    if match:
        company = match.group(1).strip().title()
        context_to_use = user_context if user_context else "general"
        new_plan = generate_plan(company, context_to_use)
        
        context_label = f" ({context_to_use}-focused)" if context_to_use != "general" else ""
        return (
            f"Generated account plan{context_label} for {company}.", 
            new_plan, 
            context_to_use
        )
    
    # --------------------------------------------------
    # 6️⃣ Pattern: Simple company name
    # --------------------------------------------------
    if len(text.split()) <= 3 and text.replace(" ", "").replace("-", "").isalpha():
        company = text.strip().title()
        context_to_use = user_context if user_context else "general"
        new_plan = generate_plan(company, context_to_use)
        
        context_label = f" ({context_to_use}-focused)" if context_to_use != "general" else ""
        return (
            f"Generated account plan{context_label} for {company}.", 
            new_plan, 
            context_to_use
        )
    
    # --------------------------------------------------
    # 7️⃣ Pattern: User just stating their role
    # --------------------------------------------------
    role_match = re.search(r"(?:i'm|i am|as a)\s+(?:a\s+)?(\w+)", text_lower)
    if role_match and not any(word in text_lower for word in ["create", "generate", "make"]):
        role_hint = role_match.group(1)
        detected_context = detect_user_context(role_hint)
        
        if detected_context != "general":
            if current_plan:
                return (
                    f"Understood! You're focused on {detected_context}. Would you like me to regenerate the account plan with a {detected_context} focus?",
                    None,
                    detected_context
                )
            else:
                return (
                    f"Got it! I'll tailor the account plan for {detected_context} needs. Which company would you like to research?",
                    None,
                    detected_context
                )
    
    # --------------------------------------------------
    # 8️⃣ Pattern: Update specific section
    # --------------------------------------------------
    for section in SECTION_TITLES:
        sec_lower = section.lower()
        
        if sec_lower in text_lower and any(
            cmd in text_lower for cmd in ["update", "change", "regenerate", "rewrite"]
        ):
            extracted = split_into_sections(current_plan)
            
            company_guess = "the company"
            if "Company Overview" in extracted:
                match_company = re.search(r"\b([A-Z][A-Za-z0-9]+)\b", extracted["Company Overview"])
                if match_company:
                    company_guess = match_company.group(1)
            
            context_to_use = user_context if user_context else "general"
            new_section_text = regenerate_section(section, company_guess, context_to_use)
            
            updated = extracted
            updated[section] = new_section_text
            
            rebuilt = ""
            for title in SECTION_TITLES:
                rebuilt += f"<div class='section-title'>{title}</div>\n"
                rebuilt += updated.get(title, "") + "\n\n"
            
            return (f"Updated {section} section.", rebuilt, user_context)
    
    # --------------------------------------------------
    # 9️⃣ Pattern: Follow-up questions
    # --------------------------------------------------
    if current_plan and any(q in text_lower for q in ["what", "how", "which", "tell me", "show me", "opportunities", "useful", "relevant", "technologies", "tech stack"]):
        context_to_use = user_context if user_context else "general"
        answer = answer_followup_question(text, current_plan, context_to_use)
        return (answer, None, user_context)
    
    # --------------------------------------------------
    # 🔟 Default response
    # --------------------------------------------------
    return ("I can help you research companies. Just tell me which company you'd like to analyze!", None, user_context)