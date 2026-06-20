<<<<<<< HEAD
from keyboards import get_large_keyboard

def register_large_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "large"})
    async def large(message):
        await message.answer("Меры поддержки многодетных семей:", keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_law"})
    async def large_law(message):
        text = db.get_large_law()  
        await message.answer(text, keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_conditions"})
    async def large_conditions(message):
        text = db.get_large_conditions()  
        await message.answer(text, keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_order"})
    async def large_order(message):
        text = db.get_large_order()  
=======
from keyboards import get_large_keyboard

def register_large_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "large"})
    async def large(message):
        await message.answer("Меры поддержки многодетных семей:", keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_law"})
    async def large_law(message):
        text = db.get_large_law()  
        await message.answer(text, keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_conditions"})
    async def large_conditions(message):
        text = db.get_large_conditions()  
        await message.answer(text, keyboard=get_large_keyboard())

    @bot.on.message(payload={"cmd": "large_order"})
    async def large_order(message):
        text = db.get_large_order()  
>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
        await message.answer(text, keyboard=get_large_keyboard())