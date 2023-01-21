from fastapi import status

SUBMENU_URL = '/api/v1/menus/1/submenus'


class TestSubmenu:

    def test_submenus_blank(self, client, create_menu):
        response = client.get(SUBMENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_submenu_create(self, client):
        data = {
            'title': 'test title',
            'description': 'test desc'
        }
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'dishes_count': 0,
        }

        response = client.post(SUBMENU_URL, json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == response_data

    def test_submenus_filled(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'dishes_count': 0
        }

        response = client.get(SUBMENU_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [response_data]

    def test_submenu_get_by_id(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'dishes_count': 0
        }

        response = client.get(SUBMENU_URL + '/1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_submenu_not_found(self, client):
        response_data = {
            'detail': 'submenu not found'
        }

        response = client.get(SUBMENU_URL + '/111')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data

    def test_submenu_update(self, client):
        updated_data = {
            'title': 'updated title',
            'description': 'updated desc'
        }
        response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated desc',
            'dishes_count': 0
        }

        response = client.patch(SUBMENU_URL + '/1', json=updated_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_dishes_count(self, client):
        dish_data = {
            'title': 'test title',
            'description': 'test desc',
            'price': '10.50'
        }
        response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated desc',
            'dishes_count': 2
        }

        client.post(SUBMENU_URL + '/1/dishes', json=dish_data)
        client.post(SUBMENU_URL + '/1/dishes', json=dish_data)
        response = client.get('/api/v1/menus/1/submenus/1')

        assert response.json() == response_data

    def test_submenu_delete(self, client):
        response_data = {
            'status': True,
            'message': 'The submenu has been deleted'
        }

        response = client.delete(SUBMENU_URL + '/1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_title_validation(self, client):
        data = {
            'title': ['test title'],
            'description': 'test desc',
        }

        response = client.post(SUBMENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_description_validation(self, client):
        data = {
            'title': 'test title',
            'description': ['test desc'],
        }

        response = client.post(SUBMENU_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_submenu_didnt_create_without_menu(self, client):
        data = {
            'title': 'test title',
            'description': 'description'
        }
        response_data = {
            'detail': 'menu not found'
        }

        response = client.post('/api/v1/menus/111/submenus', json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data
