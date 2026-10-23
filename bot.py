# bot.py dosyanızın üst kısmına ekleyin:
from admin import register_admin_handlers

# ... (Mevcut kodlarınız) ...

# bot.py dosyanızın en altındaki if __name__ == "__main__": bloğundan hemen önce ekleyin:
register_admin_handlers(bot)

if __name__ == "__main__":
    print(f"@{Config.BOT_USERNAME} başlatılıyor...")
    bot.infinity_polling(allowed_updates=['message', 'callback_query', 'my_chat_member'])
