import pytest
from fastapi import status

MENU_URL = '/menus/'


class TestMenu:

    @pytest.mark.asyncio
    async def test_get_menus_blank(self, client):
        response = await client.get(MENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_menu_create(self, client):
        data = {
            'title': 'test title',
            'description': 'test desc',
        }
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'submenus_count': 0,
            'dishes_count': 0,
        }

        response = await client.post(MENU_URL, json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_get_menus_filled(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'submenus_count': 0,
            'dishes_count': 0,
        }

        response = await client.get(MENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [response_data]

    @pytest.mark.asyncio
    async def test_menu_get_by_id(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'submenus_count': 0,
            'dishes_count': 0,
        }

        response = await client.get(MENU_URL + '1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_menu_not_found(self, client):
        response_data = {
            'detail': 'menu not found',
        }

        response = await client.get(MENU_URL + '111')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_menu_update(self, client):
        update_data = {
            'title': 'updated title',
            'description': 'updated desc',
        }
        response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated desc',
            'submenus_count': 0,
            'dishes_count': 0,
        }

        response = await client.patch(MENU_URL + '1', json=update_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_submenus_count(self, client):

        menu_response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated desc',
            'submenus_count': 2,
            'dishes_count': 0,
        }
        submenu_data = {
            'title': 'test title',
            'description': 'test desc',
        }

        await client.post(MENU_URL + '1/submenus/', json=submenu_data)
        await client.post(MENU_URL + '1/submenus/', json=submenu_data)

        response = await client.get(MENU_URL + '1')

        assert response.json() == menu_response_data

    @pytest.mark.asyncio
    async def test_dishes_count(self, client):
        response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated desc',
            'submenus_count': 2,
            'dishes_count': 2,
        }
        dish_data = {
            'title': 'test title',
            'description': 'test desc',
            'price': '13.50',
        }

        await client.post(MENU_URL + '1/submenus/1/dishes/', json=dish_data)
        await client.post(MENU_URL + '1/submenus/1/dishes/', json=dish_data)
        response = await client.get(MENU_URL + '1')

        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_post_delete(self, client):
        response_data = {
            'status': True,
            'message': 'The menu has been deleted',
        }

        response = await client.delete(MENU_URL + '1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    @pytest.mark.asyncio
    async def test_title_validate(self, client):
        data = {
            'title': ['test title'],
            'description': 'test desc',
        }

        response = await client.post(MENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_description_validate(self, client):
        data = {
            'title': 'test title',
            'description': ['test desc'],
        }

        response = await client.post(MENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
