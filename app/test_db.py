from app.database import engine

try:
    connection = engine.connect()
    print("✅ Supabase database connected successfully")
    connection.close()
except Exception as e:
    print("❌ Database connection failed")
    print(e)
