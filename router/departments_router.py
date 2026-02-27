from fastapi import APIRouter, HTTPException
from pydantic_models.models import DepartmentCreate, DepartmentResponce, DepartmentUpdate
from model.crud import * 
from model.config import DataBaseConfig
from typing import List
router = APIRouter()
config = DataBaseConfig()

@router.post('/department')
async def create_department(model: DepartmentCreate):
    try:
        inserter = Insert()
        inserter.insert_record(config, 'departments', model.model_dump())
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания отдела: {e}")

@router.get("/department/by-name", response_model = List[DepartmentResponce])
async def get_departments_name(name: str):
    try:
        selecter = SelectByColumn()
        result = selecter.execute(config, 'departments', 'name', name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения отдела по имени: {e}")

@router.get("/department/{id}", response_model=DepartmentResponce)
async def get_department_id(id: int):
    try:
        selecter = SelectId()
        result = selecter.execute(config, 'departments', id)
        if result is None:
            raise HTTPException(status_code=404, detail="Подразделение не найдено")
        return DepartmentResponce(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения отдела по id: {e}")

        
@router.get("/department", response_model=List[DepartmentResponce])
async def get_departments():
    try:
        selecter = SelectGeneral()
        result = selecter.execute(config, 'departments')
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения отделов: {e}")

@router.get("/department/", response_model=List[DepartmentResponce])
async def get_departments_limit(num:int = 10, start: int = 0):
    try:
        selecter = SelectOffset()
        result = selecter.execute(config, 'departments', num, start)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения отделов по ограничению количества: {e}")

@router.delete("/department/{id}")
async def delete_departments(id: int):
    try:
        deleter = Delete()
        deleter.delete_record(config, 'departments', id)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления отдела: {e}")

@router.put("/department/{id}")
async def update_departments(id: int, model: DepartmentUpdate):
    updater = Update()
    update_data = {k:v for k, v in model.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")
    try:
        for column, value in update_data.items():
            updater.update_record(config, 'departments', id, column, value)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обновления отдела: {e}")
    

    