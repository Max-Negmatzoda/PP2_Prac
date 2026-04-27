-- Function 1: search by pattern (name or phone)
CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- Function 2: pagination (LIMIT + OFFSET)
CREATE OR REPLACE FUNCTION get_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;