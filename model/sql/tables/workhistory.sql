CREATE TABLE IF NOT EXISTS workhistory(
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    grade INT,
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY(employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY(department_id) REFERENCES departments(id) ON DELETE CASCADE,
    FOREIGN KEY(position_id) REFERENCES positions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_workhistory_employee_id ON workhistory(employee_id)
WHERE end_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_workhistory_department_id ON workhistory(department_id)
WHERE end_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_workhistory_position_id ON workhistory(position_id)
WHERE end_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_workhistory_position_dates ON workhistory(position_id, start_date, end_date) 
WHERE end_date IS NULL;