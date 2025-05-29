import psycopg2
from psycopg2 import Error

def balance_trigger_insert(connection_params: dict):
    create_trigger_script = """
    -- Создание типа ENUM, если он ещё не существует
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transactiontype') THEN
            CREATE TYPE transactiontype AS ENUM ('INCOME', 'EXPENSE', 'TRANSFER');
        END IF;
    END;
    $$;
    
    
    -- Переименование поля initial_balance → balance, если необходимо
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'accounts'
              AND column_name = 'initial_balance'
        ) THEN
            EXECUTE 'ALTER TABLE accounts RENAME COLUMN initial_balance TO balance';
        END IF;
    END;
    $$;
    
    
    -- Функция: обработка вставки транзакции
    CREATE OR REPLACE FUNCTION trg_transaction_insert()
    RETURNS TRIGGER AS $$
    BEGIN
        IF NEW.transaction_type = 'INCOME' THEN
            UPDATE accounts SET balance = balance + NEW.amount
            WHERE id = NEW.account_id;
    
        ELSIF NEW.transaction_type = 'EXPENSE' THEN
            UPDATE accounts SET balance = balance - NEW.amount
            WHERE id = NEW.account_id;
    
        ELSIF NEW.transaction_type = 'TRANSFER' THEN
            UPDATE accounts SET balance = balance - NEW.amount
            WHERE id = NEW.account_id;
    
            UPDATE accounts SET balance = balance + NEW.amount
            WHERE id = NEW.transfer_to_account_id;
        END IF;
    
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    
    -- Функция: обработка удаления транзакции
    CREATE OR REPLACE FUNCTION trg_transaction_delete()
    RETURNS TRIGGER AS $$
    BEGIN
        IF OLD.transaction_type = 'INCOME' THEN
            UPDATE accounts SET balance = balance - OLD.amount
            WHERE id = OLD.account_id;
    
        ELSIF OLD.transaction_type = 'EXPENSE' THEN
            UPDATE accounts SET balance = balance + OLD.amount
            WHERE id = OLD.account_id;
    
        ELSIF OLD.transaction_type = 'TRANSFER' THEN
            UPDATE accounts SET balance = balance + OLD.amount
            WHERE id = OLD.account_id;
    
            UPDATE accounts SET balance = balance - OLD.amount
            WHERE id = OLD.transfer_to_account_id;
        END IF;
    
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    
    
    -- Функция: обработка изменения транзакции
    CREATE OR REPLACE FUNCTION trg_transaction_update()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Только если важные поля изменились
        IF NEW.account_id != OLD.account_id OR
           NEW.transfer_to_account_id IS DISTINCT FROM OLD.transfer_to_account_id OR
           NEW.amount != OLD.amount OR
           NEW.transaction_type != OLD.transaction_type THEN
    
            -- Откатываем старые изменения
            IF OLD.transaction_type = 'INCOME' THEN
                UPDATE accounts SET balance = balance - OLD.amount
                WHERE id = OLD.account_id;
    
            ELSIF OLD.transaction_type = 'EXPENSE' THEN
                UPDATE accounts SET balance = balance + OLD.amount
                WHERE id = OLD.account_id;
    
            ELSIF OLD.transaction_type = 'TRANSFER' THEN
                UPDATE accounts SET balance = balance + OLD.amount
                WHERE id = OLD.account_id;
    
                UPDATE accounts SET balance = balance - OLD.amount
                WHERE id = OLD.transfer_to_account_id;
            END IF;
    
            -- Применяем новые
            IF NEW.transaction_type = 'INCOME' THEN
                UPDATE accounts SET balance = balance + NEW.amount
                WHERE id = NEW.account_id;
    
            ELSIF NEW.transaction_type = 'EXPENSE' THEN
                UPDATE accounts SET balance = balance - NEW.amount
                WHERE id = NEW.account_id;
    
            ELSIF NEW.transaction_type = 'TRANSFER' THEN
                UPDATE accounts SET balance = balance - NEW.amount
                WHERE id = NEW.account_id;
    
                UPDATE accounts SET balance = balance + NEW.amount
                WHERE id = NEW.transfer_to_account_id;
            END IF;
        END IF;
    
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    
    -- Создание триггеров
    
    -- INSERT
    CREATE TRIGGER trg_on_transaction_insert
    AFTER INSERT ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION trg_transaction_insert();
    
    -- DELETE
    CREATE TRIGGER trg_on_transaction_delete
    AFTER DELETE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION trg_transaction_delete();
    
    -- UPDATE
    CREATE TRIGGER trg_on_transaction_update
    AFTER UPDATE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION trg_transaction_update();

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
