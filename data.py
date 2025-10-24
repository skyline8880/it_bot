from database.database import Database


db = Database()

con, cur = db.get_connection_and_cursor()
data = cur.execute(
"""
ALTER TABLE it.request
ADD status_id SMALLINT NOT NULL DEFAULT 1;
""")

print(data)
data = cur.execute(
"""
ALTER TABLE it.request
ADD executor_id BIGINT;
""")

print(data)
data = cur.execute(
"""
ALTER TABLE it.employee
ADD is_executor BOOLEAN DEFAULT FALSE;
""")
print(data)
con.commit()

