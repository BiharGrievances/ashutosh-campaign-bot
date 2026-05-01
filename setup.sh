#!/bin/bash
# ============================================
# SETUP.SH — ONE-COMMAND INSTALL
# Run on your HiddenCloud VPS
# ============================================

set -e

echo "🚀 Setting up Ashutosh Campaign Bot on HiddenCloud..."

# 1. Update system
echo "[1/8] Updating system..."
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
echo "[2/8] Installing Python and dependencies..."
sudo apt install -y python3-pip python3-venv git curl

# 3. Create swap
echo "[3/8] Creating swap space..."
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 4. Create project directory
echo "[4/8] Creating project directory..."
mkdir -p ~/ashutosh-campaign
cd ~/ashutosh-campaign

# 5. Setup Python environment
echo "[5/8] Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# 6. Install Python packages
echo "[6/8] Installing Python packages..."
pip install --upgrade pip
pip install requests beautifulsoup4 python-telegram-bot google-generativeai

# 7. Create directories
echo "[7/8] Creating directories..."
mkdir -p logs

# 8. Setup cron
echo "[8/8] Setting up cron job..."
CRON_CMD="0 */6 * * * cd ~/ashutosh-campaign && source venv/bin/activate && python main.py >> logs/cron.log 2>&1"
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo ""
echo "✅ Setup complete!"
echo ""
echo "NEXT STEPS:"
echo "   1. Copy all .py files into ~/ashutosh-campaign/"
echo "   2. Set environment variables:"
echo "      export GEMINI_API_KEY='your-key-here'"
echo "      export TELEGRAM_BOT_TOKEN='your-bot-token'"
echo "      export TELEGRAM_CHAT_ID='your-chat-id'"
echo "   3. Add to ~/.bashrc for persistence"
echo "   4. Run: python main.py (test)"
echo "   5. Cron will auto-run every 6 hours"
echo ""
echo "Get Gemini API key: https://aistudio.google.com/app/apikey"
echo "Get Telegram bot: Message @BotFather on Telegram"
echo ""
