
from aiohttp import web
import os

routes = web.RouteTableDef()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

INDEX_HTML_PATH = os.path.join(BASE_DIR, "website", "index.html")

def get_index_html():
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text=get_index_html(), content_type="text/html")

@routes.get("/assets/{name}", allow_head=True)
async def asset_handler(request):
    name = request.match_info["name"]
    if name not in {"hero.png", "logo.png"}:
        raise web.HTTPNotFound()
    return web.FileResponse(os.path.join(ASSET_DIR, name))

@routes.get("/api/health")
async def health_handler(request):
    from tmdb import tmdb_enabled
    return web.json_response({"ok": True, "service": "ks-movies", "tmdb_enabled": tmdb_enabled()})

@routes.get("/api/search")
async def search_handler(request):
    query=(request.query.get("q") or "").strip()
    try:
        offset=max(0,int(request.query.get("offset","0")));limit=min(20,max(1,int(request.query.get("limit","10"))))
    except ValueError:
        return web.json_response({"error":"Invalid pagination."},status=400)
    if not query:return web.json_response({"error":"Search query is required."},status=400)
    if len(query)>120:return web.json_response({"error":"Search query is too long."},status=400)
    try:
        from plugins.detect_lazysms import search_links_for_web
        from tmdb import enrich_results,tmdb_enabled
        results,total=await search_links_for_web(query,offset=offset,limit=limit)
        results=await enrich_results(results)
        return web.json_response({"ok":True,"query":query,"results":results,"offset":offset,"limit":limit,"total":total,"tmdb_enabled":tmdb_enabled()})
    except Exception as exc:
        print(f"Web search error: {exc}")
        return web.json_response({"error":"Search is temporarily unavailable."},status=503)

@routes.get("/api/home")
async def home_handler(request):
    try:
        from plugins.detect_lazysms import get_latest_links_for_web
        from tmdb import enrich_results,trending,tmdb_enabled
        latest=await get_latest_links_for_web(limit=12);latest=await enrich_results(latest);trend=await trending(limit=12)
        return web.json_response({"ok":True,"latest":latest,"trending":trend,"tmdb_enabled":tmdb_enabled()})
    except Exception as exc:
        print(f"Home API error: {exc}")
        return web.json_response({"error":"Home data is temporarily unavailable."},status=503)

async def web_server():
    web_app=web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
