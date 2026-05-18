import sqlite3

conn = sqlite3.connect("database/weather.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    humidity REAL,
    weather TEXT,
    wind_speed REAL
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")