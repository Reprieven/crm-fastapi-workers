CREATE OR REPLACE PROCEDURE delete_record_by_id(
    table_name TEXT,
    record_id INTEGER
)
AS $$
BEGIN
    EXECUTE format('DELETE FROM %I WHERE id = $1', table_name) 
    USING record_id;
END;
$$ LANGUAGE plpgsql;