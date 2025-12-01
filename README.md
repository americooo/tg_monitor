# Telegram Guruh Monitoring Boti

Bu loyiha Telegram guruhini avtomatik monitoring qilish uchun mo‘ljallangan botdir. Bot foydalanuvchilarni guruhga qo‘shish, chiqarish, soatlik statistika va kunlik hisobotlarni avtomatik qayd etadi.

---

## Loyiha maqsadi

- Guruhga qo‘shilgan va chiqqan foydalanuvchilarni bazaga yozish.  
- Soatlik va kunlik statistikani hisoblash.  
- Hozir guruhda nechta foydalanuvchi borligini ko‘rsatish.  
- Har bir foydalanuvchi faoliyatini kuzatish.

---

## Texnologiyalar

- Python 3.10+  
- Aiogram (Telegram bot framework)  
- SQLAlchemy (Async ORM)  
- SQLite (yoki boshqa DB: PostgreSQL, MySQL)  
- dotenv (env fayl orqali sozlash)  

---

## Fayllar tuzilishi
```bash
project_folder/
│
├─ bot.py # Asosiy bot kodi
├─ db.py # DB bilan ishlash
├─ models.py # User va boshqa modellari
├─ run.py # Botni ishga tushirish fayli
├─ .env # Muhit o'zgaruvchilari
└─ tg_monitor.db # SQLite bazasi (agar SQLite ishlatilsa)
```
yaml
Copy code

---

## ⚙️ O‘rnatish va ishga tushirish

1. Loyihani klonlash:

```bash
cd project_folder
Virtual muhit yaratish va kutubxonalarni o‘rnatish:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
.env faylini sozlash:

ini
Copy code
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
DATABASE_URL=sqlite+aiosqlite:///./tg_monitor.db
Botni ishga tushirish:


Copy code
python3 run.py
🧪 Test qilish
Bazani tozalash (testdan oldin):



rm tg_monitor.db
Bot ishga tushganda yangi bo‘sh bazani yaratadi.

Botni ishga tushirish:



python3 run.py
Guruhga qo‘shish / chiqarish:

Sinov foydalanuvchisini guruhga qo‘shing → bazaga yozilganini tekshiring.

Foydalanuvchi guruhdan chiqsin → left_at va duration_in_group yangilanishini tekshiring.

/stats komandasini tekshirish:

Guruhda /stats yozing.

Bugungi qo‘shilganlar, chiqqanlar, hozir guruhda bo‘lganlar soni, eng ko‘p va eng kam qo‘shilgan soatlar ko‘rsatiladi.

Soatlik statistika UTC+5 (O‘zbekiston vaqti) bilan hisoblanadi.

/stats funksiyasi
Bugungi qo‘shilganlar

Bugungi chiqqanlar

Hozir guruhda bo‘lganlar

Eng ko‘p va eng kam qo‘shilgan soatlar (lokal vaqt)


# /stats funksiyasi uchun qisqa misol
from datetime import timedelta
LOCAL_OFFSET = timedelta(hours=5)
hours_counter = Counter()
for user in users_today:
    local_joined = user.joined_at + LOCAL_OFFSET
    hours_counter[local_joined.hour] += 1
Tavsiyalar
joined_at va left_at UTC da saqlanadi, faqat ko‘rsatishda lokal vaqtga o‘tkaziladi.

Testdan oldin bazani tozalash tavsiya etiladi.

Guruhga admin sifatida qo‘shing, aks holda bot foydalanuvchi qo‘shish/chiqarishni aniqlay olmaydi.


yaml
Copy code
Bugungi statistika:

Bugun qo‘shilganlar: 5
Chiqqanlar: 2
Hozir guruhda: 8

Eng ko‘p qo‘shilgan soat: 14:00 — 3 ta
Eng kam qo‘shilgan soat: 09:00 — 1 ta


Dasturchi

Amirbek Raxmatullayev 3-kurs
Acharya University, Karakul, Uzbekistan

