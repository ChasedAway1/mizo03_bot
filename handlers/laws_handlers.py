from keyboards.keyboards import get_back_keyboard

def register_laws_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "laws"})
    async def laws(message):
        back_keyboard = get_back_keyboard()
        
        for i in range(1, 7):
            part_text = db.get_laws_part(i)
            await message.answer(part_text, keyboard=back_keyboard)