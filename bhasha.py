# ============================================
# BHASHA.PY — CONTENT FACTORY (IMPROVED)
# Better prompts, real news context, Hindi output
# ============================================

import google.generativeai as genai
from config import VOICE_PROFILE, SOLUTIONS, GEMINI_API_KEY

class BhashaAgent:
    """Improved Content Generation for Dr. Ashutosh Singh"""

    def __init__(self, issues):
        self.issues = issues
        self.content_queue = []

        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate_with_gemini(self, issue, variant_type):
        """Generate content using real news context"""
        if not self.model:
            return self._fallback_generate(issue, variant_type)

        # Get solution framework
        solution = SOLUTIONS.get(issue['policy_angle'], SOLUTIONS['General governance reform'])

        prompt = f"""You are Dr. Ashutosh Singh, a 31-year-old mechanical engineer and PhD researcher from Bihar, India. You are NOT a politician — you are a problem-solver who wants to bring young educated people into policy making.

TODAY'S REAL NEWS FROM BIHAR:
Headline: {issue['headline']}
Source: {issue['source']}
Details: {issue['raw_text']}
Urgency Level: {issue['urgency']}/5

YOUR POLICY SOLUTION FOR THIS ISSUE:
{solution}

CREATE A {variant_type} POST:

Requirements:
1. Reference the EXACT headline and real facts from the news
2. Include specific data/numbers if mentioned
3. Offer YOUR solution (not generic complaints)
4. Mention your "Bihar Youth Policy Fellowship" concept
5. End with a question to engage audience
6. Add relevant hashtags
7. Keep tone: engineer's precision + Bihari emotion
8. Language: Mix of English and Hindi (Hinglish) for urban audience

Output ONLY the post content. No explanations."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f'[BHASHA] Gemini error: {e}')
            return self._fallback_generate(issue, variant_type)

    def _fallback_generate(self, issue, variant_type):
        """Fallback with real news reference"""
        solution = SOLUTIONS.get(issue['policy_angle'], SOLUTIONS['General governance reform'])

        if variant_type == 'X Thread':
            return f"""📊 BIHAR UPDATE: {issue['headline']}

{issue['raw_text'][:100]}...

This is why we need YOUNG MINDS in policy rooms.

My approach:
{solution}

Bihar Youth Policy Fellowship — coming soon.

{VOICE_PROFILE['signature']}"""

        elif variant_type == 'Instagram Caption':
            return f"""🚨 {issue['location'].upper()} ALERT

{issue['headline']}

Reality check: {issue['raw_text'][:80]}...

Solution framework:
{solution}

Engineer hoon, politician nahi. Data se kaam karunga.

#Bihar #YouthInPolicy #DrAshutoshSingh #BiharBadlega

{VOICE_PROFILE['signature']}"""

        else:  # WhatsApp Status
            return f"""🔥 Breaking: {issue['headline'][:50]}...

Iska solution?
{solution[:80]}...

Young educated Biharis — policy table pe aao.

{VOICE_PROFILE['signature']}"""

    def generate_for_issue(self, issue):
        """Generate 3 variants per issue"""
        variants = []
        formats = ['X Thread', 'Instagram Caption', 'WhatsApp Status']

        for i, fmt in enumerate(formats):
            content = self.generate_with_gemini(issue, fmt)

            variants.append({
                'variant_id': f"{issue['id']}_V{i+1}",
                'format': fmt,
                'language': 'Hinglish',
                'content': content,
                'predicted_engagement': 'High' if issue['urgency'] >= 4 else 'Medium',
                'character_count': len(content),
                'parent_issue': issue['id'],
                'policy_angle': issue['policy_angle'],
                'news_link': issue.get('link', '')
            })

        return variants

    def run(self):
        """Full content generation"""
        print(f'[BHASHA] Generating content for {len(self.issues)} real issues...')

        for issue in self.issues:
            variants = self.generate_for_issue(issue)
            self.content_queue.extend(variants)
            print(f'[BHASHA] {issue["id"]}: {len(variants)} variants from real news')

        print(f'[BHASHA] Total: {len(self.content_queue)} content pieces')
        return self.content_queue
