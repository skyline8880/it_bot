from database.database import Database


db = Database()

con, cur = db.get_connection_and_cursor()

data = cur.execute(
"""
SELECT  
    id,
    create_date,
    department_id,
    floor,
    zone_id,
    btype_id,
    message_id,
    telegram_id
FROM it.request
""")
for line in data.fetchall():
    print(line)