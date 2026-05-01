# ============================================
# TELEGRAM_BOT.PY — DELIVERY ENGINE
# Sends approved content to your phone
# ============================================

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramBot:
    """Delivers content to Dr. Singh's phone"""

    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text, parse_mode="HTML"):
        """Send text message to Telegram"""
        if not self.token or not self.chat_id:
            print("[TELEGRAM] Warning: Token or Chat ID not set")
            print(f"[TELEGRAM] Would send: {text[:100]}...")
            return True

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                print("[TELEGRAM] Message sent successfully")
                return True
            else:
                print(f"[TELEGRAM] Error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"[TELEGRAM] Exception: {e}")
            return False

    def format_content(self, approved_items):
        """Format approved content for Telegram delivery"""
        message = "🚀 <b>DR. ASHUTOSH SINGH — DAILY CONTENT READY</b>\n"
        message += "=" * 40 + "\n\n"

        for item in approved_items:
            message += f"📌 <b>{item['variant_id']}</b> | {item['format']}\n"
            message += "-" * 30 + "\n"
            message += f"<pre>{item['content']}</pre>\n\n"
            message += "[COPY ABOVE → POST ON X/INSTAGRAM/WHATSAPP]\n\n"

        message += "=" * 40 + "\n"
        message += f"✅ {len(approved_items)} posts ready for manual posting\n"
        message += "📝 Review, edit if needed, then post manually\n"

        return message

    def send_daily_digest(self, approved_items):
        """Send daily content digest"""
        if not approved_items:
            print("[TELEGRAM] No approved items to send")
            return

        message = self.format_content(approved_items)

        if len(message) > 4000:
            chunks = [approved_items[i:i+2] for i in range(0, len(approved_items), 2)]
            for i, chunk in enumerate(chunks):
                header = f"🚀 <b>PART {i+1}/{len(chunks)}</b>\n" + "=" * 30 + "\n\n"
                chunk_msg = header + self.format_content(chunk).split("=" * 40 + "\n\n")[1]
                self.send_message(chunk_msg)
        else:
            self.send_message(message)

    def send_test(self):
        """Send test message"""
        self.send_message("🧪 <b>Test message from Ashutosh Campaign Bot</b>\n\nIf you see this, your bot is working!")
