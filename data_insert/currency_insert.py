import psycopg2
from psycopg2.extras import execute_values


def currencies_insert(connection_params: dict):
    users = (
        # Фиатные валюты
        (1, "Российский рубль", "RUB", "https://example.com/icons/rub.png"),
        (2, "Доллар США", "USD", "https://example.com/icons/usd.png"),
        (3, "Евро", "EUR", "https://example.com/icons/eur.png"),
        (4, "Британский фунт", "GBP", "https://example.com/icons/gbp.png"),
        (5, "Японская иена", "JPY", "https://example.com/icons/jpy.png"),
        (6, "Китайский юань", "CNY", "https://example.com/icons/cny.png"),
        (7, "Швейцарский франк", "CHF", "https://example.com/icons/chf.png"),
        (8, "Австралийский доллар", "AUD", "https://example.com/icons/aud.png"),
        (9, "Канадский доллар", "CAD", "https://example.com/icons/cad.png"),
        (10, "Сингапурский доллар", "SGD", "https://example.com/icons/sgd.png"),
        # Криптовалюты
        (11, "Bitcoin", "BTC", "https://example.com/icons/btc.png"),
        (12, "Ethereum", "ETH", "https://example.com/icons/eth.png"),
        (13, "Toncoin", "TON", "https://example.com/icons/ton.png"),
    )

    insert_stmt = """
                  INSERT INTO public.currencies (id, name, short_name, icon_url)
                  VALUES %s; \
                  """

    update_sequence_stmt = "SELECT setval('public.currencies_id_seq', COALESCE((SELECT MAX(id)+1 FROM currencies), 1), false);"

    with psycopg2.connect(**connection_params) as target_conn:
        with target_conn.cursor() as target_cursor:
            execute_values(target_cursor, insert_stmt, users)
            target_cursor.execute(update_sequence_stmt)
            target_conn.commit()

    print("Валюты успешно загружены")
