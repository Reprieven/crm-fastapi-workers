CREATE TABLE IF NOT EXISTS positions(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT,
    code TEXT,
    grade_min INT CHECK(grade_min>=1 AND grade_min<=18),
    grade_max INT CHECK(grade_max>=1 AND grade_max<=18)
);