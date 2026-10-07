
# ====================== bot.py ====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

import logging
import logging.config
from pyrogram import Client , idle
from config import API_ID, API_HASH, BOT_TOKEN, PORT
from aiohttp import web
from plugins.web_support import web_server

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="serveruploader",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            max_concurrent_transmissions=100
        )

    async def start(self):
       await super().start()
       me = await self.get_me()
       self.mention = me.mention
       self.username = me.username 
       app = web.AppRunner(await web_server())
       await app.setup()
       bind_address = "0.0.0.0"
       await web.TCPSite(app, bind_address, PORT).start()
       logging.info(f"{me.first_name} ✅✅ BOT started successfully - ✅✅")
       print(f"""
 _____________________________________________   
|                                             |  
|          Deployed Successfully              |  
|       🧩 with ❤ @LazyDeveloper 🤞          |
|_____________________________________________|
    """)
       await idle()

    async def stop(self, *args):
      await super().stop()      
      logging.info("Bot Stopped 🙄 - \nContact @LazyDeveloper on telegram for any query")
        
bot = Bot()
bot.run()

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
