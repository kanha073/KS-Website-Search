
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

from pyrogram import Client, filters, enums
# from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from pyrogram import Client, filters
import re
import math
import asyncio
from config import *
from lazydeveloper.helpers import  validate_query
# Initialize Pyrogram Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from lazydeveloper.lazydb import db
# latest
from imdb import IMDb, Movie
imdb = IMDb() 
from fuzzywuzzy import process
from pyrogram.errors import MessageNotModified

user_files_data = {}
files_per_page = 10
should_delete = []
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    _, offset = query.data.split("_")

    try:
        offset = int(offset)
    except:
        offset = 0

    user_id = query.from_user.id
    
    # print(f"user id => {user_id}")
    files, n_offset, total = await get_api_results(user_id,  offset=offset, filter=True)
    # print(files)
    # print(n_offset)
    # print(total)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return

    btn = [
            [
                InlineKeyboardButton(
                    text=f"📂 {file[0]}",  # movie_name
                    url=file[1]           # target_url
                )
            ]
            for file in files
        ]


    if 0 < offset <= int(MAX_BTN):
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - int(MAX_BTN)

    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton(
                    "⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
                InlineKeyboardButton(
                    f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
                InlineKeyboardButton(
                    "ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")
            ],
        )
    btn.append([
        InlineKeyboardButton("How To Open Link ❓", url="https://t.me/Howtopenlinksss")
    ])
    btn.append([
        InlineKeyboardButton("🪅Request", url="https://t.me/kslinkupdate1"),
        InlineKeyboardButton("♻️Backup", url="https://t.me/ksxplain12")
    ])
    btn.append([
        InlineKeyboardButton("18+  Channel 🔞", url="https://t.me/+cvawyNXo-5FiZjk1")
    ])
    try:
        reply_markup=InlineKeyboardMarkup(btn)
        await query.message.edit_reply_markup(reply_markup)
    except MessageNotModified:
        pass
    await query.answer("❤ Powered By @LazyDeveloperr ❤")
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

