import asyncio
from pyrogram import filters, Client, enums
from config import *
from lazydeveloper.lazydb import db 
from asyncio.exceptions import TimeoutError
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from plugins.Data import Data
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    MessageIdInvalidError
)


PHONE_NUMBER_TEXT = (
    "📞__ Now send your Phone number to Continue"
    " include Country code.__\n**Eg:** `+13124562345`\n\n"
    "Press /cancel to Cancel."
)


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

async def verify_lazy_user(user_id: int):
    return user_id in ADMIN 

async def verify_lazy_owner(user_id: int):
    return user_id == OWNER_ID 



# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_message(filters.private & filters.command("connect"))
async def connect_session(bot, msg):
    user_id = msg.from_user.id
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)

    if not await verify_lazy_owner(user_id):
        return await msg.reply("⛔ You are not authorized to use this command.")
    
    init = await msg.reply(
        "Starting session connection process..."
    )
    # get users session string
    session_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `TELETHON SESSION STRING`", filters=filters.text
    )
    if await cancelled(session_msg):
        return
    lazydeveloper_string_session = session_msg.text
    
    #get user api id 
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
        )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    
    # get user api hash
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text

    # 
    success = await bot.send_message(
        chat_id=msg.chat.id,
        text="Trying to login...\n\nPlease wait 🍟"
    )
    await asyncio.sleep(1)
    try:
        lazydeveloperrsession = TelegramClient(StringSession(lazydeveloper_string_session), api_id, api_hash)
        await lazydeveloperrsession.start()

        # for any query msg me on telegram - @LazyDeveloperr 👍
        if lazydeveloperrsession.is_connected():
            await db.set_session(user_id, lazydeveloper_string_session)
            await bot.send_message(
                chat_id=msg.chat.id,
                text="Session started successfully! ✅ \n\nNow simply index your database channel and add all sub-channels 🍿"
            )
            print(f"Session started successfully for user {user_id} ✅")
        else:
            raise RuntimeError("Session could not be started. Please re-check your provided credentials. 👍")
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please re-check your provided credentials. 👍")
    finally:
        await success.delete()
        await lazydeveloperrsession.disconnect()
        if not lazydeveloperrsession.is_connected():
            print("Session is disconnected successfully!")
        else:
            print("Session is still connected.")
        await init.edit_text("with ❤ @Legend_moon", parse_mode=enums.ParseMode.HTML)
        return

@Client.on_message(filters.private & filters.command("get_session"))
async def getsession(client , message):
    user_id = message.from_user.id
    
    if not await db.is_user_exist(user_id):
        await db.add_user(user_id)
    
    if not await verify_lazy_owner(user_id):
        return await message.reply("⛔ You are not authorized to use this command.")
    
    session = await db.get_session(user_id)
    
    if not session:
        await client.send_message(chat_id=user_id, text=f"😕NO session found !\n\n🧧 Please Login first with /login cmd...", parse_mode=enums.ParseMode.HTML)
        return
    await client.send_message(chat_id=user_id, text=f"Here is your session string...\n\n<spoiler><code>{session}</code></spoiler>\n\n⚠ Please dont share this string to anyone, You may loOSE your account.", parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("login"))
async def generate_session(bot, msg):
    lazyid = msg.from_user.id
    if not await db.is_user_exist(lazyid):
        await db.add_user(lazyid)

    if not await verify_lazy_owner(lazyid):
        return await msg.reply("⛔ You are not authorized to use this command.")
    
    init = await msg.reply(
        "sᴛᴀʀᴛɪɴG [ᴛᴇʟᴇᴛʜᴏɴ] sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ..."
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ. \nᴇxᴀᴍᴘʟᴇ : `+19876543210`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("sᴇɴᴅɪɴɢ ᴏᴛᴘ...")
    
    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` ᴀɴᴅ `API_HASH` ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ꜰᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪꜰ ʏᴏᴜ ɢᴏᴛ ɪᴛ, sᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀꜰᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ꜰᴏʀᴍᴀᴛ. \nɪꜰ ᴏᴛᴘ ɪs `12345`, **ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 10 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            
            await client.sign_in(password=password)
            
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return

    string_session = client.session.save()
    await db.set_session(lazyid, string_session)
    # await db.set_api(lazyid, api_id)
    # await db.set_hash(lazyid, api_hash)
    
    text = f"**ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n||`{string_session}`||"

    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    success = await phone_code_msg.reply(
        "Session generated ! Trying to login 👍"
    )
    # Save session to the dictionary
    await asyncio.sleep(1)
    try:
        sessionstring = await db.get_session(lazyid)

        lazydeveloperrsession = TelegramClient(StringSession(sessionstring), api_id, api_hash)
        await lazydeveloperrsession.start()

        # for any query msg me on telegram - @LazyDeveloperr 👍
        if lazydeveloperrsession.is_connected():
            await bot.send_message(
                chat_id=msg.chat.id,
                text="Session started successfully! ✅ \nNow simply index your database channel and add all sub-channels 🍿."
            )
            print(f"Session started successfully for user {user_id} ✅")
        else:
            raise RuntimeError("Session could not be started.")
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please try again.")
    finally:
        await success.delete()
        await lazydeveloperrsession.disconnect()
        if not lazydeveloperrsession.is_connected():
            print("Session is disconnected successfully!")
        else:
            print("Session is still connected.")
        await init.edit_text("with ❤ @LazyDeveloper", parse_mode=enums.ParseMode.HTML)
        return

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif "/restart" in msg.text:
        await msg.reply(
            "ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss!", quote=True)
        return True
    else:
        return False

# **********************************************************
# **********************************************************

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

# **********************************************************
# **********************************************************
