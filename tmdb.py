
import asyncio
import re
import time
from urllib.parse import urlencode

import aiohttp
from rapidfuzz.fuzz import ratio, WRatio

from config import (
    TMDB_API_KEY, TMDB_ACCESS_TOKEN, TMDB_LANGUAGE,
    TMDB_REGION, TMDB_CACHE_TTL
)

BASE = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p"
_cache = {}
_lock = asyncio.Lock()

def tmdb_enabled():
    return bool(TMDB_ACCESS_TOKEN or TMDB_API_KEY)

def _norm(s):
    s = (s or "").lower()
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"[^a-z0-9\u0900-\u097f\u0c00-\u0c7f]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def _year(s):
    m = re.search(r"\b((?:19|20)\d{2})\b", s or "")
    return int(m.group(1)) if m else None

def _queries(title):
    title = re.sub(r"\s+", " ", (title or "")).strip()
    # Telegram entries often contain an alias in parentheses:
    # "KGF: Chapter 1(KGF)" -> search "KGF: Chapter 1" first.
    main = re.split(r"\s*\(", title, maxsplit=1)[0].strip()
    vals = []
    for q in (main, title):
        q = re.sub(r"\b(480p?|720p?|1080p?|2160p?|4k|hd|full\s*movie|dual\s*audio)\b", " ", q, flags=re.I)
        q = re.sub(r"\s+", " ", q).strip(" -_")
        if q and q not in vals:
            vals.append(q)
    return vals[:2]

async def _get(path, params=None):
    if not tmdb_enabled():
        return None
    params = dict(params or {})
    headers = {"accept": "application/json"}
    if TMDB_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {TMDB_ACCESS_TOKEN}"
    else:
        params["api_key"] = TMDB_API_KEY

    key = path + "?" + urlencode(sorted(params.items()))
    now = time.time()
    cached = _cache.get(key)
    if cached and cached[0] > now:
        return cached[1]

    timeout = aiohttp.ClientTimeout(total=8)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(BASE + path, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"TMDB HTTP {resp.status}: {text[:200]}")
            data = await resp.json()

    _cache[key] = (now + TMDB_CACHE_TTL, data)
    return data

async def _search(kind, query, year=None):
    params = {
        "query": query,
        "language": TMDB_LANGUAGE,
        "include_adult": "false",
        "page": 1,
    }
    if kind == "movie" and year:
        params["year"] = year
    if kind == "tv" and year:
        params["first_air_date_year"] = year
    data = await _get(f"/search/{kind}", params)
    return (data or {}).get("results", [])[:8]

def _candidate_score(source_title, item, kind):
    target = _norm(source_title)
    name = item.get("title") if kind == "movie" else item.get("name")
    original = item.get("original_title") if kind == "movie" else item.get("original_name")
    names = [_norm(name), _norm(original)]
    names = [x for x in names if x]
    score = max([WRatio(target, x) for x in names] or [0])

    # Prefer the part before an alias/quality marker when comparing.
    main = _norm(re.split(r"\s*\(", source_title, maxsplit=1)[0])
    if main:
        score = max(score, max([WRatio(main, x) for x in names] or [0]))

    sy = _year(source_title)
    date = item.get("release_date") if kind == "movie" else item.get("first_air_date")
    if sy and date and str(date)[:4].isdigit():
        if int(str(date)[:4]) == sy:
            score += 8
        else:
            score -= 8
    return score

def _format_item(kind, item, details):
    name = details.get("title") if kind == "movie" else details.get("name")
    date = details.get("release_date") if kind == "movie" else details.get("first_air_date")
    genres = [g.get("name") for g in details.get("genres", []) if g.get("name")]
    credits = details.get("credits", {})
    cast = [p.get("name") for p in credits.get("cast", [])[:8] if p.get("name")]
    crew = credits.get("crew", [])
    directors = [p.get("name") for p in crew if p.get("job") == "Director"][:3]
    if not directors and kind == "tv":
        directors = [p.get("name") for p in crew if p.get("job") in ("Director", "Creator")][:3]

    poster = details.get("poster_path") or item.get("poster_path")
    backdrop = details.get("backdrop_path") or item.get("backdrop_path")

    return {
        "id": details.get("id"),
        "media_type": kind,
        "title": name or item.get("title") or item.get("name") or "",
        "year": str(date)[:4] if date else "",
        "release_date": date or "",
        "rating": round(float(details.get("vote_average") or item.get("vote_average") or 0), 1),
        "genres": genres,
        "overview": details.get("overview") or item.get("overview") or "",
        "poster": f"{IMG}/w500{poster}" if poster else "",
        "backdrop": f"{IMG}/w780{backdrop}" if backdrop else "",
        "cast": cast,
        "director": directors,
        "runtime": (
            details.get("runtime") if kind == "movie"
            else (details.get("episode_run_time") or [None])[0]
        ),
        "tmdb_url": f"https://www.themoviedb.org/{'movie' if kind == 'movie' else 'tv'}/{details.get('id')}",
    }

async def lookup_title(source_title):
    if not tmdb_enabled():
        return None

    cache_key = "title:" + (source_title or "").strip().lower()
    now = time.time()
    cached = _cache.get(cache_key)
    if cached and cached[0] > now:
        return cached[1]

    year = _year(source_title)
    best = None

    try:
        for q in _queries(source_title):
            # Movie and TV are both searched, but Telegram entries remain the
            # source of truth for links/results.
            movie_results, tv_results = await asyncio.gather(
                _search("movie", q, year),
                _search("tv", q, year),
            )
            for kind, items in (("movie", movie_results), ("tv", tv_results)):
                for item in items:
                    score = _candidate_score(source_title, item, kind)
                    if best is None or score > best[0]:
                        best = (score, kind, item)
            if best and best[0] >= 94:
                break

        if not best or best[0] < 55:
            result = None
        else:
            score, kind, item = best
            details = await _get(
                f"/{kind}/{item.get('id')}",
                {
                    "language": TMDB_LANGUAGE,
                    "append_to_response": "credits",
                },
            )
            result = _format_item(kind, item, details or item)
            result["match_score"] = round(score)

    except Exception as exc:
        print(f"TMDB lookup failed for {source_title!r}: {exc}")
        result = None

    _cache[cache_key] = (now + TMDB_CACHE_TTL, result)
    return result

async def enrich_results(results):
    if not results:
        return []
    # Keep each Telegram result. Never deduplicate by TMDB id.
    sem = asyncio.Semaphore(5)
    async def one(x):
        async with sem:
            info = await lookup_title(x.get("movie_name", ""))
            y = dict(x)
            y["tmdb"] = info
            return y
    return await asyncio.gather(*(one(x) for x in results))

async def trending(limit=12):
    if not tmdb_enabled():
        return []
    try:
        data = await _get(
            "/trending/movie/day",
            {"language": TMDB_LANGUAGE},
        )
        out = []
        for item in (data or {}).get("results", [])[:limit]:
            date = item.get("release_date") or ""
            poster = item.get("poster_path")
            backdrop = item.get("backdrop_path")
            out.append({
                "id": item.get("id"),
                "media_type": "movie",
                "title": item.get("title", ""),
                "year": date[:4] if date else "",
                "rating": round(float(item.get("vote_average") or 0), 1),
                "overview": item.get("overview", ""),
                "poster": f"{IMG}/w500{poster}" if poster else "",
                "backdrop": f"{IMG}/w780{backdrop}" if backdrop else "",
                "tmdb_url": f"https://www.themoviedb.org/movie/{item.get('id')}",
            })
        return out
    except Exception as exc:
        print(f"TMDB trending failed: {exc}")
        return []
