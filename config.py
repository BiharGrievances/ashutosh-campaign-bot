# ============================================
# CONFIG.PY — DR. ASHUTOSH SINGH PROFILE
# ============================================

import os

# --- YOUR PROFILE ---
CANDIDATE_NAME = "Dr. Ashutosh Singh"
CANDIDATE_TITLE = "Mechanical Engineer | PhD Researcher | Policy Catalyst"
WEBSITE = "www.ashutoshforhajipur.com"
X_HANDLE = "reach_ashutosh"

VOICE_PROFILE = {
    "identity": "Dr. Ashutosh Singh, 31, Mechanical Engineer, PhD researcher",
    "style": "Direct, data-backed, emotionally rooted in Bihar, youth-centric",
    "tone": "Hopeful but urgent. Non-politician. Problem-solver.",
    "language": "Hinglish (Hindi + English blend) + pure Hindi for rural",
    "signature": "— Dr. Ashutosh Singh | www.ashutoshforhajipur.com"
}

# --- RULES ---
RULES = {
    "religion_ok": True,
    "must_include_solution": True,
    "no_personal_attacks": True,
    "focus_areas": ["policy", "hygiene", "solutions", "youth"],
    "geography": "entire_bihar",
    "content_types": ["X Thread", "Instagram Caption", "WhatsApp Status"]
}

# --- API KEYS (set as environment variables) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- SCHEDULE ---
RUN_INTERVAL_HOURS = 6

# --- CONTENT SETTINGS ---
MAX_ISSUES_PER_RUN = 4
MAX_VARIANTS_PER_ISSUE = 3

# --- KEYWORDS FOR DETECTION ---
KEYWORDS = {
    "policy": ["policy", "governance", "administration", "reform", "scheme", "yojana", "budget", "bill"],
    "hygiene": ["sanitation", "toilet", "clean", "garbage", "drainage", "pollution", "air quality", "water", "sewage"],
    "solutions": ["development", "infrastructure", "road", "bridge", "hospital", "school", "electricity", "employment", "jobs"],
    "youth": ["student", "college", "university", "exam", "job", "unemployment", "skill", "placement", "fellowship"],
    "religion_ok": ["temple", "mosque", "gurdwara", "church", "festival", "community", "harmony", "religious"]
}

# --- SOLUTION FRAMEWORKS ---
SOLUTIONS = {
    "Environmental policy + tech-driven monitoring": 
        "1) Real-time AQI sensors in all 38 districts 2) AI-powered pollution forecasting 3) Youth-led green brigades",
    "Youth policy + industry-academia bridge": 
        "1) Bihar Youth Policy Fellowship — 500 young engineers/doctors in policy rooms 2) Skill courses co-designed with TCS/Infosys 3) Startup incubators in every district",
    "Urban hygiene policy + smart city infrastructure": 
        "1) Smart drainage with IoT sensors 2) Waste-to-energy plants 3) Tourist area cleanliness as priority, not afterthought",
    "Education policy + outcome-linked training": 
        "1) Training only if industry commits placement 2) Monthly skill audits 3) Youth board to redesign curriculum",
    "General governance reform": 
        "Young educated professionals in every department. Merit over nepotism."
}

# --- NEWS SOURCES ---
NEWS_SOURCES = [
    {"name": "Dainik Jagran Bihar", "url": "https://www.jagran.com/bihar/"},
    {"name": "Prabhat Khabar", "url": "https://www.prabhatkhabar.com/state/bihar"},
    {"name": "Hindustan Bihar", "url": "https://www.livehindustan.com/bihar"},
    {"name": "ANI Bihar", "url": "https://twitter.com/ANI"},
    {"name": "Bihar Government", "url": "https://state.bihar.gov.in/"}
]
