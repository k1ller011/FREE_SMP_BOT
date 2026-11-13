import json
import random
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

# Logging
logging.basicConfig(level=logging.INFO)

# Config faylini yuklaymiz
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
CHANNELS = config["channels"]
PROMO_POOLS = config["promo_pools"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- TUGMALAR (KEYBOARDS) ---

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Bonus Kodlarni Olish", callback_data="get_bonuses")],
        [InlineKeyboardButton(text="📖 To'liq Qo'llanma & Qoidalar", callback_data="guide_info")],
        [InlineKeyboardButton(text="🗺 Server Sirlari & Jihozlar (Old)", callback_data="server_secrets")],
        [InlineKeyboardButton(text="📌 Server IP va Ma'lumot", callback_data="server_ip")]
    ])
    return keyboard

def get_channels_keyboard():
    buttons = []
    for key, data in CHANNELS.items():
        buttons.append([InlineKeyboardButton(text=data["name"], url=data["invite_link"])])
    buttons.append([InlineKeyboardButton(text="🔍 Obunani Tasdiqlash", callback_data="check_sub")])
    buttons.append([InlineKeyboardButton(text="« Asosiy Menyu", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="« Asosiy Menyu", callback_data="main_menu")]
    ])

# --- BOT BUYRUQLARI VA CALLBACK'LAR ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome_text = (
        "🔥 **KILLERSTAX SMP — Rasmiy Bonus Botiga Xush Kelibsiz!** 🔥\n\n"
        "🤖 **Bot nima uchun qurilgan va maqsadi nima?**\n"
        "Bu bot serverimiz hamjamiyatini rivojlantirish, barcha rasmiy axborot kanal va guruhlarimizni birlashtirish hamda har bir vaypda o'yinchilarga adolatli va qiziqarli bonus resurslarini avtomatik ulashish uchun maxsus yaratilgan.\n\n"
        "👑 **Bot kim tomonidan ishlab chiqarilgan?**\n"
        "Loyiha va bot to'liq server asoschisi / bosh dasturchisi **KillerStax** tomonidan ishlab chiqilgan.\n\n"
        "📱 **Qaysi qurilmalarda kirsa bo'ladi?**\n"
        "Serverimizga xoh kompyuter (PC), xoh telefoningiz orqali (**PojavLauncher** ilovasi yordamida) istalgan vaqtda bemalol ulanib o'ynashingiz mumkin!\n\n"
        "⚠️ **Vayp va Server Tizimi:**\n"
        "Har safar serverda vayp bo'lganda, botdagi har bir kanal uchun ma'lum miqdordagi cheklangan promo-kod ishga tushadi. Vayp bo'lishi bilan serverga va botga birinchi bo'lib kirib, kodni olgan o'yinchilargina mukofotni qo'lga kiritadi!\n\n"
        "👇 Ko'proq ma'lumot uchun kerakli bo'limni tanlang:"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    main_text = (
        "⚡ **KILLERSTAX SMP Bonus Markazi**\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await callback.message.edit_text(main_text, parse_mode="Markdown", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "server_ip")
async def show_ip(callback: types.CallbackQuery):
    ip_info = (
        "🌐 **SERVER MA'LUMOTLARI VA IP MANZIL** 🌐\n\n"
        "📌 **IP Manzil:** `KILLERSTAX_SMP.aternos.me`\n"
        "⚙️ **Versiya:** 1.16.5+\n"
        "📱 **Qurilmalar:** PC va PojavLauncher (Android/iOS) to'liq qo'llab-quvvatlaydi!\n"
        "⚙️ **Admin telegram lichkasi:** `@K1LLER011`\n"
        "🚀 *Serverga ulaning va o'z sarguzashtingizni boshlang!*"
    )
    await callback.message.edit_text(ip_info, parse_mode="Markdown", reply_markup=get_back_keyboard())

@dp.callback_query(F.data == "server_secrets")
async def show_server_secrets(callback: types.CallbackQuery):
    secrets_text = (
        "🗺 **SERVER SIRLARI & EKSKLYUZIV JIHOZLAR** ⚔️\n\n"
        
        "--- 🔥 **HELLFIRE SET**  ---\n"
        "🔴 **Hellfire Helmet**\n"
        "   ├ 📌 Tavsif: Olovda yasalgan dubulg'a\n"
        "   ├ 🛡️ Passiv: Olov va lava immuniteti va HP regen\n"
        "   ├ 👑 Nether Qiroli: Barcha Nether moblari bo'ysunadi\n"
        "   ├ 🟢 Aktiv: `[F]` Mob chaqirish menusi (Full set)\n"
        "   ├ 🌀 Double Shift: `[SHIFT x2]` Nether moblari armiyasi\n"
        "   └ 👥 Team Menu: `/hellfireteam` (do'stlarni boshqarish)\n\n"
        
        "🔴 **Hellfire Chestplate**\n"
        "   ├ 📌 Tavsif: Vulkanik ko'krak nishoni\n"
        "   ├ 🛡️ Passiv: Urgan dushmanni olov aurasi bilan siylaydi\n"
        "   ├ 👑 Nether Qiroli: Netherda Strength II & Resistance II\n"
        "   └ 🌀 Skillar: Mob menusi va Double Shift (Full set)\n\n"

        "🔴 **Hellfire Leggings**\n"
        "   ├ 📌 Tavsif: Olovli vulkan shimi\n"
        "   ├ 🛡️ Passiv: HP <= 2.5 bo'lsa Strength II & Resistance II\n"
        "   └ 👑 Nether Qiroli: Nether moblari bo'ysunadi\n\n"

        "🔴 **Hellfire Boots**\n"
        "   ├ 📌 Tavsif: Lava tubidagi etiklar\n"
        "   ├ 🛡️ Passiv: Lavada Speed II tezlik\n"
        "   └ 👑 Nether Qiroli: Lava/olovda HP tez tiklanishi\n\n"

        "--- 👤 **SHADOW SET** ---\n"
        "⚫ **Shadow Helmet**\n"
        "   ├ 📌 Tavsif: Tungi soyalar toji\n"
        "   ├ 🧭 Radar: `/shadowradar` (20x20x20 maydonni ko'rish)\n"
        "   ├ 👥 Team: `/shadowteam` (Team boshqaruv GUI)\n"
        "   ├ ⚜️ Full Set: Soya rejimi (Armor ko'rinadi)\n"
        "   ├ 🟢 Aktiv: `[F]` Area Debuff Trap (15s)\n"
        "   └ 🔵 Tungi Kuch: Speed III & Strength I\n\n"

        "⚫ **Shadow Chestplate**\n"
        "   ├ 📌 Tavsif: Qorong'ulik qotili nimchasi\n"
        "   └ 🛡️ Passiv: Orqadan urganda 1.5x Kritik zarar\n\n"

        "⚫ **Shadow Leggings**\n"
        "   ├ 📌 Tavsif: Ko'rinmas soya shimi\n"
        "   └ 🛡️ Passiv: Doimiy Night Vision\n\n"

        "⚫ **Shadow Boots**\n"
        "   ├ 📌 Tavsif: Ovoz chiqarmas soya etiklari\n"
        "   └ 🛡️ Passiv: Speed II va Jump Boost I\n\n"

        "--- 🌪️ **STORM SET** ---\n"
        "🔵 **Storm Crown**\n"
        "   ├ 📌 Tavsif: Momaqaldiroq saltanati toji\n"
        "   ├ 🛡️ Passiv: Dushman urganda 5foiz ehtimol bilan qurolini tushiradi\n"
        "   ├ 👥 Team: `/stormteam` (chaqmoqli aura do'stlarga tegmaydi)\n"
        "   └ ⚡ Ob-havo: Yomg'irda Speed II & Strength I\n\n"

        "🔵 **Storm Chestplate**\n"
        "   ├ 📌 Tavsif: Tufon ko'krak nishoni\n"
        "   └ 🛡️ Passiv: O'q otilganda o'shanga qaytaradi va o'zi zarar olmaydi\n\n"

        "🔵 **Storm Leggings**\n"
        "   ├ 📌 Tavsif: Yashin tezligidagi shimi\n"
        "   ├ 🛡️ Passiv: Dushmanga Slowness II beradi\n"
        "   └ ⚡ Ob-havo: Yomg'irda Speed II & Strength I\n\n"

        "🔵 **Storm Boots**\n"
        "   ├ 📌 Tavsif: Momaqaldiroq etiklari\n"
        "   └ 🛡️ Passiv: Portlash zarari 0% va doimiy Speed I\n\n"

        "--- ⚔️ **UNIKAL ARTEFAKTLAR VA QUROLLAR** ---\n"
        "⚡ **Ultra Blade**\n"
        "   ├ 📌 Tavsif: Combo va xavfsizlik qilichi\n"
        "   ├ 💫 Passiv: Doimiy Speed I & Fire Resistance\n"
        "   ├ 📈 Combo: Har zarbada +0.25 zarar (10s urilmasa reset)\n"
        "   └ ✨ Right Click: 20s Invincible, Strength II, Regen III (CD: 2m)\n\n"

        "💥 **Explosive Bow**\n"
        "   ├ 📌 Tavsif: Portlovchi kamon\n"
        "   └ 🎯 Qobiliyat: Creeper kabi kuchli portlash va 10 HP zarar\n\n"

        "🗡️ **Killer Blade**\n"
        "   ├ 📌 Tavsif: Davlati oshgan sari kuchi ortadigan qilich\n"
        "   ├ 📊 Daraja: Level 1 dan 7 gacha (Killarga qarab)\n"
        "   ├ 🔮 O'ng Click: Qarayotgan joyga teleport (Lvl 7)\n"
        "   └ 🛡️ Shift + O'ng Click: Immortal Mode (Lvl 7)\n\n"

        "☠️ **Outlaws Blade**\n"
        "   ├ 📌 Tavsif: Debuff beruvchi daxshatli qilich\n"
        "   └ 🧪 Qobiliyat: Hunger, Poison, Blindness (Har 3 killda vaqti oshadi)\n\n"

        "✨ **Deathdagger**\n"
        "   ├ 📌 Tavsif: Enchant darajasi cheksiz o'sadigan xanjar\n"
        "   └ 🎯 Qobiliyat: 1 Kill = 1 Ochko (Shift + Right Click orqali upgrade)\n\n"

        "💀 **Necromancer's Blade**\n"
        "   ├ 📌 Tavsif: Qorong'ulik va o'liklar tigi\n"
        "   ├ 🛡️ Passiv: Y<60 da Night Vision/Resistance, Netherda Fire Res/Strength\n"
        "   ├ 🧟 Aktiv: `[F]` Zombi va Skelet armiyasi (Boshlanishi 5 ta)\n"
        "   └ 👥 Buyruqlar: `/necroteam`, `/necroteamlist`, `/necroteamclear`\n\n"

        "❄️ **Frostblade**\n"
        "   ├ 📌 Tavsif: Qadimgi muzliklar tigi\n"
        "   ├ 🛡️ Passiv: 20foiz ehtimol bilan dushmanni muzlatadi\n"
        "   ├ ⛄ Aktiv: Qor odam armiyasi (8 tadan 40 tagacha oshadi)\n"
        "   └ 👥 Buyruqlar: `/frostteam`, `/frostteamlist`, `/frostclear`\n\n"

        "📌 **BOSHQARUV VA QO'SHIMCHA MA'LUMOTLAR:**\n"
        "• 🛠️ Barcha jihoz retseptlari: Serverda `/recipes` buyrug'ini yozing\n"
        "• ⚠️ Eslatma: Bazi skillar ishlashi uchun to'liq armor (Full set) kiyilgan bo'lishi shart!\n"
        "• 👤 Bog'lanish uchun: `@K1LLER011`\n"
    )
    await callback.message.edit_text(secrets_text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@dp.callback_query(F.data == "guide_info")
async def show_guide(callback: types.CallbackQuery):
    guide_text = (
        "📖 **Qo'llanma, Qoidalar va Yordam**\n\n"
        "🎁 **Promo-Kodlar va Loot Tizimi:**\n"
        "• Jami 25 ta kod mavjud. Omadli va chaqqon minimal 5 ta o'yinchi to'liq bepul loot oladi, maksimal 25 ta alohida o'yinchi loot olishi mumkin.\n"
        "• Bu lootlar serverdagi o'sha afsonaviy, 1 vayp davomida atigi 1 marta yasaladigan noyob qurollarni yasashni osonlashtirish uchun beriladi!\n\n"
        "⏳ **Vayp va Kanalda Qolish:**\n"
        "• Vayp taxminan har 3 oyda bir marta bo'ladi. Aniq sanasini o'tkazib yubormaslik uchun kanalni kuzatib boring.\n"
        "• ⚠️ **Muhim:** Obuna bo'lib, keyin darhol chiqib ketmang! Kelgusi vayplarda yana obuna bo'lishga vaqt sarflab o'tirmasligingiz uchun kanallarda doimiy obunachi bo'lib qolganingiz ma'qul. Aks holda kelgusi safar sovg'a ololmasligingiz mumkin.\n\n"
        "🚨 **Xavfsizlik Eslatmasi:**\n"
        "Botdan olgan shaxsiy promo-kodlaringizni hech kimga ko'rsatmang! Agar kodni boshqasiga berib yuborsangiz va u sizdan oldin ishlatib qo'ysa — bunga biz javobgar emasmiz.\n\n"
        "⚖️ **Server Qoidalari:**\n"
        "• Cheat ishlatish, server TPS-sini tushiruvchi mexanika qurish qat'iyan taqiqlangan (jazosi 30 kun ban).\n"
        "• 📌 Batafsil qoidalarni bilish uchun serverga kiring va chatga yozing: `/rules`\n\n"
        "🛠️ **Muammo chiqsa kimga murojaat qilinadi?**\n"
        "Xatolik yoki savollar bo'yicha admin lichkasiga yozing: `@K1LLER011`"
    )
    await callback.message.edit_text(guide_text, parse_mode="Markdown", reply_markup=get_back_keyboard())

@dp.callback_query(F.data == "get_bonuses")
async def list_bonuses(callback: types.CallbackQuery):
    text = (
        "🎯 **Bonus Olish Bosqichlari:**\n\n"
        "1️⃣ Pastdagi barcha rasmiy kanallar va sahifalarga a'zo bo'ling.\n"
        "2️⃣ Obuna bo'lib bo'lgach, **'🔍 Obunani Tasdiqlash'** tugmasini bosing.\n"
        "3️⃣ Bot obunangizni tekshirib, darhol maxsus promo-kodlaringizni taqdim etadi! Bu promo-kodlarni serverga kirib `/claim <kod>` qilib sovg'alarni oling!\n\n"
        "👇 *Kerakli kanallar ro'yxati:*"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_channels_keyboard())

@dp.callback_query(F.data == "check_sub")
async def verify_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    not_subscribed = []

    for key, data in CHANNELS.items():
        if data["type"] == "telegram":
            try:
                member = await bot.get_chat_member(chat_id=data["channel_id"], user_id=user_id)
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    not_subscribed.append(data["name"])
            except Exception:
                not_subscribed.append(data["name"])

    if not_subscribed:
        await callback.answer("⚠️ Hali barcha kanallarga obuna bo'lmadingiz! Iltimos, obuna bo'ling.", show_alert=True)
        
        text = (
            "❌ **Tekshiruv muvaffaqiyatsiz tugadi!**\n\n"
            "Promo-kodlarni olish uchun quyidagi qolgan kanallarga ham obuna bo'ling:\n"
        )
        for ch in not_subscribed:
            text += f"▫️ {ch}\n"
        await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_channels_keyboard())
    else:
        code_tg_rasmiy = random.choice(PROMO_POOLS["tg_rasmiy"])
        code_tg_muhokama = random.choice(PROMO_POOLS["tg_muhokama"])
        code_tg_yt = random.choice(PROMO_POOLS["tg_yt"])
        code_yt = random.choice(PROMO_POOLS["youtube"])
        code_insta = random.choice(PROMO_POOLS["insta"])

        success_response = (
            "🎉 **Tabriklaymiz! Barcha obunalar muvaffaqiyatli tasdiqlandi!**\n\n"
            "💎 **Sizning shaxsiy promo-kodlaringiz:**\n"
            f"🔹 Rasmiy Kanal: `{code_tg_rasmiy}`\n"
            f"🔹 Muhokama Guruhi: `{code_tg_muhokama}`\n"
            f"🔹 YT Telegram: `{code_tg_yt}`\n"
            f"🔴 YouTube Bonus: `{code_yt}`\n"
            f"📸 Instagram Bonus: `{code_insta}`\n\n"
            "📌 **Qanday faollashtiriladi?**\n"
            "Serverga (PC yoki PojavLauncher) orqali kiring va chatga yozing:\n"
            f"👉 `/claim {code_tg_rasmiy}`\n\n"
            "⚠️ **Eslatma:** Kodlarni hech kimga ko'rsatmang! Har bir kod minimum 5 ta, maksimum 25 ta o'yinchi uchun amal qiladi. Vayp paytida ulgursangiz — mukofot(lar) sizniki! Agar ulgursangiz bu mukofotlarni afsonaviy aslaha va qurollarni yasashda ishlating!"
        )
        
        await callback.message.edit_text(success_response, parse_mode="Markdown", reply_markup=get_back_keyboard())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())