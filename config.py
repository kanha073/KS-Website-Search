
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = int(os.environ.get("API_ID", "0"))

API_HASH = os.environ.get("API_HASH", "")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

DB_NAME = os.environ.get("DB_NAME","xxx")     

DB_URL = os.environ.get("DB_URL","xxx")

FLOOD = int(os.environ.get("FLOOD", "10"))
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "100"))

# FOR SESSION LOGIN - ONLY OWNER CAN LOGIN 
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/nr6nqC4/IMG-20241030-153858-361.jpg")

# CAN HAVE MULTIPLE ADMINS
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]

PORT = os.environ.get("PORT", "8080")
BOT_SESSION_NAME = os.environ.get("BOT_SESSION_NAME", "Lazydeveloper")
MAX_BTN = int(os.environ.get("MAX_BTN", "5"))

DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "0"))

SELF_DELETE_SECONDS = int(os.environ.get("SELF_DELETE_SECONDS", "300"))
# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================


# ====================== KS MOVIES WEBSITE / TMDB ======================
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "").strip()
TMDB_ACCESS_TOKEN = os.environ.get("TMDB_ACCESS_TOKEN", "").strip()
TMDB_LANGUAGE = os.environ.get("TMDB_LANGUAGE", "en-IN").strip()
TMDB_REGION = os.environ.get("TMDB_REGION", "IN").strip().upper()
TMDB_CACHE_TTL = int(os.environ.get("TMDB_CACHE_TTL", "21600"))
