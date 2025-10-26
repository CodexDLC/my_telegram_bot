

CREATE TRIGGER IF NOT EXISTS trg_users_update_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users
    SET updated_at = CURRENT_TIMESTAMP
    WHERE user_id = OLD.user_id;
END;


CREATE TRIGGER IF NOT EXISTS trg_context_update_timestamp
AFTER UPDATE ON context
FOR EACH ROW
BEGIN
    UPDATE context
    SET updated_at = CURRENT_TIMESTAMP
    WHERE message_id = OLD.message_id;
END;