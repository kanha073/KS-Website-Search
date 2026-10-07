# KS Movies — Fully Updated

This build keeps the existing Telegram bot and its DB search source, and adds the KS Movies website to the same Koyeb process.

## What changed

- Mobile-first KS Movies website with exactly 3 visible sections:
  1. Search
  2. New Updates
  3. Trending Today
- Website is served by the existing aiohttp server, so browser search uses same-origin `/api/search` and does not depend on CORS.
- Search results always come from the Telegram `DB_CHANNEL`.
- Every Telegram result is preserved independently.
- TMDB is used only to enrich each Telegram result with poster/details.
- Example:
  - `KGF: Chapter 1(KGF)` -> its own Telegram URL + TMDB Chapter 1 metadata
  - `KGF: Chapter 2(KGF 2)` -> its own Telegram URL + TMDB Chapter 2 metadata
- TMDB matching does NOT replace, merge, or limit Telegram results.
- Movie details modal includes poster, backdrop, rating, year, runtime, genres, overview and cast.
- New Updates comes from the newest entries in the Telegram DB.
- Trending Today comes from TMDB daily movie trending.
- TMDB data is cached in memory to reduce repeated API calls.
- Existing Telegram bot handlers are left in place.

## Koyeb environment variables

Keep your existing Telegram/Mongo environment variables:

- API_ID
- API_HASH
- BOT_TOKEN
- DB_NAME
- DB_URL
- OWNER_ID
- ADMIN
- PORT
- BOT_SESSION_NAME
- MAX_BTN
- DB_CHANNEL
- SELF_DELETE_SECONDS
- FLOOD
- AUTO_DELETE_TIME
- START_PIC

Add:

- TMDB_API_KEY = your TMDB v3 API key
  OR
- TMDB_ACCESS_TOKEN = your TMDB API Read Access Token

Optional:

- TMDB_LANGUAGE=en-IN
- TMDB_REGION=IN
- TMDB_CACHE_TTL=21600

Do not put Telegram credentials or the TMDB secret in GitHub.

## Important

TMDB is free for non-commercial use when its attribution requirements are followed. If the site is used commercially/revenue-generating, obtain the appropriate TMDB commercial license. See TMDB's official API FAQ.

The site includes the required attribution notice in the footer area.

## Run

```bash
python3 bot.py
```

The same process serves:

- `/`
- `/api/health`
- `/api/search?q=KGF`
- `/api/home`

No second bot is created.
