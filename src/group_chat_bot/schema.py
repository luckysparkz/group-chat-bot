SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_full_name TEXT NOT NULL,
    content TEXT NOT NULL,
    sent_at INT NOT NULL
)
"""
