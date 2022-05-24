from django.core.management.base import BaseCommand, CommandError
from ugc.telegram_bot.bot import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(os.getenv("TELEGRAM_SECRET"), use_context=True)
        disp = updater.dispatcher
        disp.add_handler(CommandHandler("start", start))
        disp.add_handler(MessageHandler(Filters.text, mess_handler))
        disp.add_handler(CallbackQueryHandler(all_callback))
        # disp.add_handler(CallbackQueryHandler(call_back_sub))
        # disp.add_handler(CallbackQueryHandler(callback_login))
        updater.start_polling()
        updater.idle()
