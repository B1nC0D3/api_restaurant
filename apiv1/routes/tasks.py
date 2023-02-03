from fastapi import APIRouter, Depends, status

from apiv1.services.task_service import TaskService

router = APIRouter(
        prefix='/tasks')


@router.post('/create_test_data', status_code=status.HTTP_201_CREATED)
async def create_test_data(task_service: TaskService = Depends()):
    await task_service.create_test_data()
    return {'status': True,
            'detail': 'Test data was created'}


@router.post('/create_excel_file')
async def create_excel_file():
    pass


@router.get('/get_excel_file/{task_id}')
async def get_excel_file(task_id: str):  # todo добавить возможность загрузки своего json
    pass
