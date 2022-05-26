from django.core.management.base import BaseCommand, CommandError
from ugc.telegram_bot.bot import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, downloader, all_callback, start, mess_handler
import os
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(os.getenv("TELEGRAM_SECRET"), use_context=True)
        disp = updater.dispatcher
        disp.add_handler(CommandHandler("start", start))
        disp.add_handler(MessageHandler(Filters.text, mess_handler))
        disp.add_handler(CallbackQueryHandler(all_callback))
        disp.add_handler(MessageHandler(Filters.document, downloader))
        updater.start_polling()
        updater.idle()
