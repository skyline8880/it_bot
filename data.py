from database.database import Database


db = Database()

con, cur = db.get_connection_and_cursor()
""" cur.execute(
    "DELETE FROM it.department WHERE id = -1"
)

con.commit() """
data = cur.execute(
"""
SELECT  
    id,
    name
FROM it.department
""")
for line in data.fetchall():
    print(line)

