from loguru import logger
import json


@logger.catch()
def editing_calendar(text: str, key: str):
    if text:
        keyboard_dict = json.loads(text.replace("'", '"'))
        if key == 'm' or key == 'y':  # редактирование месяцев
            for _ in range(len(keyboard_dict['inline_keyboard'])):
                for _ in range(len(keyboard_dict['inline_keyboard'][0])):
                    if keyboard_dict['inline_keyboard'][0][0]['text'] == ' ':
                        keyboard_dict['inline_keyboard'][0].pop(0)
                    else:
                        break
                if len(keyboard_dict['inline_keyboard'][0]) == 0:
                    keyboard_dict['inline_keyboard'].pop(0)
                else:
                    break
        elif key == 'd':  # редактирование дат
            days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
            for i, i_day in enumerate(days):
                keyboard_dict['inline_keyboard'][0][i]['text'] = i_day
            for _ in range(len(keyboard_dict['inline_keyboard']) - 2):
                count = 0
                for j in range(len(keyboard_dict['inline_keyboard'][1])):
                    if keyboard_dict['inline_keyboard'][1][j]['text'] == ' ':
                        count += 1
                    else:
                        break
                if count == 7:
                    keyboard_dict['inline_keyboard'].pop(1)
                else:
                    break

        return str(keyboard_dict).replace("'", '"')