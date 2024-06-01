from .config import RANGE_LIST

def chek_color(data_dict, key, ind):
    try:
        r = int(data_dict[key][ind]['red'] * 255)
    except KeyError:
        r = 0
    try:
        g = int(data_dict[key][ind]['green'] * 255)
    except KeyError:
        g = 0
    try:
        b = int(data_dict[key][ind]['blue'] * 255)
    except KeyError:
        b = 0

    return r, g, b

def check_style(data_dict, key):
    if data_dict[key][1] != None:
        r, g, b = chek_color(data_dict, key, 1)

        cell_style = f"background-color: rgb({r}, {g}, {b});"
    else:
        cell_style = ''
    
    if data_dict[key][2] != None:

        r, g, b = chek_color(data_dict, key, 2)

        font_color = f"color: rgb({r}, {g}, {b});"
    else:
        font_color = ''
    return cell_style, font_color



def generate_html_table(data_dict):
    # Находим минимальный числовой индекс ячейки
    min_index = min(int(key[1:]) for key in data_dict.keys() if key[0] != ' ')

    # Создаем заголовок таблицы
    header_html = "<tr>"
    for letter in RANGE_LIST:
        key = f"{letter.upper()}{min_index}"
        if key in data_dict:

            cell_style, font_color = check_style(data_dict, key)

            cell_data = data_dict[key]
            header_html += f"<th style='{cell_style}{font_color}'>{cell_data[0]}</th>"
    header_html += "</tr>"

    # Создаем строки данных
    data_rows_html = ""
    for i in range(min_index + 1, int(list(data_dict.keys())[-1][1:]) + 1):
        data_row_html = "<tr>"
        for letter in RANGE_LIST:
            key = f"{letter.upper()}{i}"
            if key in data_dict:

                cell_style, font_color = check_style(data_dict, key)

                cell_data = data_dict[key]
                cell_html = f"<td style='{cell_style}{font_color}'>{cell_data[0]}</td>"
                data_row_html += cell_html
        data_row_html += "</tr>"
        data_rows_html += data_row_html

    # Собираем таблицу HTML
    table_html = f"<table border='1'>{header_html}{data_rows_html}</table>"
    return table_html
