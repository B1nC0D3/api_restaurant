import pytest
from fastapi import status

SUBMENU_URL = "/menus/1/submenus/"


class TestSubmenu:
    @pytest.mark.asyncio
    async def test_submenus_blank(self, client, create_menu):
        response = await client.get(SUBMENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_submenu_create(self, client):
        data = {
            "title": "test title",
            "description": "test desc",
        }
        response_data = {
            "id": "1",
            "title": "test title",
            "description": "test desc",
            "dishes_count": 0,
        }

        response = await client.post(SUBMENU_URL, json=data)

        assert response.json() == response_data
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_submenus_filled(self, client):
        response_data = {
            "id": "1",
            "title": "test title",
            "description": "test desc",
            "dishes_count": 0,
        }

        response = await client.get(SUBMENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [response_data]

    @pytest.mark.asyncio
    async def test_submenu_get_by_id(self, client):
        response_data = {
            "id": "1",
            "title": "test title",
            "description": "test desc",
            "dishes_count": 0,
        }

        response = await client.get(SUBMENU_URL + "1")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_submenu_not_found(self, client):
        response_data = {
            "detail": "submenu not found",
        }

        response = await client.get(SUBMENU_URL + "111")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_submenu_update(self, client):
        updated_data = {
            "title": "updated title",
            "description": "updated desc",
        }
        response_data = {
            "id": "1",
            "title": "updated title",
            "description": "updated desc",
            "dishes_count": 0,
        }

        response = await client.patch(SUBMENU_URL + "1", json=updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_dishes_count(self, client):
        dish_data = {
            "title": "test title",
            "description": "test desc",
            "price": "10.50",
        }
        response_data = {
            "id": "1",
            "title": "updated title",
            "description": "updated desc",
            "dishes_count": 2,
        }

        await client.post(SUBMENU_URL + "1/dishes/", json=dish_data)
        await client.post(SUBMENU_URL + "1/dishes/", json=dish_data)
        response = await client.get("/menus/1/submenus/1")

        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_submenu_delete(self, client):
        response_data = {
            "status": True,
            "message": "The submenu has been deleted",
        }

        response = await client.delete(SUBMENU_URL + "1")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_title_validation(self, client):
        data = {
            "title": ["test title"],
            "description": "test desc",
        }

        response = await client.post(SUBMENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_description_validation(self, client):
        data = {
            "title": "test title",
            "description": ["test desc"],
        }

        response = await client.post(SUBMENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_submenu_didnt_create_without_menu(self, client):
        data = {
            "title": "test title",
            "description": "description",
        }
        response_data = {
            "detail": "menu not found",
        }

        response = await client.post("/menus/111/submenus/", json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data
