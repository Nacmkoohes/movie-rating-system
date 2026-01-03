from sqlalchemy.orm import text
from app.db.session import engine

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")).scalar()
    print("DB OK:", result)