@Client.on_message(filters.group & filters.text & filters.incoming & ~filters.command(['start']))
async def message_handler(client, message):
      try:
         if message.text.startswith("/"):
               return
         print("\nMessage Received: " + message.text)
        # Validate and sanitize query
         args = message.text
         user_id = message.from_user.id
         txt = await message.reply(f"**⏳ Searching for links matching:** `{args}` 🔍")
         
         queryz = await validate_query(args)
         if not queryz:
            await message.reply("Please provide a valid search query.")
            return
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
         queryz = queryz.lower()
         find = queryz.split(" ")
         queryz = ""
         removes = ["in", "series", "full", "horror", "thriller", "mystery", "print", "file", "2k", "4k", "2004", "2024", "2025", "2020", "2021", "2022", "2023","new","movies", "the", "a", "an", "480", "480p", "720p", "720", "1080p", "1080", "hindi","english", "eng", "hin","kor","korean" ]
         for x in find:
             if x in removes:
                 continue
             else:
                 queryz = queryz + x + " "
                 # print(f"New search is : {search}")
         queryz = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", queryz, flags=re.IGNORECASE)
         queryz = re.sub(r"\s+", " ", queryz).strip()
         queryz = queryz.replace("-", " ")
         queryz = queryz.replace(":","")
         # print(f"Search Query: {queryz}")
         await asyncio.sleep(1)
         sessionstring = await db.get_session(OWNER_ID)
         if sessionstring is None:
            await txt.delete()
            # msstt h na - 😂 - isiliye copy krne aaye ho 😂 - kr lo - kr lo 
            return await message.reply(
                    "Please visit again later. I’m waiting for my owner to initialize me. 😔\n\n"
                    "If you know my owner, kindly ask him to initialize me. ❤️"
                )
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
         Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
         if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()
         # await Lazyuserbot.start()
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
         search_results = []
         try:
            # Search for messages containing the query term in the database channel #limit=5
            async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz):
               if search_msg.text:
                  # Look for a URL in the first line
                  match = re.match(r"(https?://[^\s]+)", search_msg.text)
                  if match:
                     target_url = match.group(1).strip()  # Extract the URL

                     # Extract the movie name from text in parentheses ()
                     movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                     movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

                     # Append the result as a tuple of (movie_name, target_url)
                     search_results.append({"movie_name": movie_name, "target_url": target_url})
                     # print(search_results)
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
            if not search_results:
               miss_spelled = await lazydeveloperr_spell_check(queryz, message)
               if miss_spelled:
                  await txt.delete()
                  queryz = miss_spelled
                  return await display_files(message, user_id, queryz, offset=0)
                # Search for messages containing the query term in the database channel #limit=5
                #   async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz):
                #     if search_msg.text:
                #         # Look for a URL in the first line
                #         match = re.match(r"(https?://[^\s]+)", search_msg.text)
                #         if match:
                #             target_url = match.group(1).strip()  # Extract the URL

                #             # Extract the movie name from text in parentheses ()
                #             movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                #             movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

                #             # Append the result as a tuple of (movie_name, target_url)
                #             search_results.append({"movie_name": movie_name, "target_url": target_url})
                #             # print(search_results)
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
            print(f"Search results saved for user {user_id}: {search_results}")
         except Exception as e:
               print(f"Error while searching messages: {e}")
               await message.reply("An error occurred while searching.")
               return
         # Handle no results
         if search_results:
            user_files_data[user_id] = search_results
            await txt.delete()
            await display_files(message, user_id, queryz, offset=0)  # Display page 1
         else:
            no_result_text = (
                f"**No results found for '{queryz}'**\n\n"
                f"Try refining your query or checking spelling on "
                f"[Google](http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie) 🔍."
            )
            link = f"http://www.google.com/search?q={queryz.replace(' ', '%20')}%20Movie"
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Check On Google 🔍", url=link)]
            ])
            await txt.delete()
            no_result = await message.reply(no_result_text, reply_markup=btn, disable_web_page_preview=True)
            asyncio.create_task(delete_lazy_msg(no_result))
            return
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
        
      except Exception as e:
         print(e)
         if txt:
               await txt.delete()
         await message.reply("I couldn't process your request. Please try again later.")
      finally:
         asyncio.create_task(delete_lazy_msg(message))
         await asyncio.sleep(2)
         # tried to avoid overhead  - session load !
         await Lazyuserbot.disconnect()
         if not Lazyuserbot.is_connected():
               print("Session is disconnected successfully!")
         else:
               print("Session is still connected.")
               await Lazyuserbot.disconnect()
               print("⚠ Tried to disconnect session.\n If u r seeing this message again again then please report to  @LazyDeveloper ❤")
         return

# ✅ Global dict: store files per user
async def lazydeveloperr_spell_check(wrong_name, msg):
    async def search_movie(wrong_name):
        search_results = imdb.search_movie(wrong_name)
        return [movie['title'] for movie in search_results]
    movie_list = await search_movie(wrong_name)
    if not movie_list:
        return
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
    # Try up to 5 closest matches
    for _ in range(5):
        closest_match = process.extractOne(wrong_name, movie_list)
        if not closest_match or closest_match[1] <= 80:
            return  # No good match
        movie = closest_match[0]
        lazy_id = msg.id
        # ✅ Check if Telegram search gives results for this candidate
        files, offset, total_results = await get_search_results_badAss_LazyDeveloperr(
            msg.from_user.id, lazy_id, movie
        )
        if files:
            return movie  # Only return if real results exist
        # Else, remove that candidate and try next fuzzy match
        movie_list.remove(movie)
        print(f"here is files i got in lazy ai spell check : {files}")
    return


