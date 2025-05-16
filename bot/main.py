import asyncio
import logging
import sys
import textwrap

from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
    
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer_photo(caption=f"Hello, {html.bold(message.from_user.full_name)}! I am reminder bot. Use /help for get info about commands.", 
                               photo="https://southpark.fandom.com/wiki/A.W.E.S.O.M.-O_4000")

@dp.message(Command("help"))
async def help(message: Message) -> None:
    help_text= textwrap.dedent(f"""
        <b>ℹ️About bot</b>
        <i>bot reminds the user of something</i>
                               
        <b>💻Bot commands</b>
        /start - <i>welcomes the user</i>
        /help - <i>bot commands</i>
        /remind &lt;minutes&gt; &lt;text&gt; - <i>set up remind</i>""")
    await message.answer(text=help_text, parse_mode=ParseMode.HTML)
    

@dp.message(Command("remind"))
async def remind(message: Message) -> None:
    try:
        parts = message.text.split(maxsplit=2)
        minutes = int(parts[1])
        text = parts[2]
        await asyncio.sleep(minutes * 60)
        remind_text = textwrap.dedent(f"""
            <b>🔔Remind</b>
            
            🕒Time elapsed: <i>{str(minutes)} minutes</i>
            📌Reminder: <i>{text}</i>""")
        await message.answer(text=remind_text, parse_mode=ParseMode.HTML,)
    except Exception as e:
        await message.answer(text="Invalid format! Use: /remind <minutes> <text>", parse_mode=None)

@dp.message()
async def message_wo_com(message: Message) -> None:
    await message.answer(text="Don't get what you write. Use /help for information")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
