<<<<<<< HEAD
from keyboards import get_back_keyboard

def register_common_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "common"})
    async def common(message):
        text = db.get_common_text()
=======
from keyboards.keyboards import get_back_keyboard

def register_common_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "common"})
    async def common(message):
        text = db.get_common_text()
>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
        await message.answer(text, keyboard=get_back_keyboard())