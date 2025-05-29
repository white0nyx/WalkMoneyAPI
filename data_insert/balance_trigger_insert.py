import psycopg2
from psycopg2 import Error

def balance_trigger_insert(connection_params: dict):
    create_trigger_script = """
    -- Удаляем существующую функцию, если она есть
    DROP FUNCTION IF EXISTS update_account_balance() CASCADE;

    -- Создаем функцию
    CREATE OR REPLACE FUNCTION update_account_balance()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Проверка существования счетов
        IF (NEW IS NOT NULL AND NEW.account_id IS NOT NULL AND NOT EXISTS (
                SELECT 1 FROM accounts WHERE id = NEW.account_id
            )) THEN
            RAISE EXCEPTION 'Account with id % does not exist', NEW.account_id;
        END IF;
        IF (NEW IS NOT NULL AND NEW.transaction_type = 'transfer' AND NEW.transfer_to_account_id IS NOT NULL AND NOT EXISTS (
                SELECT 1 FROM accounts WHERE id = NEW.transfer_to_account_id
            )) THEN
            RAISE EXCEPTION 'Transfer account with id % does not exist', NEW.transfer_to_account_id;
        END IF;
        IF (OLD IS NOT NULL AND OLD.account_id IS NOT NULL AND NOT EXISTS (
                SELECT 1 FROM accounts WHERE id = OLD.account_id
            )) THEN
            RAISE EXCEPTION 'Account with id % does not exist', OLD.account_id;
        END IF;
        IF (OLD IS NOT NULL AND OLD.transaction_type = 'transfer' AND OLD.transfer_to_account_id IS NOT NULL AND NOT EXISTS (
                SELECT 1 FROM accounts WHERE id = OLD.transfer_to_account_id
            )) THEN
            RAISE EXCEPTION 'Transfer account with id % does not exist', OLD.transfer_to_account_id;
        END IF;

        -- Обработка INSERT
        IF TG_OP = 'INSERT' THEN
            IF NEW.transaction_type = 'income' THEN
                UPDATE accounts
                SET balance = balance + NEW.amount
                WHERE id = NEW.account_id;
            ELSIF NEW.transaction_type = 'expense' THEN
                UPDATE accounts
                SET balance = balance - NEW.amount
                WHERE id = NEW.account_id;
            ELSIF NEW.transaction_type = 'transfer' THEN
                UPDATE accounts
                SET balance = balance - NEW.amount
                WHERE id = NEW.account_id;
                UPDATE accounts
                SET balance = balance + NEW.amount
                WHERE id = NEW.transfer_to_account_id;
            END IF;

        -- Обработка DELETE
        ELSIF TG_OP = 'DELETE' THEN
            IF OLD.transaction_type = 'income' THEN
                UPDATE accounts
                SET balance = balance - OLD.amount
                WHERE id = OLD.account_id;
            ELSIF OLD.transaction_type = 'expense' THEN
                UPDATE accounts
                SET balance = balance + OLD.amount
                WHERE id = OLD.account_id;
            ELSIF OLD.transaction_type = 'transfer' THEN
                UPDATE accounts
                SET balance = balance + OLD.amount
                WHERE id = OLD.account_id;
                UPDATE accounts
                SET balance = balance - OLD.amount
                WHERE id = OLD.transfer_to_account_id;
            END IF;

        -- Обработка UPDATE
        ELSIF TG_OP = 'UPDATE' THEN
            IF OLD.account_id != NEW.account_id OR OLD.amount != NEW.amount OR 
               OLD.transaction_type != NEW.transaction_type OR 
               OLD.transfer_to_account_id IS DISTINCT FROM NEW.transfer_to_account_id THEN
                -- Откатываем старую транзакцию
                IF OLD.transaction_type = 'income' THEN
                    UPDATE accounts
                    SET balance = balance - OLD.amount
                    WHERE id = OLD.account_id;
                ELSIF OLD.transaction_type = 'expense' THEN
                    UPDATE accounts
                    SET balance = balance + OLD.amount
                    WHERE id = OLD.account_id;
                ELSIF OLD.transaction_type = 'transfer' THEN
                    UPDATE accounts
                    SET balance = balance + OLD.amount
                    WHERE id = OLD.account_id;
                    UPDATE accounts
                    SET balance = balance - OLD.amount
                    WHERE id = OLD.transfer_to_account_id;
                END IF;

                -- Применяем новую транзакцию
                IF NEW.transaction_type = 'income' THEN
                    UPDATE accounts
                    SET balance = balance + NEW.amount
                    WHERE id = NEW.account_id;
                ELSIF NEW.transaction_type = 'expense' THEN
                    UPDATE accounts
                    SET balance = balance - NEW.amount
                    WHERE id = NEW.account_id;
                ELSIF NEW.transaction_type = 'transfer' THEN
                    UPDATE accounts
                    SET balance = balance - NEW.amount
                    WHERE id = NEW.account_id;
                    UPDATE accounts
                    SET balance = balance + NEW.amount
                    WHERE id = NEW.transfer_to_account_id;
                END IF;
            END IF;
        END IF;

        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;

    -- Создание триггера
    CREATE TRIGGER transaction_balance_trigger
    AFTER INSERT OR UPDATE OR DELETE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_account_balance();
    """

    try:
        with psycopg2.connect(**connection_params) as target_conn:
            with target_conn.cursor() as target_cursor:
                # Выполняем скрипт
                target_cursor.execute(create_trigger_script)
                target_conn.commit()
        print("Триггер для обновления баланса счетов успешно создан.")
    except Error as e:
        print(f"Ошибка при создании триггера: {e}")
        raise
