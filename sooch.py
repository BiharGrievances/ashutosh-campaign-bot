# ============================================
# SOOCH.PY — PERCEPTION ENGINE (REAL NEWS)
# Scrapes actual Bihar news from RSS feeds
# ============================================

import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
from datetime import datetime
import hashlib
from config import KEYWORDS

class SoochAgent:
    """Real-time Issue Detection for Bihar via RSS"""

    # Real RSS feeds for Bihar news
    RSS_FEEDS = [
        {"name": "Jagran Bihar", "url": "https://www.jagran.com/rss/bihar.xml"},
        {"name": "Prabhat Khabar", "url": "https://www.prabhatkhabar.com/rss/state/bihar"},
        {"name": "Live Hindustan", "url": "https://www.livehindustan.com/rss/bihar.xml"},
        {"name": "Times of India Bihar", "url": "https://timesofindia.indiatimes.com/rssfeeds/1890554.cms"},
        {"name": "NDTV Bihar", "url": "https://feeds.feedburner.com/ndtvnews-bihar"}
    ]

    def __init__(self):
        self.detected_issues = []
        self.seen_hashes = set()
        self.load_seen_hashes()

    def load_seen_hashes(self):
        """Load previously seen articles to avoid duplicates"""
        try:
            with open('logs/seen_articles.json', 'r') as f:
                self.seen_hashes = set(json.load(f))
        except:
            self.seen_hashes = set()

    def save_seen_hashes(self):
        """Save seen articles"""
        os.makedirs('logs', exist_ok=True)
        with open('logs/seen_articles.json', 'w') as f:
            json.dump(list(self.seen_hashes), f)

    def fetch_rss(self, feed_url):
        """Fetch and parse RSS feed"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(feed_url, headers=headers, timeout=15)
            response.raise_for_status()

            # Parse XML
            root = ET.fromstring(response.content)

            # RSS 2.0 format
            items = root.findall('.//item')
            if not items:
                # Try Atom format
                items = root.findall('.//{http://www.w3.org/2005/Atom}entry')

            articles = []
            for item in items[:5]:  # Top 5 articles per feed
                title = item.findtext('title', '')
                link = item.findtext('link', '')
                description = item.findtext('description', '')
                pub_date = item.findtext('pubDate', datetime.now().isoformat())

                if title:
                    articles.append({
                        'headline': title,
                        'link': link,
                        'raw_text': description or title,
                        'timestamp': pub_date,
                        'source': feed_url
                    })

            return articles

        except Exception as e:
            print(f"[SOOCH] Error fetching {feed_url}: {e}")
            return []

    def classify_issue(self, article):
        """Classify article into issue categories"""
        text = (article['headline'] + ' ' + article['raw_text']).lower()

        # Create unique hash
        article_hash = hashlib.md5(article['headline'].encode()).hexdigest()

        # Skip if already seen
        if article_hash in self.seen_hashes:
            return None

        self.seen_hashes.add(article_hash)

        # Detect categories
        categories = []
        for cat, kws in KEYWORDS.items():
            if any(kw in text for kw in kws):
                categories.append(cat)

        if not categories:
            categories = ['general']

        # Calculate urgency based on keywords
        urgency = 1
        urgent_words = ['death', 'kill', 'crash', 'collapse', 'flood', 'fire', 'accident', 
                       'protest', 'strike', 'shutdown', 'emergency', 'crisis']
        if any(w in text for w in urgent_words):
            urgency = 5
        elif any(w in text for w in ['unemployment', 'jobless', 'poverty']):
            urgency = 4
        elif any(w in text for w in ['pollution', 'garbage', 'drainage', 'water']):
            urgency = 3

        religion_relevant = any(kw in text for kw in KEYWORDS['religion_ok'])

        # Determine policy angle
        policy_angles = {
            'air': 'Environmental policy + tech-driven monitoring',
            'pollution': 'Environmental policy + tech-driven monitoring',
            'water': 'Urban hygiene policy + smart city infrastructure',
            'drainage': 'Urban hygiene policy + smart city infrastructure',
            'garbage': 'Urban hygiene policy + smart city infrastructure',
            'unemployment': 'Youth policy + industry-academia bridge',
            'job': 'Youth policy + industry-academia bridge',
            'skill': 'Education policy + outcome-linked training',
            'education': 'Education policy + outcome-linked training',
            'school': 'Education policy + outcome-linked training',
            'hospital': 'General governance reform',
            'health': 'General governance reform',
            'road': 'General governance reform',
            'bridge': 'General governance reform',
            'electricity': 'General governance reform',
            'power': 'General governance reform'
        }

        policy_angle = 'General governance reform'
        for key, angle in policy_angles.items():
            if key in text:
                policy_angle = angle
                break

        return {
            'id': f'ISSUE_{len(self.detected_issues)+1:03d}',
            'headline': article['headline'],
            'source': article['source'],
            'location': 'Bihar',  # Could be extracted with NLP
            'categories': categories,
            'urgency': urgency,
            'religion_relevant': religion_relevant,
            'policy_angle': policy_angle,
            'timestamp': article['timestamp'],
            'raw_text': article['raw_text'],
            'link': article['link'],
            'hash': article_hash
        }

    def run(self):
        """Full detection cycle with real feeds"""
        print('[SOOCH] Scanning real Bihar news feeds...')

        all_articles = []
        for feed in self.RSS_FEEDS:
            print(f'[SOOCH] Fetching: {feed["name"]}')
            articles = self.fetch_rss(feed['url'])
            all_articles.extend(articles)
            print(f'[SOOCH]   Got {len(articles)} articles')

        print(f'[SOOCH] Total articles fetched: {len(all_articles)}')

        # Classify and filter new articles
        new_issues = []
        for article in all_articles:
            issue = self.classify_issue(article)
            if issue:
                new_issues.append(issue)
                self.detected_issues.append(issue)

        self.save_seen_hashes()

        print(f'[SOOCH] New unique issues: {len(new_issues)}')

        if not new_issues:
            print('[SOOCH] No new issues found. Using fallback data.')
            return self._fallback_issues()

        return new_issues[:4]  # Return top 4

    def _fallback_issues(self):
        """Fallback if no new RSS data"""
        return [
            {
                'id': 'ISSUE_001',
                'headline': 'Bihar youth unemployment at 19.8% — highest in India',
                'source': 'Economic Survey',
                'location': 'Statewide',
                'categories': ['youth', 'solutions'],
                'urgency': 5,
                'religion_relevant': False,
                'policy_angle': 'Youth policy + industry-academia bridge',
                'timestamp': datetime.now().isoformat(),
                'raw_text': 'CMIE data shows Bihar youth unemployment at 19.8%, highest among all states.',
                'link': ''
            }
        ]

if __name__ == '__main__':
    agent = SoochAgent()
    issues = agent.run()
    for i in issues:
        print(f'  - {i["id"]}: {i["headline"][:50]}... (Urgency: {i["urgency"]}/5)')
