from vkbottle import Keyboard, KeyboardButtonColor, Text

def get_main_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Категории граждан", payload={"cmd": "categories"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Общие вопросы", payload={"cmd": "common"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Text("Выписки из законов", payload={"cmd": "laws"}), color=KeyboardButtonColor.POSITIVE)
    return keyboard

def get_categories_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Участники СВО", payload={"cmd": "svo"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Многодетные семьи", payload={"cmd": "large"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Назад", payload={"cmd": "main"}), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_svo_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Мера 1: ИЖС", payload={"cmd": "measure1"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Мера 2: Под жилым домом", payload={"cmd": "measure2"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Мера 3: Сельхозпроизводство", payload={"cmd": "measure3"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Назад", payload={"cmd": "categories"}), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_measure_keyboard(measure_num):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Перечень документов", payload={"cmd": f"docs_{measure_num}"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Кто имеет право", payload={"cmd": f"right_{measure_num}"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Как получить участок", payload={"cmd": f"howto_{measure_num}"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Выписка из закона", payload={"cmd": f"law_{measure_num}"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Назад к мерам", payload={"cmd": "svo"}), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_large_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Выписка из закона", payload={"cmd": "large_law"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Условия предоставления", payload={"cmd": "large_conditions"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Порядок предоставления", payload={"cmd": "large_order"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Назад", payload={"cmd": "categories"}), color=KeyboardButtonColor.SECONDARY)
    return keyboard

def get_back_keyboard():
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("В главное меню", payload={"cmd": "main"}), color=KeyboardButtonColor.SECONDARY)
    return keyboard