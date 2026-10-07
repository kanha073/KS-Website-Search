import motor.motor_asyncio
from config import DB_URL, DB_NAME

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.settings_col = self.db.settings  # New collection for settings like skip_msg_id
        self.forwarded_col = self.db.forwarded_messages  # New collection for forwarded IDs
        self.admins = self.db.admins  # New collection for forwarded IDs
        self.movie_col = self.db.movies  # New collection for movies

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    def new_movie(self, title, link):
        return {
            "title": title,
            "link": link
        }

    async def add_movie(self, title, link):
        movie = self.new_movie(title, link)
        await self.movie_col.insert_one(movie)

    async def search_movies(self, query, offset=0, limit=10):
        results = self.movie_col.find(
            {"title": {"$regex": query, "$options": "i"}}
        ).skip(offset).limit(limit)
        return await results.to_list(length=limit)

    async def total_movies_count(self):
        return await self.movie_col.count_documents({})

# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================

    # session
    async def set_session(self, id, session_string):
        print(session_string)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_session_string': session_string}})
        print(z)

    async def get_session(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_session_string', None)
    
db = Database(DB_URL, DB_NAME)


# ====================== 💘❤👩‍💻====================================
#    ==> P O W E R E D - B Y - 🤞 L A Z Y D E V E L O P E  R        |
# ==================================================================
