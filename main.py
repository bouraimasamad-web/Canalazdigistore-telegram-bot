import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TELEGRAM_TOKEN, GROQ_API_KEY, CHANNEL_USERNAME, ADMIN_ID

client = Groq(api_key=GROQ_API_KEY)
scheduler = AsyncIOScheduler()

with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    user_message = update.message.text

    prompt = f"""
Tu es l'assistant officiel du canal AZ Digistore.

BASE DE CONNAISSANCES
{knowledge}

Ton rôle est d'aider l'administrateur à :

- rédiger des publications
- créer des annonces
- créer des promotions
- générer du contenu marketing
- préparer des campagnes de contenu

INSTRUCTION ADMINISTRATEUR
{user_message}

Si l'instruction demande une publication immédiate,
génère uniquement le texte final prêt à être publié
dans le canal Telegram.

Le message doit être clair, impactant et adapté à Telegram.
"""

    response = client
