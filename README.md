**🚀 Agentic Company Research Assistant**<br>
An AI-powered interactive agent for intelligent company research & personalized account plan generation.

**📌 Overview**<br>
Agentic Company Research Assistant is an AI-driven platform designed to help users explore companies, gather insights, and generate complete professional account plans through natural dialogue. It leverages advanced agentic reasoning and adaptive behaviors to deliver dynamic, actionable research. The assistant integrates seamlessly with Groq LLaMA, SerpAPI, and Streamlit for real-time intelligence and document generation.

**✨ Features**<br>
**🗣 Natural Interaction**
Converse using everyday language and let the agent handle ambiguous or incomplete queries intelligently.

**📄 Professional Account Plan (HTML)**<br>
Automatically generates clean, structured account plans with company overview, news, competitors, opportunities, and next steps.

**🔄 Section-Level Updates**<br>
Revise any section of the account plan, anytime, without full regeneration.

**🌐 Real-Time Research**<br>
Pull real company details, news, and web insights using SerpAPI, synthesized by an LLM into a unified report.

**🖥 Polished UI**<br>
Streamlit-powered chat and plan panels, including document preview and PDF download features.

**🛠 Future Enhancements**<br>
PPT exports, company comparisons, voice interaction, persistent user memories, and agent-driven multi-step research are on the roadmap.

**🧩 Project Structure**<br>

/project<br>
│── app.py          → Streamlit UI + Chat + PDF Download  
│── agent.py        → LLM core logic + Section updates  
│── search.py       → SerpAPI integrations  
│── utils.py        → Helper utilities  
│── requirements.txt<br>
│── .env.example<br>
│── README.md

**⚙️ Tech Stack**<br>
- Python
- Groq LLaMA 3.3
- Streamlit
- SerpAPI
- ReportLab 

**🧑‍💻 Setup Instructions**<br>
**1. Clone the Repository**<br>
git clone https://github.com/sowjanyakodam/company-research-assistant.git
cd YOUR_REPO

**2. Install Dependencies**<br>
pip install -r requirements.txt

**3. Set Environment Variables**<br>
### Create a .env file<br>
GROQ_API_KEY=your_groq_key<br>
SERPAPI_KEY=your_serpapi_key

**4. Run the App**<br>
streamlit run app.py

**📊 Example Account Plan Structure**<br>
- Company Overview
- Recent News
- Products / Services
- Competitors
- Key Opportunities
- Suggested Next Steps

**🙌 Contributing**<br>
Contributions are welcome! If you'd like to help improve this project, please open an issue or pull request.

**👥 Maintainers**<br>
Sowjanya Kodam<br>
https://github.com/sowjanyakodam
