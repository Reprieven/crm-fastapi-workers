CREATE OR REPLACE VIEW department_view AS 
SELECT 
    d.id AS department_id,
    d.name AS department_name,  
    p.name AS position_name,          
    p.grade_min AS grade_min,         
    p.grade_max AS grade_max,         
    s.num AS num                      
FROM schedule AS s
JOIN departments AS d ON s.department_id = d.id
JOIN positions AS p ON s.position_id = p.id;