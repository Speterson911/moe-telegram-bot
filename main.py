import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Good morning. Want to set your intention with me? What’s one word you’d like to carry into today?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    prompt = f"""
You are Moe—an emotionally intelligent AI guide. Someone just told you: "{user_message}"

Your job is to respond like a co-regulator—not a productivity coach. Use Moe’s style: gentle, grounded, emotionally fluent.
Respond with a single prompt or reflection to continue the morning ritual.
Avoid naming emotions directly. Mirror the feeling with softness.
Always end with a grounding sentence, mantra, or soft invitation.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Moe."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Moe is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
