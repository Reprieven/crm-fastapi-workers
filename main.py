from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from model.setup import *
from router import departments_router, schedule_router, positons_router, employees_router, workhistory_router, queries_router

config = DataBaseConfig()

tables = [DepartmentsTableCreator(),
          PositionsTableCreator(),
          ScheduleTableCreator(),
          EmployeeTableCreator(),
          WorkHistoryTableCreator()]
views = [DepartmentView()]

functions = [AgeFunction(), CheckGradeFunction(), EmployeeFunction(),DeleteById()]

setup = DatabaseSetup(config=config, table_creators=tables, view_creators=views, func_creators=functions)

setup.create_db()
setup.create_tables()
setup.create_views()
setup.create_functions()

app = FastAPI()

app.mount("/view", StaticFiles(directory="view"), name="view")
 
@app.get("/", include_in_schema=False)
async def admin_ui():
    return FileResponse("view/index.html")

app.include_router(router=queries_router.router, tags=['queries'])
app.include_router(router=departments_router.router, tags=['departments'])
app.include_router(router=employees_router.router, tags=['employees'])
app.include_router(router=positons_router.router, tags=['positions'])
app.include_router(router=schedule_router.router, tags=['schedule'])
app.include_router(router=workhistory_router.router, tags=['workhistory'])


