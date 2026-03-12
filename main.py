import asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from groq import Groq

from config import *
from scheduler import start_scheduler
from campaign_manager import schedule_post

client = Groq(api_key=GROQ_API_KEY)

with open("knowledge_base.txt","r",encoding="utf-8") as f:
    knowledge=f.read()

async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id!=ADMIN_ID:
        return

    msg=update.message.text

    prompt=f"""
Tu es l'assistant marketing de AZ Digistore.

Connaissances:
{knowledge}

L'administrateur peut demander :

- publier un message
- programmer un message
- créer une campagne marketing
- générer contenu

Message admin:
{msg}

Réponds uniquement avec le contenu à publier.
"""

    res=client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role":"user","content":prompt}]
    )

    text=res.choices[0].message.content

    await context.bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

async def main():

    start_scheduler()

    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT,handle))

    await app.run_polling()

asyncio.run(main())
