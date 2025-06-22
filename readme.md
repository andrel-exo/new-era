# 🏠 Idealista Telegram Notifier

This Python script automatically monitors new property listings on Idealista (e.g., T2/T3 homes in Maia, Portugal) and sends notifications to a Telegram chat when new listings are found.

## 📋 Features

- Scrapes Idealista for new listings
- Detects only unnotified (new) ads
- Sends structured messages via Telegram Bot
- Stores notified listings to avoid duplicates

---

## 💻 Requirements

- Operating System: **Windows**
- Python version: **3.10 or higher**
- Internet connection

---

## 🔧 Installation

### 1. Install Python (Windows only)

If you don’t already have Python installed:

- Go to: https://www.python.org/downloads/windows/
- Download the latest **Python 3.x** installer for Windows
- During installation, **check the option** ✅ *“Add Python to PATH”*

### 2. Download or clone the project

Using Git (recommended):

```bash
git clone https://github.com/andrel-exo/new-era.git
cd new-era
```
Or manually download the ZIP and extract it.

### 3. Create the configuration file

Create a file named `config.json` in the project folder with the following content:

```json
{
  "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
  "bot_chat_id": "YOUR_CHAT_ID",
  "communicated_houses_file": "communicated_houses.json",
  "listing_url": "https://www.idealista.pt/comprar-casas/maia/com-preco-max_280000,preco-min_160000,t2,t3/?ordem=atualizado-desc"
}
```

- Replace `YOUR_TELEGRAM_BOT_TOKEN` with your Telegram bot token (from [BotFather](https://t.me/BotFather)).
- Replace `YOUR_CHAT_ID` with the Telegram chat or group ID where you want to receive notifications.

---

### 4. Install Python dependencies

Make sure you are in the project folder, then run:

```bash
pip install -r requirements.txt
```

### 5. Running the script

After installing the dependencies and creating your `config.json`, you can run the script with:

```bash
python main.py
```

The script will check for new listings and send notifications to your Telegram chat.

---

### 6. Stopping the script

To stop the script, simply press `Ctrl + C` in the terminal window.

---