async def get_search_results_badAss_LazyDeveloperr(user_id, lazy_id, query, max_results=10, offset=0):
    files = []
    try:
        sessionstring = await db.get_session(OWNER_ID)
        if not sessionstring:
            return [], "", 0
        Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
        if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()
        # ✅ Build regex pattern
        query = query.strip()
        if not query:
            raw_pattern = '.'
        elif ' ' not in query:
            raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
        else:
            raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
        try:
            regex = re.compile(raw_pattern, flags=re.IGNORECASE)
        except:
            return [], "", 0
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
        # ✅ First fetch some messages (rough search by first word, then refine with regex)
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=query.split()[0]):
            if search_msg.text:
                match = re.match(r"(https?://[^\s]+)", search_msg.text)
                if match:
                    target_url = match.group(1).strip()
                    movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                    movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                    # ✅ Apply regex filter on movie_name
                    if regex.search(movie_name):
                        files.append((movie_name, target_url))

        total_results = len(files)
        next_offset = offset + max_results
        if next_offset >= total_results:
            next_offset = ""
        # Slice results for pagination
        files = files[offset:offset + max_results]
        # ✅ Store results into global user_files_data
        user_files_data[user_id] = files  
        print(f"get_search_results_badAss_LazyDeveloperr => {files}")
        return files, next_offset, total_results
    except Exception as e:
        print(f"Error in get_search_results_badAss_LazyDeveloperr: {e}")
        return [], "", 0

# async def get_search_results_badAss_LazyDeveloperr(user_id, lazy_id, query, max_results=10, offset=0):
#     files = []
#     try:
#         sessionstring = await db.get_session(OWNER_ID)
#         if not sessionstring:
#             return [], "", 0

#         Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
#         if not Lazyuserbot.is_connected():
#             await Lazyuserbot.start()

#         async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=query):
#             if search_msg.text:
#                 # Extract URL from first line
#                 match = re.match(r"(https?://[^\s]+)", search_msg.text)
#                 if match:
#                     target_url = match.group(1).strip()

#                     # Extract movie name from text in parentheses
#                     movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
#                     movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

#                     # ✅ Always save as tuple
#                     files.append((movie_name, target_url))

#         total_results = len(files)
#         next_offset = offset + max_results
#         if next_offset >= total_results:
#             next_offset = ""

#         # Slice results for pagination
#         files = files[offset:offset + max_results]
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

#         # ✅ Store results into global user_files_data
#         user_files_data[user_id] = files  
#         print(f"get_search_results_badAss_LazyDeveloperr=>  {files}")
#         return files, next_offset, total_results

#     except Exception as e:
#         print(f"Error in get_search_results_badAss_LazyDeveloperr: {e}")
#         return [], "", 0
async def delete_lazy_msg(msg):
    try:
        await asyncio.sleep(SELF_DELETE_SECONDS)
        await msg.delete()
    except Exception as LazyDeveloperr:
        print(LazyDeveloperr)

