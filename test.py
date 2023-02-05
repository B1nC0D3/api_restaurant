import asyncio

import xlsxwriter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from apiv1.models.task import MenuTask
from database.database import Session
from database.tables import Menu


async def test():
    workbook = xlsxwriter.Workbook('menus.xlsx')
    worksheet = workbook.add_worksheet('Menus')
    async with Session() as session:
        raw_menus = await session.execute(
                    select(Menu)
                    .options(selectinload(Menu.submenus)))
    menus = []
    for menu in raw_menus.unique().scalars().all():
        menus.append(MenuTask.from_orm(menu))
    row = 0
    for menu_cnt, menu in enumerate(menus, 1):
        col = 0
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


asyncio.run(test())
