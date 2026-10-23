import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
import database as db

def register_admin_handlers(bot: telebot.TeleBot):
    """Admin komutlarını ve callback işleyicilerini bot nesnesine kaydeder."""

    def is_admin(user_id: int) -> bool:
        """Kullanıcının admin olup olmadığını kontrol eder."""
        return user_id in Config.ADMIN_IDS

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        """Admin yönetim paneli ana menüsü"""
        if not is_admin(message.from_user.id):
            bot.reply_to(message, "⛔ **Erişim Engellendi:** Bu komut sadece yöneticiler içindir.")
            return

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("📢 Reklam İnceleme Havuzu", callback_data="admin_ads_list")
        )
        markup.row(
            InlineKeyboardButton("📊 Genel İstatistikler", callback_data="admin_stats"),
            InlineKeyboardButton("📣 Toplu Duyuru Yap", callback_data="admin_broadcast")
        )

        bot.send_message(
            message.chat.id,
            "🛡️ **Admin Yönetim Paneline Hoş Geldiniz**\n\nAşağıdaki butonlardan yapmak istediğiniz işlemi seçin:",
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def handle_admin_callbacks(call):
        if not is_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Yetkiniz yok!", show_alert=True)
            return

        # Bekleyen Reklamlar
        if call.data == "admin_ads_list":
            pending_ads = db.get_pending_ads()
            if not pending_ads:
                bot.answer_callback_query(call.id, "Onay bekleyen reklam bulunmuyor.", show_alert=True)
                return

            bot.answer_callback_query(call.id)
            for ad in pending_ads:
                markup = InlineKeyboardMarkup()
                markup.row(
                    InlineKeyboardButton("✅ Onayla", callback_data=f"ad_approve_{ad['id']}"),
                    InlineKeyboardButton("❌ Reddet", callback_data=f"ad_reject_{ad['id']}")
                )
                bot.send_message(
                    call.message.chat.id,
                    f"📢 **Reklam Onay Talebi**\n"
                    f"🆔 **Reklam ID:** `{ad['id']}`\n"
                    f"👤 **Gönderen:** `{ad['user_id']}`\n"
                    f"📅 **Tarih:** `{ad['created_at']}`\n\n"
                    f"📝 **İçerik:**\n{ad['content']}",
                    reply_markup=markup
                )

        # İstatistikler
        elif call.data == "admin_stats":
            stats = db.get_system_stats()
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                f"📊 **Sistem İstatistikleri**\n\n"
                f"👤 **Toplam Kullanıcı:** `{stats['total_users']}`\n"
                f"👨 **Erkek Kullanıcı:** `{stats['male_users']}`\n"
                f"👧 **Kız Kullanıcı:** `{stats['female_users']}`\n"
                f"📢 **Onaylanan Reklamlar:** `{stats['approved_ads']}`\n"
                f"⏳ **Bekleyen Reklamlar:** `{stats['pending_ads']}`"
            )

        # Toplu Mesaj Gönderme Rehberi
        elif call.data == "admin_broadcast":
            bot.answer_callback_query(call.id)
            bot.send_message(
                call.message.chat.id,
                "📣 **Toplu Duyuru Göndermek İçin:**\n\n"
                "`/broadcast Mesajınız buraya gelecek`\n\n"
                "şeklinde mesaj atabilirsiniz. Mesaj tüm kayıtlı kullanıcılara iletilecektir."
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith(("ad_approve_", "ad_reject_")))
    def handle_ad_decision(call):
        if not is_admin(call.from_user.id):
            return

        action, ad_id = call.data.rsplit("_", 1)
        ad_id = int(ad_id)
        ad = db.get_ad_by_id(ad_id)

        if not ad:
            bot.answer_callback_query(call.id, "Reklam bulunamadı.")
            return

        if action == "ad_approve":
            db.update_ad_status(ad_id, "approved")
            bot.answer_callback_query(call.id, "Reklam onaylandı!")
            bot.edit_message_text(
                f"✅ **Reklam Onaylandı!**\n\n🆔 **ID:** `{ad_id}`\n📝 **İçerik:** {ad['content']}",
                call.message.chat.id,
                call.message.message_id
            )
            # Reklam sahibine bildirim gönder
            try:
                bot.send_message(ad['user_id'], "🎉 **Tebrikler!** Reklam talebiniz onaylandı ve yayınlandı.")
            except Exception:
                pass

        elif action == "ad_reject":
            db.update_ad_status(ad_id, "rejected")
            bot.answer_callback_query(call.id, "Reklam reddedildi.")
            bot.edit_message_text(
                f"❌ **Reklam Reddedildi.**\n\n🆔 **ID:** `{ad_id}`",
                call.message.chat.id,
                call.message.message_id
            )
            # Reklam sahibine bildirim gönder
            try:
                bot.send_message(ad['user_id'], "❌ **Üzgünüz,** reklam talebiniz yöneticiler tarafından uygun görülmedi.")
            except Exception:
                pass

    @bot.message_handler(commands=['broadcast'])
    def broadcast_message(message):
        """Tüm kullanıcılara toplu mesaj atar."""
        if not is_admin(message.from_user.id):
            return

        text = message.text.replace("/broadcast", "").strip()
        if not text:
            bot.reply_to(message, "⚠️ Lütfen duyuru mesajı girin. Örnek: `/broadcast Merhaba millet!`")
            return

        users = db.get_all_users()
        success, failed = 0, 0

        bot.send_message(message.chat.id, f"🚀 Duyuru `{len(users)}` kullanıcıya gönderiliyor...")

        for user in users:
            try:
                bot.send_message(user['user_id'], f"📣 **Yönetici Duyurusu:**\n\n{text}")
                success += 1
            except Exception:
                failed += 1

        bot.send_message(
            message.chat.id,
            f"✅ **Duyuru Tamamlandı!**\n\n"
            f"🟢 **Başarılı:** `{success}`\n"
            f"🔴 **Başarısız (Engellemiş):** `{failed}`"
        )
