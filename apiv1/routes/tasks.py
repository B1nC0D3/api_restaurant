from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse

from apiv1.services.task_service import TaskService, CeleryService

router = APIRouter(
        prefix='/tasks')


@router.post('/create_test_data', status_code=status.HTTP_201_CREATED)
async def create_test_data(task_service: TaskService = Depends()):
    await task_service.create_test_data()
    return {'status': True,
            'detail': 'Test data was created'}


@router.post('/create_excel_file', status_code=status.HTTP_202_ACCEPTED)
async def create_excel_file(celery_service: CeleryService = Depends()):
    return await celery_service.create_task_to_excel_file()


# todo добавить возможность загрузки своего json
@router.get('/get_excel_file/{task_id}', response_class=FileResponse)
async def get_excel_file(task_id: str, celery_service: CeleryService = Depends()):
    data = await celery_service.get_excel_file_by_task_id(task_id)
    return FileResponse(**data)
