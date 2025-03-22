from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database import save_user_interests, find_matching_users
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key="sk-13DJKXp6QBphm8MaRbUwOiwRmx9E2qwW6lf9dMP30eEeqyXJ",
    base_url="https://api.deerapi.com/v1"
)

async def start(update, context):
    """Handle the /start command"""
    await update.message.reply_text("Welcome! Please tell me your favorite game genres, e.g., 'I like Genshin Impact and Honor of Kings'.")

async def handle_message(update, context):
    """Process user messages"""
    user_id = update.message.from_user.id
    user_input = update.message.text

    # Get username
    user = update.message.from_user
    username = user.username or user.first_name or "Anonymous User"

    # Call ChatGPT to extract interest keywords
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an interest extraction assistant. Extract game-related interest keywords from user messages, separated by commas."},
                {"role": "user", "content": f"Extract interest keywords: {user_input}"}
            ]
        )
        raw_interests = response.choices[0].message.content.strip()
        interests = [x.strip() for x in raw_interests.split(",") if x.strip()]
        
        if not interests:
            await update.message.reply_text("No interest keywords detected. Please try again.")
            return

    except Exception as e:
        print(f"ChatGPT API call failed: {e}")
        await update.message.reply_text("Service temporarily unavailable. Please try again later.")
        return

    # Save user interests to database
    if save_user_interests(user_id, username, interests):
        await update.message.reply_text(f"Your interests have been recorded: {', '.join(interests)}! Searching for matching players...")
        matches = find_matching_users(user_id, interests)
        if matches:
            match_list = "\n".join(
                [f"User {user['username']} (Interests: {', '.join(user['interests'])})" 
                 for user in matches]
            )
            await update.message.reply_text(f"Found matching players:\n{match_list}")
        else:
            await update.message.reply_text("No matching players found at the moment.")
    else:
        await update.message.reply_text("Failed to save interests. Please try again.")

def main():
    """Start the bot"""
    # Initialize application with ApplicationBuilder
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()