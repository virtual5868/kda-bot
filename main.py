import datetime
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Настройка выпадающего меню ---
class RulesSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="[ОБЩИЕ ПРАВИЛА]",
                description="Главные правила и понятия сервера",
                value="general"
            ),
            discord.SelectOption(
                label="[ВНУТРИИГРОВЫЕ]",
                description="Правила поведения в игре и РП-процесса",
                value="ingame"
            ),
            discord.SelectOption(
                label="[ПРАВИЛА ДИСКОРДА]",
                description="Правила общения в текстовых и голосовых чатах",
                value="discord"
            )
        ]
        super().__init__(
            placeholder="Выберите категорию правил...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_rules_select_dropdown"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "general":
            text = (
                "```text\n"
                "=== ОБЩИЕ ПРАВИЛА ===\n\n"
                "1.1 Администрация оставляет за собой право принимать окончательные решения.\n"
                "1.2 Запрещена продажа игровых ценностей за реальные деньги.\n"
                "1.3 Незнание правил не освобождает от ответственности.\n"
                "```"
            )
        elif self.values[0] == "ingame":
            text = (
                "```text\n"
                "=== ВНУТРИИГРОВЫЕ ПРАВИЛА ===\n\n"
                "2.1 Запрещено использование стороннего софта, читов и багов.\n"
                "2.2 Соблюдайте лор и правила ролевого процесса.\n"
                "2.3 Бессмысленное вредительство и гриферство запрещены.\n"
                "```"
            )
        elif self.values[0] == "discord":
            text = (
                "```text\n"
                "=== ПРАВИЛА ДИСКОРДА ===\n\n"
                "3.1 Запрещен спам, флуд и чрезмерный капс в чатах.\n"
                "3.2 Соблюдайте порядок в голосовых каналах.\n"
                "3.3 Запрещена несогласованная реклама сторонних ресурсов.\n"
                "```"
            )
        else:
            text = "Информация не найдена."

        if len(text) <= 2000:
            await interaction.response.send_message(text, ephemeral=True)
        else:
            chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
            await interaction.response.send_message(chunks[0], ephemeral=True)
            for chunk in chunks[1:]:
                await interaction.followup.send(chunk, ephemeral=True)

class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RulesSelect())

@bot.event
async def on_ready():
    bot.add_view(RulesView())
    print(f"Бот {bot.user} успешно запущен!")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    # 1. Обычный текст перед эмбедами
    content_text = (
        "***КДА*** *- это политический сервер с глубоким сюжетом, где историю мира пишут сами игроки.*\n\n"
        "~~Весь наш мир~~ - это огромное, **древнее Королевство.** Король распределил земли между своими вассалами, "
        "раздав им статус сюзеренов. __Ваша задача__ - с нуля поднять свой город, развивать архитектуру, учитывая климат "
        "и ресурсы биома, и превратить скромное поселение в неприступную столицу региона.\n\n"
        "`Бла Бла Бла`\n\n"
        "*Более подробно прочитать* - [можно прочитать туту](https://discord.com/channels/1505574035034079252/1505577544282411078)\n\n"
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    # 2. Первое окно (Embed 1 — Правила)
    embed1 = discord.Embed(
        title="Правила",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description=(
            "1.Никогда никому не рассказывать о Бойцовском клубе.\n"
            "2.Никогда никому не рассказывать о Бойцовском клубе.\n"
            "3.Если противник потерял сознание или сдался, бой окончен."
        ),
        color=0x42AD18
    )
    embed1.add_field(name="ыыыыы", value="Гера лох", inline=False)
    embed1.set_thumbnail(url="https://i.pinimg.com/originals/31/a7/2a/31a72afda250825d993400c3ef28c55c.gif")
    embed1.set_image(url="https://i.pinimg.com/originals/80/ec/77/80ec77932091113c4970a88f69b9bb4f.gif")
    
    # Дата 12/08/2026 как на скриншоте
    embed1.set_footer(text="Постскриптум - идите траву потрогайте")
    embed1.timestamp = datetime.datetime(2026, 8, 12, 0, 0, tzinfo=datetime.timezone.utc)

    # 3. Второе окно (Embed 2 — Администрация всегда права)
    embed2 = discord.Embed(
        title="Администрация всегда права",
        description=(
            "*Если вы не согласны с действиями, решениями или мнением администрации, к вам применяются следующие дисциплинарные меры и последствия:*\n\n"
            "**Предупреждение (Варн)** — за попытку оспорить решение, сомнения в непогрешимости админа или легкое несогласие.\n\n"
            "**Блокировка (Бан)** — за активный спор, пререкания, бунт или повторное проявление несогласия.\n\n"
            "**Деанонимизация (Докс)** — за упорное нежелание признавать правоту администрации, критику правил и попытки развести токсичность.\n\n"
            "**Полный тотальный деструктив (Хуекс)** — за финальную стадию несогласия, когда простые меры уже не помогают.\n\n"
            "***Главные постулаты сервера:***\n\n"
            "__Администрация права по определению.__\n"
            "Если вам кажется, что администрация не права — см. Пункт 1.\n"
            "Любое решение админа обжалованию не подлежит.\n"
            "Попытка доказать свою правоту приравнивается к добровольному отказу от пребывания на сервере."
        ),
        color=0x42AD18
    )
    embed2.set_image(url="https://i.pinimg.com/1200x/67/ee/87/67ee87b6ca37719fcbd52d6d5b6b555a.jpg")

    try:
        # Отправляем текст + 2 эмбеда + меню
        await ctx.send(content=content_text, embeds=[embed1, embed2], view=RulesView())
        await ctx.message.delete()
    except discord.Forbidden:
        await ctx.send("Ошибка: у бота нет прав на отправку сообщений или управление сообщениями в этом канале.")

bot.run("MTUzODg0ODE0MTc3MDYyNTE2Nw.GMQwmg.PWfMnbToS0b3iz2GFcs7mIdGKZ9mheglV1s-yY")
