# ============================================
# BHASHA.PY — CONTENT FACTORY
# Gemini-powered content generation
# ============================================

import google.generativeai as genai
from config import VOICE_PROFILE, SOLUTIONS, GEMINI_API_KEY

class BhashaAgent:
    """Autonomous Content Generation for Dr. Ashutosh Singh"""

    def __init__(self, issues):
        self.issues = issues
        self.content_queue = []

        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate_with_gemini(self, issue, variant_type):
        """Use Gemini API for high-quality generation"""
        if not self.model:
            return self._fallback_generate(issue, variant_type)

        prompt = f"""
You are writing political campaign content for Dr. Ashutosh Singh, a 31-year-old mechanical engineer and PhD researcher from Bihar, India.

CANDIDATE PROFILE:
- Identity: Dr. Ashutosh Singh, Mechanical Engineer, PhD researcher
- Style: Direct, data-backed, emotionally rooted in Bihar, youth-centric
- Tone: Hopeful but urgent. Non-politician. Problem-solver.
- Language: Hinglish (Hindi + English blend) for urban, pure Hindi for rural
- Religion: Acceptable to reference religious harmony and community
- Signature: — Dr. Ashutosh Singh | www.ashutoshforhajipur.com

ISSUE TO WRITE ABOUT:
Headline: {issue['headline']}
Location: {issue['location']}
Details: {issue['raw_text']}
Policy Angle: {issue['policy_angle']}
Urgency: {issue['urgency']}/5

CONTENT TYPE: {variant_type}
- X Thread: Punchy, data-heavy, thread format
- Instagram Caption: Visual-friendly, emotional, hashtags
- WhatsApp Status: Short, shareable, Hinglish

RULES:
1. Must include specific policy solutions (not just complaints)
2. Can reference religious harmony if relevant
3. Emphasize youth participation in policy making
4. Use "I am not a politician, I am an engineer" angle
5. End with call to action

Generate ONLY the content text. No explanations.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[BHASHA] Gemini error: {e}")
            return self._fallback_generate(issue, variant_type)

    def _fallback_generate(self, issue, variant_type):
        """Fallback template-based generation"""
        solution = SOLUTIONS.get(issue["policy_angle"], SOLUTIONS["General governance reform"])

        if variant_type == "X Thread":
            return f"""📊 BIHAR REALITY CHECK

{issue['headline']}

{issue['raw_text'][:80]}...

This is NOT a political issue. This is a POLICY FAILURE.

My solution framework:
{solution}

Young educated Biharis must sit in policy rooms. Not as spectators. As architects.

{VOICE_PROFILE['signature']}"""

        elif variant_type == "Instagram Caption":
            return f"""🧹 {issue['location'].upper()} NEEDS ACTION

{issue['headline']}

Problem: {issue['raw_text'][:60]}...

Solution: {solution}

I am not a politician. I am an engineer who came back from Italy & France to fix this.

Join the movement. Link in bio.

{VOICE_PROFILE['signature']}"""

        else:
            return f"""🚨 Bihar Alert: {issue['headline'][:40]}...

Problem samajh me aaya? Ab solution bhi suno:
{solution[:100]}...

Young minds chahiye policy me. Aap aaoge?

{VOICE_PROFILE['signature']}"""

    def generate_for_issue(self, issue):
        """Generate 3 variants per issue"""
        variants = []
        formats = ["X Thread", "Instagram Caption", "WhatsApp Status"]

        for i, fmt in enumerate(formats):
            content = self.generate_with_gemini(issue, fmt)

            variants.append({
                "variant_id": f"{issue['id']}_V{i+1}",
                "format": fmt,
                "language": "English",
                "content": content,
                "predicted_engagement": "High" if issue["urgency"] >= 4 else "Medium",
                "character_count": len(content),
                "parent_issue": issue["id"],
                "policy_angle": issue["policy_angle"]
            })

        return variants

    def run(self):
        """Full content generation cycle"""
        print(f"[BHASHA] Generating content for {len(self.issues)} issues...")

        for issue in self.issues:
            variants = self.generate_for_issue(issue)
            self.content_queue.extend(variants)
            print(f"[BHASHA] {issue['id']}: {len(variants)} variants generated")

        print(f"[BHASHA] Total: {len(self.content_queue)} content pieces")
        return self.content_queue
