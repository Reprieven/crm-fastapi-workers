from fastapi import APIRouter, HTTPException
from pydantic_models.models import WorkHistoryCreate, WorkHistoryResponce, WorkHistoryUpdate
from model.crud import * 
from model.config import DataBaseConfig
from typing import List
router = APIRouter()
config = DataBaseConfig()

@router.post('/workhistory')
async def create_workhistory(model: WorkHistoryCreate):
    try:
        inserter = Insert()
        inserter.insert_record(config, 'workhistory', model.model_dump())
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания истории работы: {e}")

@router.get("/workhistory/{id}", response_model=WorkHistoryResponce)
async def get_workhistory_id(id: int):
    selecter = SelectId()
    result = selecter.execute(config, 'workhistory', id)
    if result is None:
        raise HTTPException(status_code=404, detail="История работы на найдено")
    return WorkHistoryResponce(**result)
    
    
@router.get("/workhistory", response_model=List[WorkHistoryResponce])
async def get_workhistory():
    try:
        selecter = SelectGeneral()
        result = selecter.execute(config, 'workhistory')
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска работы: {e}")
    
@router.get("/workhistory/", response_model=List[WorkHistoryResponce])
async def get_workhistory_limit(num:int = 10, start: int = 0):
    try:
        selecter = SelectOffset()
        result = selecter.execute(config, 'workhistory', num, start)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска работы по лимиту: {e}")

@router.delete("/workhistory/{id}")
async def delete_workhistory(id: int):
    try:
        deleter = Delete()
        deleter.delete_record(config, 'workhistory', id)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления истории работы: {e}")

@router.put("/workhistory/{id}")
async def update_workhistory(id: int, model: WorkHistoryUpdate):
    updater = Update()
    update_data = {k:v for k, v in model.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    try:
        for column, value in update_data.items():
            updater.update_record(config, 'workhistory', id, column, value)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обновления истории работы: {e}")
    

    