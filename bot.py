import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from PIL import Image

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "📄 PDF Utility Bot\n\n"
        "Send me a PHOTO and I will convert it to PDF."
    )

@dp.message(F.photo)
async def image_to_pdf(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    img_path = f"{TEMP_DIR}/{message.from_user.id}.jpg"
    pdf_path = f"{TEMP_DIR}/{message.from_user.id}.pdf"

    await bot.download_file(file.file_path, img_path)

    img = Image.open(img_path).convert("RGB")
    img.save(pdf_path)

    await message.answer_document(open(pdf_path, "rb"))

    os.remove(img_path)
    os.remove(pdf_path)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
