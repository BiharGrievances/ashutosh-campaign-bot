# ============================================
# TELEGRAM_BOT.PY — DELIVERY ENGINE (IMPROVED)
# Better formatting with news source links
# ============================================

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    """Delivers real content to Dr. Singh's phone"""

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, text, parse_mode='HTML'):
        """Send text message"""
        if not self.token or not self.chat_id:
            print('[TELEGRAM] Warning: Token or Chat ID not set')
            print(f'[TELEGRAM] Would send: {text[:100]}...')
            return True

        url = f'{self.base_url}/sendMessage'
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                print('[TELEGRAM] Message sent successfully')
                return True
            else:
                print(f'[TELEGRAM] Error: {response.status_code} - {response.text}')
                return False
        except Exception as e:
            print(f'[TELEGRAM] Exception: {e}')
            return False

    def format_content(self, approved_items):
        """Format with real news context"""
        message = '🚀 <b>DR. ASHUTOSH SINGH — DAILY CONTENT READY</b>
'
        message += f'📅 {datetime.now().strftime("%d %b %Y, %I:%M %p")}
'
        message += '=' * 40 + '

'

        for item in approved_items:
            message += f'📌 <b>{item["variant_id"]}</b> | {item["format"]}
'
            if item.get('news_link'):
                message += f'🔗 Source: {item["news_link"]}
'
            message += '-' * 30 + '
'
            message += f'<pre>{item["content"]}</pre>

'
            message += '✅ <b>APPROVED — Ready to post</b>
'
            message += '[Copy above → Post on X/Instagram/WhatsApp]

'

        message += '=' * 40 + '
'
        message += f'✅ {len(approved_items)} posts ready
'
        message += '📝 Review, edit if needed, then post manually
'
        message += '⏰ Next batch: 6 hours
'

        return message

    def send_daily_digest(self, approved_items):
        """Send digest with splitting for long messages"""
        if not approved_items:
            self.send_message('⚠️ No new content this run. All caught up!')
            return

        message = self.format_content(approved_items)

        if len(message) > 4000:
            # Send header first
            header = '🚀 <b>DR. ASHUTOSH SINGH — CONTENT READY (Part 1)</b>

'
            self.send_message(header)

            # Send each post separately
            for item in approved_items:
                item_msg = f'📌 <b>{item["variant_id"]}</b> | {item["format"]}
'
                item_msg += f'<pre>{item["content"]}</pre>

'
                item_msg += '✅ Ready to post
'
                self.send_message(item_msg)
        else:
            self.send_message(message)

    def send_test(self):
        """Test message"""
        self.send_message('🧪 <b>Bot Test</b>

If you see this, your AI campaign bot is working!')

if __name__ == '__main__':
    from datetime import datetime
    bot = TelegramBot()
    bot.send_test()
