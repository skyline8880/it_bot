from secrets.secrets import Secrets

from database.database import Database
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.status import Status
from database.tables.zone import Zone

db = Database()

con, cur = db.get_connection_and_cursor()
#data = cur.execute(
#"""
#ALTER TABLE it.request
#ADD status_id SMALLINT NOT NULL DEFAULT 1;
#""")
#
#print(data)
#data = cur.execute(
#"""
#ALTER TABLE it.request
#ADD executor_id BIGINT;
#""")
#
#print(data)
#data = cur.execute(
#"""
#ALTER TABLE it.employee
#ADD is_executor BOOLEAN DEFAULT FALSE;
#""")
#print(data)
#con.commit()

res = cur.execute(
f"""
UPDATE it.request
    SET status_id = 3;
"""
)
con.commit()
print(res.statusmessage)
#print([col.name for col in res.description])
