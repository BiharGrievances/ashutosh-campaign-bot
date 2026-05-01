# ============================================
# MAIN.PY — ORCHESTRATOR
# Runs all agents in sequence
# ============================================

import os
import sys
from datetime import datetime

from config import MAX_ISSUES_PER_RUN
from sooch import SoochAgent
from bhasha import BhashaAgent
from neeti import NeetiAgent
from telegram_bot import TelegramBot
from gyaan import GyaanAgent

def main():
    """Main execution pipeline"""
    print("=" * 70)
    print(f"🚀 DR. ASHUTOSH SINGH — AI CAMPAIGN BOT")
    print(f"   Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Step 1: Detect issues
    print("\n[1/5] Running SOOCH (Issue Detection)...")
    sooch = SoochAgent()
    issues = sooch.run()

    if not issues:
        print("[MAIN] No issues detected. Exiting.")
        return

    issues = issues[:MAX_ISSUES_PER_RUN]
    print(f"[MAIN] Processing top {len(issues)} issues")

    # Step 2: Generate content
    print("\n[2/5] Running BHASHA (Content Generation)...")
    bhasha = BhashaAgent(issues)
    content = bhasha.run()

    if not content:
        print("[MAIN] No content generated. Exiting.")
        return

    # Step 3: Evaluate and approve
    print("\n[3/5] Running NEETI (Approval Gate)...")
    neeti = NeetiAgent(content)
    approved, flagged = neeti.run()

    # Step 4: Deliver to Telegram
    print("\n[4/5] Running TELEGRAM (Delivery)...")
    bot = TelegramBot()
    if approved:
        bot.send_daily_digest(approved)
    else:
        bot.send_message("⚠️ No content passed approval this run. Check flagged items.")

    # Step 5: Log and learn
    print("\n[5/5] Running GYAAN (Learning)...")
    gyaan = GyaanAgent(approved, flagged)
    report = gyaan.run()

    # Summary
    print("\n" + "=" * 70)
    print("✅ RUN COMPLETE")
    print("=" * 70)
    print(f"   Issues detected: {len(issues)}")
    print(f"   Content generated: {len(content)}")
    print(f"   Approved: {len(approved)}")
    print(f"   Flagged: {len(flagged)}")
    print(f"   Next run: {MAX_ISSUES_PER_RUN} hours")
    print("=" * 70)

if __name__ == "__main__":
    main()
