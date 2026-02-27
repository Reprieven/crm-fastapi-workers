from fastapi import APIRouter, HTTPException
from pydantic_models.models import ScheduleCreate, ScheduleResponce, ScheduleUpdate
from model.crud import * 
from model.config import DataBaseConfig
from typing import List
router = APIRouter()
config = DataBaseConfig()

@router.post('/schedule')
async def create_schedule(model: ScheduleCreate):
    try:
        inserter = Insert()
        inserter.insert_record(config, 'schedule', model.model_dump())
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания расписание: {e}")

@router.get("/schedule/{id}", response_model = ScheduleResponce)
async def get_schedule_id(id: int):
    selecter = SelectId()
    result = selecter.execute(config, 'schedule', id)
    if result is None:
        raise HTTPException(status_code=404, detail="Расписание на найдено")
    return ScheduleResponce(**result)
    
@router.get("/schedule", response_model=List[ScheduleResponce])
async def get_schedules():
    try:
        selecter = SelectGeneral()
        result = selecter.execute(config, 'schedule')
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска расписания: {e}")
    
@router.get("/schedule/", response_model=List[ScheduleResponce])
async def get_schedules_limit(num:int = 10, start: int = 0):
    try:
        selecter = SelectOffset()
        result = selecter.execute(config, 'schedule', num, start)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска по лимиту: {e}")

@router.delete("/schedule/{id}")
async def delete_schedule(id: int):
    try:
        deleter = Delete()
        deleter.delete_record(config, 'schedule', id)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления расписания: {e}")

@router.put("/schedule/{id}")
async def update_schedule(id: int, model: ScheduleUpdate):
    updater = Update()
    update_data = {k:v for k, v in model.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    try:
        for column, value in update_data.items():
            updater.update_record(config, 'schedule', id, column, value)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обновления расписания: {e}")
    

    