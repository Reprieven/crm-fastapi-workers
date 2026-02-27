CREATE TABLE IF NOT EXISTS employees(
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE CHECK(birth_date <= CURRENT_DATE - INTERVAL '18 years'),
    gender TEXT CHECK(gender IN ('М','Ж')),
    marital_status TEXT
);

CREATE INDEX IF NOT EXISTS idx_employees_birth_date ON employees(birth_date)
WHERE birth_date IS NOT NULL;