import psycopg2
from psycopg2.extras import execute_values


def account_types_insert(connection_params: dict):
    users = (
        (1, "Обычный", "Наличные, карта, ..."),
        (2, "Долговой", "Кредит, ипотека, ..."),
        (3, "Накопительный", "Сбережения, цель"),
    )

    insert_stmt = """
                  INSERT INTO public.account_types (id, name, description)
                  VALUES %s; \
                  """

    update_sequence_stmt = "SELECT setval('public.account_types_id_seq', COALESCE((SELECT MAX(id)+1 FROM account_types), 1), false);"

    with psycopg2.connect(**connection_params) as target_conn:
        with target_conn.cursor() as target_cursor:
            execute_values(target_cursor, insert_stmt, users)
            target_cursor.execute(update_sequence_stmt)
            target_conn.commit()

    print("Тип счетов успешно загружены")
