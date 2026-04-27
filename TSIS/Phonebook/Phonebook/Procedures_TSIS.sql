-- Add phone to existing contact
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    phone VARCHAR,
    email VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        p.id,
        p.name,
        p.phone,
        p.email
    FROM phonebook p
    LEFT JOIN phones ph ON p.id = ph.contact_id
    WHERE
        p.name ILIKE '%' || p_query || '%'
        OR p.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%';
END;
$$;


-- Move contact to group (create group if not exists)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    g_id INTEGER;
BEGIN
    -- Create group if not exists
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- Get group id
    SELECT id INTO g_id
    FROM groups
    WHERE name = p_group_name;

    -- Update contact
    UPDATE phonebook
    SET group_id = g_id
    WHERE name = p_contact_name;
END;
$$;


-- Search contacts by name, email or phone
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    name TEXT,
    phone TEXT,
    email TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        p.id,
        p.name,
        p.phone,
        p.email
    FROM phonebook p
    LEFT JOIN phones ph ON p.id = ph.contact_id
    WHERE
        p.name ILIKE '%' || p_query || '%'
        OR p.email ILIKE '%' || p_query || '%'
        OR ph.phone ILIKE '%' || p_query || '%';
END;
$$;