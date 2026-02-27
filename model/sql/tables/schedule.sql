CREATE TABLE IF NOT EXISTS schedule(
    id SERIAl PRIMARY KEY,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    num INT,
    FOREIGN KEY(department_id) REFERENCES departments(id) ON DELETE CASCADE,
    FOREIGN KEY(position_id) REFERENCES positions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_schedule_department_id ON schedule(department_id);
CREATE INDEX IF NOT EXISTS idx_schedule_position_id ON schedule(position_id);