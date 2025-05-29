import psycopg2

def roles_insert(connection_params: dict):

    insert_stmt = "INSERT INTO roles (name) VALUES ('admin'), ('user');"

    update_sequence_stmt = "SELECT setval('public.roles_id_seq', COALESCE((SELECT MAX(id)+1 FROM roles), 1), false);"

    with psycopg2.connect(**connection_params) as target_conn:
        with target_conn.cursor() as target_cursor:
            target_cursor.execute(insert_stmt)
            target_cursor.execute(update_sequence_stmt)
            target_conn.commit()

    print("Роли успешно загружены")
