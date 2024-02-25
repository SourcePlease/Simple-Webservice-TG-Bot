from aiohttp import web
from pyrogram import Client, filters
import asyncio
import psutil
from time import time

bot_token, api_id, api_hash = "6364824731:AAHV6xX75aVZAaJdekT-OECFKskF5qDImb4", "27486644", "149f309eb1c416c8edac85bba6c5eec2"
app = Client("bot", bot_token=bot_token, api_id=api_id, api_hash=api_hash)

botStartTime = time()

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return f"{int(d)}d {int(h)}h {int(m)}m {int(s)}s"

async def get_stats():
    sys_uptime = format_time(time() - psutil.boot_time())
    bot_uptime = format_time(time() - botStartTime)
    
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    p_cores = psutil.cpu_count(logical=False)
    v_cores = cpu_count - p_cores
    cpu_frequency = psutil.cpu_freq(percpu=False).current
    
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_in_use_gb = ram.used / (1024 ** 3)
    ram_total_gb = ram.total / (1024 ** 3)
    ram_free_gb = ram.free / (1024 ** 3)
    
    swap = psutil.swap_memory()
    swap_percent = swap.percent
    swap_in_use_gb = swap.used / (1024 ** 3)
    swap_total_gb = swap.total / (1024 ** 3)
    swap_free_gb = swap.free / (1024 ** 3)
    
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_in_use_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)
    disk_free_gb = disk.free / (1024 ** 3)
    
    ul = psutil.net_io_counters().bytes_sent / (1024 ** 2)
    dl = psutil.net_io_counters().bytes_recv / (1024 ** 2)
    
    stats = f"**Bot Statistics**\n\n" \
            f"**System Uptime:** {sys_uptime}\n" \
            f"**Bot Uptime:** {bot_uptime}\n\n" \
            f"**CPU:** [{'⬢' * int(cpu_percent / 10)}{'⬡' * (10 - int(cpu_percent / 10))}] {cpu_percent:.1f}%\n" \
            f"**CPU Total Core(s):** {cpu_count}\n" \
            f"**P-Core(s):** {p_cores} | **V-Core(s):** {v_cores}\n" \
            f"**Frequency:** {cpu_frequency:.3f} Mhz\n\n" \
            f"**RAM:** [{'⬢' * int(ram_percent / 10)}{'⬡' * (10 - int(ram_percent / 10))}] {ram_percent:.1f}%\n" \
            f"**RAM In Use:** {ram_in_use_gb:.2f} GB [{ram_percent:.1f}%]\n" \
            f"**Total:** {ram_total_gb:.2f} GB | **Free:** {ram_free_gb:.2f} GB\n\n" \
            f"**SWAP:** [{'⬢' * int(swap_percent / 10)}{'⬡' * (10 - int(swap_percent / 10))}] {swap_percent:.1f}%\n" \
            f"**SWAP In Use:** {swap_in_use_gb:.2f} GB [{swap_percent:.1f}%]\n" \
            f"**Allocated:** {swap_total_gb:.2f} GB | **Free:** {swap_free_gb:.2f} GB\n\n" \
            f"**DISK:** [{'⬢' * int(disk_percent / 10)}{'⬡' * (10 - int(disk_percent / 10))}] {disk_percent:.1f}%\n" \
            f"**Drive In Use:** {disk_in_use_gb:.2f} GB [{disk_percent:.1f}%]\n" \
            f"**Total:** {disk_total_gb:.2f} GB | **Free:** {disk_free_gb:.2f} GB\n\n" \
            f"**UL:** {ul:.2f} MB | **DL:** {dl:.2f} MB"
    
    return stats

@app.on_message(filters.command(["stats"]))
async def stats_command(_, message):
    stats = await get_stats()
    await app.send_message(chat_id=message.chat.id, text=stats)

routes = web.RouteTableDef()

@routes.post("/webhook")
async def webhook_handler(request):
    await app.process_updates(request.body.decode("utf-8"))
    return web.Response(text="OK")

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("Bot is Running")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def main():
    await app.start()
    runner = web.AppRunner(await web_server())
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
