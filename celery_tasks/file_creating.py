import os

import xlsxwriter

from apiv1.models.task import MenuTask


def create_excel_file(raw_menus: dict, task_id: str) -> str:
    path = "files/"
    file_path = f"{path}/{task_id}.xlsx"
    if not os.path.exists(path):
        os.makedirs(path)
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet("Menus")
    row = 0

    for menu_cnt, raw_menu in enumerate(raw_menus, 1):
        col = 0
        menu = MenuTask.parse_obj(raw_menu)
        menu_data = [menu_cnt, menu.title, menu.description]
        submenus = menu.submenus
        worksheet.write_row(row, col, menu_data)
        row += 1

        for submenu_cnt, submenu in enumerate(submenus, 1):
            col = 1
            submenu_data = [submenu_cnt, submenu.title, submenu.description]
            dishes = submenu.dishes
            worksheet.write_row(row, col, submenu_data)
            row += 1

            for dish_cnt, dish in enumerate(dishes, 1):
                col = 2
                dish_data = [dish_cnt, dish.title, dish.description, dish.price]
                worksheet.write_row(row, col, dish_data)
                row += 1

    workbook.close()
    return file_path
