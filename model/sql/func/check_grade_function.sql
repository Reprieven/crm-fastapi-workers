CREATE OR REPLACE FUNCTION check_grade_function()
RETURNS TRIGGER AS $$
DECLARE 
    position_min INT;
    position_max INT;
BEGIN
    SELECT grade_min, grade_max INTO position_min, position_max
    FROM positions WHERE id = NEW.position_id;

    IF NEW.grade IS NOT NULL AND (NEW.grade < position_min OR NEW.grade > position_max) THEN
        RAISE EXCEPTION 'Разряд % не входит в диапазон должности ID % (%-%)',
            NEW.grade, NEW.position_id, position_min, position_max;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_check_grade_function
    BEFORE INSERT OR UPDATE ON workhistory
    FOR EACH ROW EXECUTE FUNCTION check_grade_function();