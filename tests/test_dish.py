from fastapi import status

DISHES_URL = '/api/v1/menus/1/submenus/1/dishes'


class TestDish:

    def test_dishes_blank(self, client, create_menu, create_submenu):
        response = client.get(DISHES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_dish_create(self, client):
        data = {
            'title': 'test title',
            'description': 'test desc',
            'price': 10.50
        }
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'price': '10.50'
        }
        response = client.post(DISHES_URL, json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == response_data

    def test_dishes_filled(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'price': '10.50'
        }

        response = client.get(DISHES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [response_data]

    def test_dish_get_by_id(self, client):
        response_data = {
            'id': '1',
            'title': 'test title',
            'description': 'test desc',
            'price': '10.50'
        }

        response = client.get(DISHES_URL + '/1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_dish_not_found(self, client):
        response_data = {
            'detail': 'dish not found'
        }

        response = client.get(DISHES_URL + '/111')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data

    def test_dish_update(self, client):
        update_data = {
            'title': 'updated title',
            'description': 'updated description',
            'price': '100.50'
        }
        response_data = {
            'id': '1',
            'title': 'updated title',
            'description': 'updated description',
            'price': '100.50'
        }

        response = client.patch(DISHES_URL + '/1', json=update_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_dish_delete(self, client):
        response_data = {
            'status': True,
            'message': 'The dish has been deleted',
        }

        response = client.delete(DISHES_URL + '/1')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == response_data

    def test_title_validation(self, client):
        data = {
            'title': [],
            'description': 'test desc',
            'price': 10.50
        }

        response = client.post(DISHES_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_description_validation(self, client):
        data = {
            'title': 'test title',
            'description': [],
            'price': 10.50
        }

        response = client.post(DISHES_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_price_validation(self, client):
        data = {
            'title': 'test title',
            'description': 'test desc',
            'price': [10.50]
        }

        response = client.post(DISHES_URL, json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_dish_didnt_create_without_submenu(self, client):
        data = {
            'title': 'test title',
            'description': 'test description',
            'price': 10.50,
        }
        response_data = {
            'detail': 'Create submenu first'
        }

        response = client.post(DISHES_URL, json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == response_data
