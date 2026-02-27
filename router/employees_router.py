from fastapi import APIRouter, HTTPException
from pydantic_models.models import EmployeeCreate, EmployeeResponce, EmployeeUpdate
from model.crud import * 
from model.config import DataBaseConfig
from typing import List
router = APIRouter()
config = DataBaseConfig()

@router.post('/employee')
async def create_employee(model: EmployeeCreate):
    try:
        inserter = Insert()
        inserter.insert_record(config, 'employees', model.model_dump())
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка создания работника: {e}")

@router.get("/employee/by-full-name", response_model = List[EmployeeResponce])
async def get_employees_name(full_name: str):
    try:
        selecter = SelectByColumn()
        result = selecter.execute(config, 'employees', 'full_name', full_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска по имени: {e}")


@router.get("/employee/{id}", response_model=EmployeeResponce)
async def get_employee_id(id: int):
    selecter = SelectId()
    result = selecter.execute(config, 'employees', id)
    if result is None:
        raise HTTPException(status_code=404, detail="Работник не найден")
    return EmployeeResponce(**result)
    
@router.get("/employee", response_model=List[EmployeeResponce])
async def get_employees():
    try:
        selecter = SelectGeneral()
        result = selecter.execute(config, 'employees')
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска работников: {e}")

@router.get("/employee/", response_model=List[EmployeeResponce])
async def get_employees_limit(num:int = 10, start: int = 0):
    try:
        selecter = SelectOffset()
        result = selecter.execute(config, 'employees', num, start)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка поиска по лимиту записей: {e}")


@router.delete("/employee/{id}")
async def delete_employee(id: int):
    try:
        deleter = Delete()
        deleter.delete_record(config, 'employees', id)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления работника: {e}")

@router.put("/employee/{id}")
async def update_employee(id: int, model: EmployeeUpdate):
    updater = Update()
    update_data = {k:v for k, v in model.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для работников")
    try:
        for column, value in update_data.items():
            updater.update_record(config, 'employees', id, column, value)
        return {"message":"ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обновления работника: {e}")
    

    