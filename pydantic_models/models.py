from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional

class DepartmentBase(BaseModel):
    name : str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None

class DepartmentResponce(BaseModel):
    id: int
    name: str

class EmployeeBase(BaseModel):
    full_name: str
    birth_date: date
    gender: str
    marital_status: str

    @field_validator('birth_date')
    def check_age(cls, value):
        today = date.today()
        if value > date(today.year - 18, today.month, today.day):
            raise ValueError("Сотрудник младше 18 лет")
        return value
    
    @field_validator('gender')
    def check_gender(cls, value):
        if value not in ['Ж','М']:
            raise ValueError("Некорректный пол сотрудника")
        return value
    
class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    marital_status: Optional[str] = None

class EmployeeResponce(BaseModel):
    id: int
    full_name: str
    birth_date: date
    gender: str
    marital_status: str

class PositionBase(BaseModel):
    name: str
    short_name: str
    code: str
    grade_min: int
    grade_max: int

    @field_validator('grade_min')
    @classmethod
    def check_grade_min(cls, value):
        if value < 1 or value > 18:
            raise ValueError('Некорректное значение минимального разряда')
        return value
    
    @field_validator('grade_max')
    @classmethod
    def check_grade_max(cls, value):
        if value < 1 or value > 18:
            raise ValueError('Некорректное значение максимального разряда')
        return value
    
    @field_validator('grade_max')
    @classmethod
    def check_max_grade(cls, value, info):
        values = info.data
        if 'grade_min' in values and value < values['grade_min']:
            raise ValueError('Максимальный разряд должен быть больше или равен минимальному')
        return value

    @field_validator('grade_min')  
    @classmethod
    def check_min_grade(cls, value, info):
        values = info.data
        if 'grade_max' in values and value > values['grade_max']:
            raise ValueError('Минимальный разряд должен быть меньше или равен максимальному')
        return value
    
class PositionCreate(PositionBase):
    pass

class PositionUpdate(PositionBase):
    name: Optional[str] = None
    short_name: Optional[str] = None
    code: Optional[str] = None
    grade_min: Optional[int] = None
    grade_max: Optional[int]= None

class PositionResponce(BaseModel):
    id: int
    name: str
    short_name: str
    code: str
    grade_min: int
    grade_max: int

class ScheduleBase(BaseModel):
    department_id: int
    position_id: int
    num: int

    @field_validator('num')
    def check_num(cls, value):
        if value<0:
            raise ValueError('Колличество мест не может быть отрицательным')
        return value

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    num: Optional[int] = None

class ScheduleResponce(BaseModel):
    id: int
    department_id: int
    position_id: int
    num: int

class WorkHistoryBase(BaseModel):
    employee_id: int
    department_id: int
    position_id: int
    grade: int
    start_date: date
    end_date: Optional[date] = None

    @field_validator('start_date')
    @classmethod
    def check_start_date(cls, value, info):
        values = info.data
        if 'end_date' in values  and values['end_date']:
            if values['end_date'] < value:
                raise ValueError('Дата окончания работы не может быть раньше даты начала')
        return value
    
    @field_validator('end_date')
    @classmethod
    def check_end_date(cls, value, info):
        values = info.data
        if 'start_date' in values and value:
            if value < values['start_date']:
                raise ValueError('Дата окончания работы не может быть раньше даты начала')
        return value

    @field_validator('grade')
    @classmethod
    def check_grade(cls, value):
        if value < 1 or value > 18:
            raise ValueError('Неправильное значение разряда')
        return value

class WorkHistoryCreate(WorkHistoryBase):
    pass

class WorkHistoryUpdate(WorkHistoryBase):
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    grade: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class WorkHistoryResponce(WorkHistoryBase):
    id: int
    employee_id: int
    department_id: int
    position_id: int
    grade: int
    start_date: date
    end_date: Optional[date] = None

class EmployeeQueryResponce(BaseModel):
    full_name: str
    birth_date: date
    department_id: int
    department_name: str

class DepartmentQuerryResponce(BaseModel):
    department_id: int
    department_name: str
    position_name: str
    grade_min: int
    grade_max: int
    num: int