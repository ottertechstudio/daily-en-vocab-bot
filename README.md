# Daily Vocab Bot
### Step-by-Step Setup Guide
> Telegram • OpenRouter AI • GitHub Actions

| 💰 100% Free | ⏰ 24/7 Auto | 📱 No PC Needed | 🤖 AI Powered |
|---|---|---|---|
| No cost at all | 4 times a day | Phone is enough | DeepSeek AI |

---

## Overview

This guide will help you set up an automated Telegram bot that sends English vocabulary lessons every day — 4 times a day — powered by DeepSeek AI. No programming knowledge required.

| Service | Purpose | Website |
|---|---|---|
| Telegram | Receive vocab messages on your phone | telegram.org |
| OpenRouter | Free AI (DeepSeek) to generate vocab | openrouter.ai |
| GitHub | Store code and run automatically | github.com |

---

## Step 1 — Create Your Telegram Bot

1. Open Telegram and search for **"@BotFather"** in the search bar.
2. Tap on BotFather and send: `/newbot`
3. When asked for a name, type anything. Example: `My Vocab Bot`
4. When asked for a username, it must end with `_bot`. Example: `myvocab_bot`
5. BotFather will reply with a Token. Copy and save it.

> **Your Bot Token looks like this:**
> ```
> 7483920174:AAFkdjfslkdjfXXXXXXXXXXXX
> ```

> ⚠️ Never share your Bot Token with anyone. It gives full control of your bot.

---

## Step 2 — Find Your Telegram Chat ID

1. Go to your bot in Telegram and send: `/start`
2. Open your browser and go to this URL (replace TOKEN with your actual token):

```
https://api.telegram.org/botTOKEN/getUpdates
```

3. Find the part that says `"chat":{"id":` — the number after it is your Chat ID.

> **Look for this in the response:**
> ```
> "chat":{"id": 123456789, "first_name": "Your Name" ...}
> ```

4. Save that number. That is your Chat ID.

> ⚠️ If you see an empty result `{}`, make sure you sent `/start` to the bot first, then try the URL again.

---

## Step 3 — Get Your OpenRouter API Key

1. Go to [openrouter.ai](https://openrouter.ai) in your browser.
2. Click **"Sign in"** and log in with your Google account.
3. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
4. Click **"Create Key"** and give it any name.
5. Copy the key that appears and save it immediately.

> **Your OpenRouter Key looks like this:**
> ```
> sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
> ```

> ⚠️ The key is only shown once. Copy it before closing the page!

---

## Step 4 — Create a GitHub Account

1. Go to [github.com](https://github.com) in your browser.
2. Click **"Sign up"** and fill in Email, Password, and Username.
3. Verify your email address.

✅ You are now logged in to GitHub.

---

## Step 5 — Create a Repository (Code Folder)

1. After logging in, click the **"+"** button in the top right corner.
2. Click **"New repository"**.
3. Fill in the following:

| Field | What to Enter |
|---|---|
| Repository name | `vocab-bot` |
| Visibility | ✅ Select **Private** |
| Add a README file | ✅ Check this box |

4. Click **"Create repository"**.

---

## Step 6 — Save Your Secret Keys in GitHub

This stores your tokens securely so GitHub can use them without exposing them.

1. Inside your `vocab-bot` repository, click the **"Settings"** tab at the top.
2. In the left sidebar click **"Secrets and variables"** → then **"Actions"**.
3. Click **"New repository secret"** and add each of the 3 secrets below one at a time:

| Name (type exactly) | Secret Value |
|---|---|
| `TELEGRAM_TOKEN` | Your Bot Token from Step 1 |
| `CHAT_ID` | Your Chat ID number from Step 2 |
| `OPENROUTER_API_KEY` | Your OpenRouter key from Step 3 |

> ⚠️ Secret names cannot have spaces. Use underscore `_` only. e.g. `TELEGRAM_TOKEN` not `TELEGRAM TOKEN`

---

## Step 7 — Create the Bot Code File (bot.py)

1. In your `vocab-bot` repository, click **"Add file"** → **"Create new file"**.
2. In the filename box, type: `bot.py`
3. Copy ALL the code below and paste into the large text area:

```python
import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

def get_vocab():
    prompt = """
Create a daily English vocabulary lesson for learners.
Format exactly like this:

Word: [english word]
Meaning: [clear simple English meaning]
Spoken English: [how to use in spoken English + simple English explanation]
Written English: [how to use in written English + simple English explanation]
Examples:
1. [example sentence 1]
2. [example sentence 2]
3. [example sentence 3]
Watch Out: [common mistakes and tips in simple English]

Keep it beginner-friendly. Use simple and clear English only.
Do NOT use any other language. Everything must be in English only.
    """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    data = response.json()
    if "choices" not in data:
        raise Exception(f"API Error: {data}")
    return data["choices"][0]["message"]["content"]

def send_vocab():
    vocab = get_vocab()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": vocab
    })
    print("Vocab sent!")

send_vocab()
```

4. Scroll down and click **"Commit changes"** → **"Commit changes"** again.

✅ bot.py file created!

---

## Step 8 — Create the Schedule File (vocab.yml)

1. Click **"Add file"** → **"Create new file"** again.
2. In the filename box, type EXACTLY:

```
.github/workflows/vocab.yml
```

> ⚠️ Type it exactly as shown. The dot at the start is important. GitHub will auto-create the folders.

3. Copy ALL the code below and paste into the text area:

```yaml
name: Send Vocab

on:
  schedule:
    - cron: '0 0 * * *'    # 12:00 AM UTC
    - cron: '0 6 * * *'    # 6:00 AM UTC
    - cron: '0 12 * * *'   # 12:00 PM UTC
    - cron: '0 18 * * *'   # 6:00 PM UTC
  workflow_dispatch:

jobs:
  send-vocab:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install requests
      - run: python bot.py
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```

4. Click **"Commit changes"** → **"Commit changes"** again.

✅ Schedule file created!

---

## Step 9 — Test Your Bot

1. In your repository, click the **"Actions"** tab at the top.
2. On the left side, click **"Send Vocab"**.
3. Click the **"Run workflow"** button on the right.
4. Click the green **"Run workflow"** button in the popup.
5. Wait 1–2 minutes and watch the status icon.
6. When it shows a green checkmark — check your Telegram!

| Status Icon | Meaning |
|---|---|
| 🟡 Yellow circle | Still running — please wait |
| ✅ Green checkmark | Success! Check Telegram for your vocab message |
| ❌ Red X | Something failed — copy the error and ask for help |

---

## 🎉 Setup Complete!

Your Daily Vocab Bot is now fully set up. Here is a summary of everything you built:

- ✅ Step 1 — Telegram Bot created
- ✅ Step 2 — Chat ID found
- ✅ Step 3 — OpenRouter API Key obtained
- ✅ Step 4 — GitHub Account created
- ✅ Step 5 — Repository (vocab-bot) created
- ✅ Step 6 — Secret Keys saved securely
- ✅ Step 7 — bot.py code file added
- ✅ Step 8 — vocab.yml schedule file added
- ✅ Step 9 — Bot tested successfully

---

> 🚀 **Your bot will automatically send English vocab 4 times every day to your Telegram — forever!**
