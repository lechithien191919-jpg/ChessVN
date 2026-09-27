import os
import discord
from discord.ext import commands
import google.generativeai as genai
from openai import OpenAI

# Cấu hình API Keys (Ông thay chuỗi trong ngoặc thành key thật của ông nha)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"       # Dùng cho ChatGPT
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"   # Dùng chung chuẩn OpenAI cho DeepSeek

# Khởi tạo Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Khởi tạo OpenAI (ChatGPT)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Khởi tạo DeepSeek (Dùng base_url của DeepSeek nhưng xài chung thư viện openai cho gọn)
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Cấu hình Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập thành công với tên: {bot.user}')

@bot.command(name="ai")
async def chat_with_all(ctx, *, prompt: str):
    """Lệnh gọi tất cả AI cùng trả lời một câu hỏi: !ai <câu hỏi>"""
    await ctx.send(f"🤖 **Câu hỏi từ {ctx.author.mention}:** *{prompt}*\nĐang gọi các AI vào bàn tròn...")

    # 1. Gọi Gemini
    try:
        gemini_res = gemini_model.generate_content(prompt)
        gemini_text = gemini_res.text
    except Exception as e:
        gemini_text = f"Lỗi Gemini: {e}"

    # 2. Gọi ChatGPT
    try:
        chatgpt_res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        chatgpt_text = chatgpt_res.choices[0].message.content
    except Exception as e:
        chatgpt_text = f"Lỗi ChatGPT: {e}"

    # 3. Gọi DeepSeek
    try:
        deepseek_res = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        deepseek_text = deepseek_res.choices[0].message.content
    except Exception as e:
        deepseek_text = f"Lỗi DeepSeek: {e}"

    # Gửi kết quả lên các khung chat Discord tương ứng hoặc gom chung
    await ctx.send(f"✨ **Gemini:**\n{gemini_text[:1900]}")
    await ctx.send(f"🟢 **ChatGPT:**\n{chatgpt_text[:1900]}")
    await ctx.send(f"🔵 **DeepSeek:**\n{deepseek_text[:1900]}")

# Chạy bot (Thay token Discord của ông vào đây)
bot.run("YOUR_DISCORD_BOT_TOKEN")
      
