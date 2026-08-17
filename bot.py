import os
import discord
from discord.ext import commands
from datetime import datetime, timezone
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Настройка выпадающего меню ---
class RulesSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="[ОБЩИЕ ПРАВИЛА]", description="Главные правила и понятия сервера", value="general"),
            discord.SelectOption(label="[ВНУТРИИГРОВЫЕ]", description="Правила поведения в игре и РП-процесса", value="ingame"),
            discord.SelectOption(label="[ПРАВИЛА ДИСКОРДА]", description="Правила общения в текстовых и голосовых чатах", value="discord")
        ]
        super().__init__(
            placeholder="Выберите категорию правил...",
            min_values=1, max_values=1, options=options,
            custom_id="persistent_rules_select_dropdown" # custom_id делает меню вечным
        )

    async def callback(self, interaction: discord.Interaction):
        # ... (Твоя логика с текстами без изменений) ...
        text = "Тестовый текст" # Заглушка для примера
        
        if len(text) <= 2000:
            await interaction.response.send_message(text, ephemeral=True)
        else:
            # Если текст огромный, лучше отправлять его без ```text ```, 
            # иначе форматирование сломается при разделении на чанки.
            chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
            await interaction.response.send_message(chunks[0], ephemeral=True)
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk, ephemeral=True)

class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout=None обязателен для персистентных меню
        self.add_item(RulesSelect())

# ПРАВИЛЬНАЯ регистрация персистентных View (вызывается 1 раз при запуске)
async def setup_hook():
    bot.add_view(RulesView())
    print("Персистентные меню зарегистрированы в системе.")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"Бот {bot.user} успешно запущен и готов к работе!")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    content_text = (
        "***КДА*** *- это политический сервер с глубоким сюжетом, где историю мира пишут сами игроки.*\n\n"
        "~~Весь наш мир~~ - это огромное, **древнее Королевство.** Король распределил земли между своими вассалами, "
        "раздав им статус сюзеренов. __Ваша задача__ - с нуля поднять свой город...\n\n"
        "*Более подробно прочитать* - [можно прочитать тут](https://discord.com/channels/...)\n\n"
    )

    embed1 = discord.Embed(
        title="Правила",
        description="1. Никогда никому не рассказывать о Бойцовском клубе.\n2. Никогда никому не рассказывать о Бойцовском клубе.",
        color=0x42AD18
    )
    embed1.set_thumbnail(url="https://i.pinimg.com/originals/31/a7/2a/31a72afda250825d993400c3ef28c55c.gif")
    embed1.set_image(url="https://i.pinimg.com/originals/80/ec/77/80ec77932091113c4970a88f69b9bb4f.gif")
    embed1.set_footer(text="Постскриптум - идите траву потрогайте")
    embed1.timestamp = datetime(2026, 8, 12, 0, 0, tzinfo=timezone.utc) # Стало чище

    embed2 = discord.Embed(
        title="Администрация всегда права",
        description="Главные постулаты сервера:\n__Администрация права по определению.__",
        color=0x42AD18
    )
    embed2.set_image(url="https://i.pinimg.com/1200x/67/ee/87/67ee87b6ca37719fcbd52d6d5b6b555a.jpg")

    try:
        await ctx.send(content=content_text, embeds=[embed1, embed2], view=RulesView())
        await ctx.message.delete()
    except discord.Forbidden:
        await ctx.send("⚠️ Ошибка: у бота нет прав на отправку Embed-сообщений или удаление чужих сообщений в этом канале.")

# Обработчик ошибок, чтобы обычные юзеры видели адекватный ответ, а не тишину
@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ У тебя нет прав Администратора для настройки сервера!", delete_after=10)
        try:
            await ctx.message.delete()
        except:
            pass

# Безопасный запуск
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("ОШИБКА: Токен не найден! Создай файл .env и пропиши там DISCORD_TOKEN=...")
else:
    bot.run(TOKEN)
