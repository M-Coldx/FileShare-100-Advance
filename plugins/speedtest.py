import os
import speedtest
import requests
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS

@Bot.on_message(filters.command("speedtest") & filters.user(ADMINS))
async def run_speedtest(client: Bot, message: Message):
    m = await message.reply_text("⚡️ Memulai speedtest server...")
    
    try:
        # Initialize speedtest
        test = speedtest.Speedtest()
        await m.edit("🔍 Mencari server terbaik...")
        test.get_best_server()
        
        # Test download speed
        await m.edit("📥 Testing download speed...")
        download_speed = test.download() / 1024 / 1024  # Convert to Mbps
        
        # Test upload speed
        await m.edit("📤 Testing upload speed...")
        upload_speed = test.upload() / 1024 / 1024  # Convert to Mbps
        
        # Get results and share URL
        test.results.share()
        result = test.results.dict()
        
    except Exception as e:
        await m.edit(f"❌ <b>Error during speedtest:</b>\n<code>{str(e)}</code>")
        return
    
    await m.edit("📊 Generating speedtest image...")
    
    path = None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(result["share"], headers=headers, timeout=30)
        response.raise_for_status()
        
        path = "speedtest_result.png"
        with open(path, "wb") as file:
            file.write(response.content)
            
    except requests.exceptions.RequestException as req_err:
        # If image download fails, just show text results
        path = None
        
    # Format results
    output = f"""🚀 <b>SpeedTest Results</b>

👤 <b>Client Info:</b>
• <b>ISP:</b> <code>{result['client']['isp']}</code>
• <b>Country:</b> <code>{result['client']['country']}</code>

🖥 <b>Server Info:</b>
• <b>Name:</b> <code>{result['server']['name']}</code>
• <b>Location:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
• <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>

📊 <b>Speed Results:</b>
• <b>Ping:</b> <code>{result['ping']:.2f} ms</code>
• <b>Download:</b> <code>{download_speed:.2f} Mbps</code>
• <b>Upload:</b> <code>{upload_speed:.2f} Mbps</code>

🔗 <b>Results URL:</b> <a href="{result['share']}">View Online</a>"""

    try:
        if path and os.path.exists(path):
            await client.send_photo(
                chat_id=message.chat.id, 
                photo=path, 
                caption=output,
                reply_to_message_id=message.id
            )
            os.remove(path)
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=output,
                reply_to_message_id=message.id,
                disable_web_page_preview=True
            )
        await m.delete()
        
    except Exception as e:
        await m.edit(f"✅ <b>Speedtest completed but failed to send image:</b>\n\n{output}")
        if path and os.path.exists(path):
            os.remove(path)
