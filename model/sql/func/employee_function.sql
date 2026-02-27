CREATE OR REPLACE FUNCTION employee_function(check_date DATE)
RETURNS TABLE(
    full_name TEXT,
    birth_date DATE,
    department_id INT,
    department_name TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.full_name,
        e.birth_date,
        d.id,
        d.name
    FROM employees AS e
    JOIN workhistory AS wh ON wh.employee_id = e.id
    JOIN departments AS d ON wh.department_id = d.id
    WHERE e.gender = 'Ж'
        AND EXTRACT(YEAR FROM age(CURRENT_DATE, e.birth_date)) = 55
        AND check_date BETWEEN wh.start_date AND COALESCE(wh.end_date, check_date)
    ORDER BY d.id;
END;
$$ LANGUAGE plpgsql;