async def display_files(message, user_id, lazydevelopr_query, offset):
    try:
        files, offset, total_results = await get_api_results(user_id, offset=0, filter=True)
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
        btn = [
            [
                InlineKeyboardButton(
                    text=f"📂 {file[0]}",  # movie_name
                    url=file[1]           # target_url
                )
            ]
            for file in files
        ]
        if offset != "":
            btn.append(
                [
                    InlineKeyboardButton(
                        text=f"🗓 1/{math.ceil(int(total_results) / int(MAX_BTN))}",
                        callback_data="pages"
                    ),
                    InlineKeyboardButton(
                        text="ɴᴇxᴛ ⋟", callback_data=f"next_{offset}"
                    )
                ]
            )
        else:
            btn.append([InlineKeyboardButton(text="🗓 1/1", callback_data="pages")])

        btn.append([
            InlineKeyboardButton("How To Open Link ❓", url="https://t.me/Howtopenlinksss")
        ])
        btn.append([
            InlineKeyboardButton("🪅Request", url="https://t.me/kslinkupdate1"),
            InlineKeyboardButton("♻️Backup", url="https://t.me/ksxplain12")
        ])
        btn.append([
            InlineKeyboardButton("18+  Channel 🔞", url="https://t.me/+cvawyNXo-5FiZjk1")
        ])
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
        lazymsg = await message.reply_text(
            f"<blockquote><b>👻 Here is what i found for your query <code>{lazydevelopr_query}</code></b></blockquote>",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        asyncio.create_task(delete_lazy_msg(lazymsg))
    except Exception as e:
        print(e)

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

async def get_api_results(user_id, max_results=MAX_BTN, offset=0, filter=False):
    """For given query lazydeveloper returns (results, next_offset)"""
    files_data = user_files_data.get(user_id, [])
    total_results = len(files_data)
    next_offset = offset + max_results
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

    # Slice the files list according to the offset and max_results
    raw_files = files_data[offset:offset + max_results]

    # ✅ Force everything into tuple format (movie_name, target_url)
    files = []
    for f in raw_files:
        if isinstance(f, dict):
            files.append((f.get("movie_name", "Unknown"), f.get("target_url", "")))
        elif isinstance(f, (tuple, list)) and len(f) >= 2:
            files.append((f[0], f[1]))
        else:
            print(f"⚠ Unknown format in files_data: {f}")
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

    if next_offset > total_results:
        next_offset = ''

    return files, next_offset, total_results

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

# async def lazydeveloperr_spell_check(wrong_name, msg):
#     async def search_movie(wrong_name):
#         search_results = imdb.search_movie(wrong_name)
#         movie_list = [movie['title'] for movie in search_results]
#         return movie_list
#     user_id = msg.from_user.id
#     movie_list = await search_movie(wrong_name)
#     if not movie_list:
#         return
#     for _ in range(5):
#         closest_match = process.extractOne(wrong_name, movie_list)
#         if not closest_match or closest_match[1] <= 80:
#             return 
#         movie = closest_match[0]
#     print(movie)
#     return movie

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

# from rapidfuzz import process  # better than fuzzywuzzy (faster, safer)

# async def lazydeveloperr_spell_check(wrong_name, msg):
#     def search_movie(wrong_name):
#         search_results = imdb.search_movie(wrong_name)
#         # remove duplicates by converting to set
#         movie_list = list({movie['title'] for movie in search_results})
#         return movie_list

#     user_id = msg.from_user.id
#     movie_list = await asyncio.to_thread(search_movie, wrong_name)  # run in thread to avoid blocking
    
#     if not movie_list:
#         return None

#     # Pick the best match only once
#     closest_match = process.extractOne(wrong_name, movie_list, score_cutoff=70)  
#     # lowered to 70 → more tolerance, still safe

#     if not closest_match:
#         return None

#     movie = closest_match[0]
#     print(f"✨ Spell-corrected '{wrong_name}' → '{movie}'")
#     return movie

# async def lazydeveloperr_spell_check(wrong_name, msg):
#     async def search_movie(wrong_name):
#         search_results = imdb.search_movie(wrong_name)
#         movie_list = [movie['title'] for movie in search_results]
#         return movie_list
#     movie_list = await search_movie(wrong_name)
#     if not movie_list:
#         return
#     for _ in range(5):
#         closest_match = process.extractOne(wrong_name, movie_list)
#         if not closest_match or closest_match[1] <= 80:
#             return 
#         movie = closest_match[0]
#         lazy_id = msg.id
#         files, offset, total_results = await get_search_results_badAss_LazyDeveloperr(msg.from_user.id, lazy_id, movie)
#         if files:
#             return movie
#         movie_list.remove(movie)
#     return


# async def get_search_results_badAss_LazyDeveloperr(user_id, lazy_id, query, max_results=10, offset=0):

#     files = []
#     try:
#         sessionstring = await db.get_session(OWNER_ID)
#         if not sessionstring:
#             return [], "", 0

#         Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
#         if not Lazyuserbot.is_connected():
#             await Lazyuserbot.start()

#         async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=query):
#             if search_msg.text:
#                 # Extract URL from first line
#                 match = re.match(r"(https?://[^\s]+)", search_msg.text)
#                 if match:
#                     target_url = match.group(1).strip()

#                     # Extract movie name from text in parentheses
#                     movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
#                     movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"

#                     files.append((movie_name, target_url))

#         total_results = len(files)
#         next_offset = offset + max_results
#         if next_offset >= total_results:
#             next_offset = ""

#         # Slice results for pagination
#         files = files[offset:offset + max_results]

#         return files, next_offset, total_results

#     except Exception as e:
#         print(f"Error in get_search_results_badAss_LazyDeveloperr: {e}")
#         return [], "", 0

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================





# ====================== WEBSITE SEARCH API ======================
# Reuses the same Telegram user-session + DB_CHANNEL search source
# used by the Telegram bot. This is intentionally separate from the
# Telegram message handler so existing bot behaviour remains intact.

async def search_links_for_web(raw_query, offset=0, limit=10):
    queryz = await validate_query(raw_query)
    if not queryz:
        return [], 0

    queryz = queryz.lower()
    find = queryz.split(" ")
    removes = [
        "in", "series", "full", "horror", "thriller", "mystery", "print", "file",
        "2k", "4k", "2004", "2024", "2025", "2020", "2021", "2022", "2023",
        "new", "movies", "the", "a", "an", "480", "480p", "720p", "720",
        "1080p", "1080", "hindi", "english", "eng", "hin", "kor", "korean"
    ]
    queryz = " ".join(x for x in find if x not in removes)
    queryz = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)",
        "", queryz, flags=re.IGNORECASE
    )
    queryz = re.sub(r"\s+", " ", queryz).strip().replace("-", " ").replace(":", "")
    if not queryz:
        return [], 0

    sessionstring = await db.get_session(OWNER_ID)
    if not sessionstring:
        raise RuntimeError("Telegram user session is not initialized")

    Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
    try:
        if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()

        all_results = []
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=queryz):
            if not search_msg.text:
                continue
            match = re.match(r"(https?://[^\s]+)", search_msg.text)
            if not match:
                continue
            target_url = match.group(1).strip()
            movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
            movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
            all_results.append({"movie_name": movie_name, "target_url": target_url})

        # Keep the same fuzzy-spelling fallback used by the Telegram bot.
        if not all_results:
            # Reuse the existing helper, but only if it can find a real Telegram result.
            class WebMessage:
                id = 0
                class User:
                    id = 0
                from_user = User()
            corrected = await lazydeveloperr_spell_check(queryz, WebMessage())
            if corrected and corrected.lower() != queryz.lower():
                async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, search=corrected):
                    if not search_msg.text:
                        continue
                    match = re.match(r"(https?://[^\s]+)", search_msg.text)
                    if not match:
                        continue
                    target_url = match.group(1).strip()
                    movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
                    movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
                    all_results.append({"movie_name": movie_name, "target_url": target_url})

        total = len(all_results)
        page = all_results[offset:offset + limit]
        return page, total
    finally:
        if Lazyuserbot.is_connected():
            await Lazyuserbot.disconnect()


# ====================== KS MOVIES WEBSITE LATEST ======================

async def get_latest_links_for_web(limit=12):
    """Return newest Telegram DB entries. Telegram DB remains source of truth."""
    sessionstring = await db.get_session(OWNER_ID)
    if not sessionstring:
        raise RuntimeError("Telegram user session is not initialized")

    Lazyuserbot = TelegramClient(StringSession(sessionstring), API_ID, API_HASH)
    try:
        if not Lazyuserbot.is_connected():
            await Lazyuserbot.start()

        results = []
        async for search_msg in Lazyuserbot.iter_messages(DB_CHANNEL, limit=max(20, limit * 3)):
            if not search_msg.text:
                continue
            match = re.match(r"(https?://[^\s]+)", search_msg.text)
            if not match:
                continue
            target_url = match.group(1).strip()
            movie_name_match = re.search(r"\(([^)]+)\)", search_msg.text)
            movie_name = movie_name_match.group(1).strip() if movie_name_match else "Missing title 😂"
            results.append({
                "movie_name": movie_name,
                "target_url": target_url,
            })
            if len(results) >= limit:
                break
        return results
    finally:
        if Lazyuserbot.is_connected():
            await Lazyuserbot.disconnect()
