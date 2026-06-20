from keyboards import get_svo_keyboard, get_measure_keyboard

def register_svo_handlers(bot, db):
    
    @bot.on.message(payload={"cmd": "svo"})
    async def svo(message):
        await message.answer("Меры поддержки участников СВО. Выберите нужную меру:", keyboard=get_svo_keyboard())

    @bot.on.message(payload={"cmd": "measure1"})
    async def measure1(message):
        title = db.get_svo_title(1)
        await message.answer(title, keyboard=get_measure_keyboard(1))

    @bot.on.message(payload={"cmd": "docs_1"})
    async def docs1(message):
        text = db.get_svo_docs(1)
        await message.answer(text, keyboard=get_measure_keyboard(1))

    @bot.on.message(payload={"cmd": "right_1"})
    async def right1(message):
        text = db.get_svo_right(1)
        await message.answer(text, keyboard=get_measure_keyboard(1))

    @bot.on.message(payload={"cmd": "howto_1"})
    async def howto1(message):
        text = db.get_svo_howto(1)
        await message.answer(text, keyboard=get_measure_keyboard(1))

    @bot.on.message(payload={"cmd": "law_1"})
    async def law1(message):
        text = db.get_svo_law(1)
        await message.answer(text, keyboard=get_measure_keyboard(1))

    # Мера 2
    @bot.on.message(payload={"cmd": "measure2"})
    async def measure2(message):
        await message.answer(db.get_svo_title(2), keyboard=get_measure_keyboard(2))

    @bot.on.message(payload={"cmd": "docs_2"})
    async def docs2(message):
        await message.answer(db.get_svo_docs(2), keyboard=get_measure_keyboard(2))

    @bot.on.message(payload={"cmd": "right_2"})
    async def right2(message):
        await message.answer(db.get_svo_right(2), keyboard=get_measure_keyboard(2))

    @bot.on.message(payload={"cmd": "howto_2"})
    async def howto2(message):
        await message.answer(db.get_svo_howto(2), keyboard=get_measure_keyboard(2))

    @bot.on.message(payload={"cmd": "law_2"})
    async def law2(message):
        await message.answer(db.get_svo_law(2), keyboard=get_measure_keyboard(2))

    # Мера 3
    @bot.on.message(payload={"cmd": "measure3"})
    async def measure3(message):
        await message.answer(db.get_svo_title(3), keyboard=get_measure_keyboard(3))

    @bot.on.message(payload={"cmd": "docs_3"})
    async def docs3(message):
        await message.answer(db.get_svo_docs(3), keyboard=get_measure_keyboard(3))

    @bot.on.message(payload={"cmd": "right_3"})
    async def right3(message):
        await message.answer(db.get_svo_right(3), keyboard=get_measure_keyboard(3))

    @bot.on.message(payload={"cmd": "howto_3"})
    async def howto3(message):
        await message.answer(db.get_svo_howto(3), keyboard=get_measure_keyboard(3))

    @bot.on.message(payload={"cmd": "law_3"})
    async def law3(message):
        await message.answer(db.get_svo_law(3), keyboard=get_measure_keyboard(3))