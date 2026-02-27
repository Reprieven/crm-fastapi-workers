CREATE OR REPLACE FUNCTION age_function(max_age INT, pos_id INT)
RETURNS TABLE(
    id INT,
    full_name TEXT,
    birth_date DATE,
    gender TEXT,
    marital_status TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.id,
        e.full_name,
        e.birth_date,
        e.gender,
        e.marital_status
    FROM employees AS e
    JOIN workhistory AS wh ON e.id = wh.employee_id
    JOIN positions AS p ON wh.position_id = p.id
    WHERE EXTRACT(YEAR FROM age(CURRENT_DATE, e.birth_date)) < max_age
        AND p.id = pos_id
        AND CURRENT_DATE BETWEEN wh.start_date AND COALESCE(wh.end_date, CURRENT_DATE);
END;
$$ LANGUAGE plpgsql;