from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values


def users_load(connection_params: dict):

    qwerty_password_hash = "$2b$12$Jo7WlgixuZY74JW/jzS4Y.acv8kMjvqCEKLGZtwVONQUQ5Jy7gCdq"
    string_password_hash = "$2b$12$YQRDP6ncv6IPDJ5U8hfWpuhjbxmBBGntKTsd0/yoF2IvyUD5iLsXe"

    users = (
        (1, "admin@mail.ru", "Админ", 1, qwerty_password_hash, True, datetime.now(), datetime.now()),
        (2, "user@example.com", "Тестовый пользователь", 2, string_password_hash, True, datetime.now(), datetime.now()),
    )

    insert_stmt = """
        INSERT INTO public.users (
            id, email, name, role_id, hash_password, is_active, created_at, updated_at
        ) VALUES %s;
        """

    update_sequence_stmt = "SELECT setval('public.users_id_seq', COALESCE((SELECT MAX(id)+1 FROM users), 1), false);"

    with psycopg2.connect(**connection_params) as target_conn:
        with target_conn.cursor() as target_cursor:
            execute_values(target_cursor, insert_stmt, users)
            target_cursor.execute(update_sequence_stmt)
            target_conn.commit()

    print("Пользователи успешно загружены")