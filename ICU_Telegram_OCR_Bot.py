
# ICU Multiverse - Telegram Bot Integration with OCR API

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import base64
import os

# ✅ Replace with your actual credentials
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OCR_API_URL = "https://img-service.com/api/ocr"  # Replace with real endpoint
OCR_API_KEY = "YOUR_OCR_API_KEY"

# Function to send an image to the OCR API and retrieve extracted text
def extract_text_from_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    data = {
        "api_key": OCR_API_KEY,
        "image": encoded_image,
        "output_format": "text"
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(OCR_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("text", "No text found.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Handler function for processing image messages
def handle_image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1].get_file()
    file_path = photo.download()

    extracted_text = extract_text_from_image(file_path)
    update.message.reply_text(f"Extracted Text:
{extracted_text}")

    # Optional: Clean up downloaded file
    os.remove(file_path)

# Main function to start the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add a message handler for images
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
