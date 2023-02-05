import json

from celery.result import AsyncResult
from fastapi import Depends, HTTPException, status

from apiv1.models.dish import DishCreate
from apiv1.models.menu import MenuCreate
from apiv1.models.submenu import SubmenuCreate
from apiv1.models.task import MenuTask
from celery_tasks.tasks import start_creating_excel_file
from database.db_operations.dish_operations import DishOperations
from database.db_operations.menu_operations import CeleryOperations, MenuOperations
from database.db_operations.submenu_operations import SubmenuOperations
from database.tables import Dish, Menu, Submenu


class TaskService:
    def __init__(
        self,
        menu_operations: MenuOperations = Depends(),
        submenu_operations: SubmenuOperations = Depends(),
        dish_operations: DishOperations = Depends(),
    ):
        self.menu_operations = menu_operations
        self.submenu_operations = submenu_operations
        self.dish_operations = dish_operations

    async def create_test_data(self):
        with open("test_data.json", encoding="utf-8") as file:
            data = json.load(file)

        menus = data.get("menus")

        for menu_data in menus.values():
            submenus = menu_data.pop("submenus")
            menu = await self._create_menu(menu_data)
            for submenu_data in submenus.values():
                dishes = submenu_data.pop("dishes")
                submenu = await self._create_submenu(menu.id, submenu_data)
                for dish_data in dishes.values():
                    await self._create_dish(submenu.id, dish_data)

    async def _create_menu(self, menu_data: dict) -> Menu:
        parsed_menu = MenuCreate.parse_obj(menu_data)
        menu = await self.menu_operations.create(parsed_menu)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create menu"
            )
        return menu

    async def _create_submenu(self, menu_id: int, submenu_data: dict) -> Submenu:
        parsed_submenu = SubmenuCreate.parse_obj(submenu_data)
        submenu = await self.submenu_operations.create(menu_id, parsed_submenu)
        if not submenu:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create submenu"
            )
        return submenu

    async def _create_dish(self, submenu_id: int, dish_data: dict) -> Dish:
        parsed_dish = DishCreate.parse_obj(dish_data)
        dish = await self.dish_operations.create(submenu_id, parsed_dish)
        if not dish:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cant create dish"
            )
        return dish


class CeleryService:
    def __init__(self, operations: CeleryOperations = Depends()):
        self.operations = operations

    async def create_task_to_excel_file(self) -> dict:
        raw_menus = await self.operations.get_all_to_celery()
        menus = []
        for menu in raw_menus:
            menus.append(MenuTask.from_orm(menu).dict())
        task = start_creating_excel_file.delay(menus)
        return {"task_id": task.id, "task_status": task.status}

    async def get_excel_file_by_task_id(self, task_id: str) -> dict:
        task = AsyncResult(task_id)
        if task.status != "SUCCESS":
            raise HTTPException(
                status_code=status.HTTP_425_TOO_EARLY,
                detail=f"Task not ready or failed. Task status {task.status}",
            )
        return {
            "path": task.result,
            "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "filename": "menus",
        }
