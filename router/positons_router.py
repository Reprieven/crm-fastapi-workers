from fastapi import APIRouter, HTTPException
from pydantic_models.models import PositionCreate, PositionResponce, PositionUpdate
from model.crud import * 
from model.config import DataBaseConfig
from typing import List

router = APIRouter()
config = DataBaseConfig()

@router.post('/position')
async def create_position(model: PositionCreate):
    try:
        inserter = Insert()
        inserter.insert_record(config, 'positions', model.model_dump())
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания позиции: {e}")

@router.get("/position/by-name", response_model = List[PositionResponce])
async def get_positions_name(name: str):
    try:
        selecter = SelectByColumn()
        result = selecter.execute(config, 'positions', 'name', name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания позиции: {e}")

@router.get("/position/{id}", response_model=PositionResponce)
async def get_position_id(id: int):
    selecter = SelectId()
    result = selecter.execute(config, 'positions', id)
    if result is None:
        raise HTTPException(status_code=404, detail="Позиции на найдено")
    return PositionResponce(**result)
    
@router.get("/position", response_model=List[PositionResponce])
async def get_positions():
    try:
        selecter = SelectGeneral()
        result = selecter.execute(config, 'positions')
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Позиций на найдено: {e}")

@router.get("/position/", response_model=List[PositionResponce])
async def get_positions_limit(num:int = 10, start: int = 0):
    try:
        selecter = SelectOffset()
        result = selecter.execute(config, 'positions', num, start)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Позиций на найдено: {e}")

@router.delete("/position/{id}")
async def delete_position(id: int):
    try:
        deleter = Delete()
        deleter.delete_record(config, 'positions', id)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления позиции: {e}")

@router.put("/position/{id}")
async def update_position(id: int, model: PositionUpdate):
    updater = Update()
    update_data = {k:v for k, v in model.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    try:
        for column, value in update_data.items():
            updater.update_record(config, 'positions', id, column, value)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обновления позиции: {e}")
    

    