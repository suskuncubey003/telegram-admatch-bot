🤖 Telegram Reklam & Eşleşme Botu (AdMatch Bot)

Python ve pyTelegramBotAPI (telebot) kütüphanesi ile geliştirilmiş; kullanıcıların referans ve görevler ile puan kazanıp kanallarına reklam verebildiği veya cinsiyet bazlı sosyal eşleşme yapabildiği Telegram bot projesi.

🌟 Öne Çıkan Özellikler

🚻 Zorunlu Cinsiyet Seçimi: /start komutu sonrasında kullanıcıdan cinsiyet (Erkek / Kız) seçmesi istenir. Seçim tamamlanmadan ana menü açılmaz ve kullanıcıya başlangıç ödülü (+10 Puan) tanımlanır.

🔗 Referans (Davet & Kazan) Sistemi: Her kullanıcıya özel üretilen davet linki (t.me/BotUsername?start=ref_USERID) ile katılan her yeni üye için davet eden kullanıcıya +5 Puan verilir.

➕ Gruba Ekle & Kazan: Botu gruplara ekleyen/yönetici yapan kullanıcılara +10 Puan kazandıran görev altyapısı.

📢 Reklam Havuzu: Biriken puanlar ile kullanıcıların kendi kanal veya grup reklamlarını yayınlama imkanı.

💬 Sosyal Eşleşme: Erkek ve Kız kullanıcı havuzları arasında filtrelenmiş anonim sohbet/eşleşme mekanizması.

⚙️ Modüler Yapılandırma: Ortam değişkenleri (.env) ve merkezi konfigürasyon (config.py) yönetimi.

📁 Proje Dosya Yapısı

telegram-admatch-bot/
├── config.py          # Merkezi yapılandırma ve .env okuyucu
├── bot.py             # Ana bot işleyicisi ve komut yönlendirmeleri
├── database.py        # SQLite / MongoDB veritabanı işlemleri
├── .env               # Hassas ortam değişkenleri (Token, Admin ID vs.)
├── .gitignore         # GiT tarafından yoksayılacak dosyalar
├── requirements.txt   # Gerekli Python paketleri
└── README.md          # Proje dokümantasyonu


🛠️ Kurulum ve Çalıştırma

1. Depoyu Klonlayın

git clone https://github.com/kullanici-adi/telegram-admatch-bot.git
cd telegram-admatch-bot


2. Sanal Ortam Oluşturun ve Bağımlılıkları Yükleyin

python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/macOS için:
source venv/bin/activate

pip install -r requirements.txt


3. Ortam Değişkenlerini Ayarlayın

Dizinde .env adında bir dosya oluşturup @BotFather üzerinden aldığınız bilgileri ve sistem ayarlarını girin:

BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
BOT_USERNAME=AdMatchBot
DATABASE_PATH=database.db

POINTS_WELCOME=10
POINTS_REFERRAL=5
POINTS_ADD_GROUP=10

ADMIN_IDS=123456789


4. Botu Başlatın

python bot.py


📝 Lisans

Bu proje MIT lisansı altında sunulmaktadır.
