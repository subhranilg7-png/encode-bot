# ===============================================================
#  🎬 VideoEncoder Bot
#
#  🚀 Advanced Encoder Bot
#  ⚡ Developed by Kunal
#  🛠 Maintained by Awakeners Bots
#
#  🔗 GitHub  : https://github.com/KunalG932
#  🔗 Telegram: https://t.me/Awakeners_Bots
#
#  ⚠️  Do not remove this credit header.
#  Unauthorized removal of credits is strictly prohibited.
#
#  © 2026 Kunal & Awakeners Bots. All Rights Reserved.
# ===============================================================

import os
import dns.resolver
from pyrogram import idle
from . import app
from .core.cfg import cfg
from .core.log import log
import time
import http.client
import email.utils
import asyncio
from aiohttp import web

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

def sync_bot_time():
    try:
        conn = http.client.HTTPConnection("google.com", timeout=5)
        conn.request("GET", "/")
        r = conn.getresponse()
        ts = r.getheader("date")
        if ts:
            remote_time = email.utils.mktime_tz(email.utils.parsedate_tz(ts))
            offset = int(remote_time - time.time())
            if abs(offset) > 2:
                log.inf("time_sync", offset=f"{offset}s", status="applied")
                return offset
    except Exception as e:
        log.err("time_sync_failed", error=str(e))
    return 0

async def start_web():
    async def health(request):
        return web.Response(text="OK")
    app_web = web.Application()
    app_web.router.add_get("/", health)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    log.inf("web_server", status="started", port=port)

async def main():
    await start_web()
    try:
        try:
            await app.start()
        except Exception as e:
            if "[16]" in str(e):
                offset = sync_bot_time()
                if hasattr(app, "session") and app.session:
                    app.session.offset = offset
                    log.inf("time_correction", status="applied", offset=f"{offset}s")
                    await app.start()
                else:
                    raise e
            else:
                raise e
        
        log.inf("bot", status="started", username=(await app.get_me()).username)
        
        if cfg.LOG_CHANNEL:
            await app.send_message(
                cfg.LOG_CHANNEL, 
                f"▸ <b>VideoEncoder</b>\nStatus: ● Online\nBot: @{(await app.get_me()).username}"
            )
            
        await idle()
    except Exception as e:
        import traceback
        traceback.print_exc()
        log.logger.exception(f"bot_fatal: {str(e)}")
    finally:
        if app.is_connected:
            await app.stop()
        log.inf("bot", status="stopped")

if __name__ == "__main__":
    app.loop.run_until_complete(main())

# ===============================================================
#  🎬 VideoEncoder Bot
#
#  🚀 Advanced Encoder Bot
#  ⚡ Developed by Kunal
#  🛠 Maintained by Awakeners Bots
#
#  🔗 GitHub  : https://github.com/KunalG932
#  🔗 Telegram: https://t.me/Awakeners_Bots
#
#  ⚠️  Do not remove this credit header.
#  Unauthorized removal of credits is strictly prohibited.
#
#  © 2026 Kunal & Awakeners Bots. All Rights Reserved.
# ===============================================================
