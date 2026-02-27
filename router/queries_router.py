from fastapi import APIRouter, HTTPException
from model.queries import DepartmentQuery, EmployeeQuery, EmployeeAgeCheckQuery
from pydantic_models.models import EmployeeQueryResponce, EmployeeResponce, DepartmentQuerryResponce
from model.crud import * 
from model.config import DataBaseConfig
from typing import List
from datetime import date
router = APIRouter()
config = DataBaseConfig()

@router.get('/queries_department/{department_id}', response_model=List[DepartmentQuerryResponce])
def get_departments(department_id:int):
    try:
        query = DepartmentQuery()
        result = query.execute(config=config, department_id=department_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка запроса: {e}")
    
@router.get('/queries_pension/{Date}', response_model=List[EmployeeQueryResponce])
def get_employees(Date: date):
    try:
        query = EmployeeQuery()
        result = query.execute(config=config, date = Date)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка запроса: {e}")
    
@router.get('/queries_age/', response_model=List[EmployeeResponce])
def get_employees(age: int, position_id: int):
    try:
        query = EmployeeAgeCheckQuery()
        result = query.execute(config=config, age=age, pos_id=position_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка запроса: {e}")