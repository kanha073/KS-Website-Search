
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import START_PIC, FLOOD, ADMIN 
from lazydeveloper.lazydb import db
from lazydeveloper.txt import lazydeveloper

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"""👋 Hey {message.from_user.mention}\nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ᴀᴜᴛᴏ ᴘᴏsᴛ search ʙᴏᴛ..\n\n<blockquote>♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/'>Kahna S</a></blockquote>\n"""
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
        ],[
        InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs ', url='https://t.me/AllTypeOfLinkss'),
        InlineKeyboardButton('🍂 18+ sᴜᴘᴘᴏʀᴛ ', url='https://t.me/+jt0FTlngGCc3OWI1')
        ],[
        InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ ', callback_data='about'),
        InlineKeyboardButton('ℹ ʜᴇʟᴘ ', callback_data='help')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, parse_mode=enums.ParseMode.HTML,  disable_web_page_preview=True)

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"👋 Hey {query.from_user.mention} \nɪ'ᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇ ᴀᴜᴛᴏ ᴘᴏsᴛ search ʙᴏᴛ.\n\n<blockquote>♥ ʙᴇʟᴏᴠᴇᴅ ᴏᴡɴᴇʀ <a href='https://telegram.me/_'>Kanha S</a></blockquote>",
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("✿.｡:☆ ᴏᴡɴᴇʀ ⚔ ᴅᴇᴠs ☆:｡.✿", callback_data='dev')
                ],[
                InlineKeyboardButton('📢 ᴜᴘᴅᴀᴛᴇs ', url='https://t.me/AllTypeOfLinkss'),
                InlineKeyboardButton('🍂 18+ sᴜᴘᴘᴏʀᴛ ', url='https://t.me/+jt0FTlngGCc3OWI1')
                ],[
                InlineKeyboardButton('🍃 ᴀʙᴏᴜᴛ ', callback_data='about'),
                InlineKeyboardButton('ℹ ʜᴇʟᴘ ', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=lazydeveloper.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=lazydeveloper.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "dev":
        await query.message.edit_text(
            text=lazydeveloper.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_message(filters.command('logs') & filters.user(ADMIN))
async def log_file(client, message):
    try:
        user_id = message.from_user.id
        if not await db.is_user_exist(user_id):
            await db.add_user(user_id)
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply_text(f"Error:\n`{e}`")

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
