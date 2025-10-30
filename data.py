from secrets.secrets import Secrets

from database.database import (INSERT_INTO_EMPLOYEE, UPDATE_EMPLOYEE_IS_ADMIN,
                               UPDATE_EMPLOYEE_IS_EXECUTOR, Database)
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
# (3, False, '79998185113', 228241435, 'Серëга (IBBQI)', '@IIBBQII', False)
# (2, False, '79258999734', 5204359462, 'ADMIN TELEGRAM OHANA', '@It_ohana', False)
""" for phone, telegram_id, fullname, username in [
    [79856955202, 1229595123, 'Nikolay', '@Nikolaybboy'],
    [79776611341, 5693627941, '𝒱𝓁𝒶𝒹𝒾𝓈𝓁𝒶𝓋', '@vl_13_m'],
    [79266153646, 477613350, 'Alexander Avramenko', '@Alexander_a83'],
]:
    cur.execute(
        query=INSERT_INTO_EMPLOYEE,
        params={
            Employee().PHONE: str(phone),
            Employee().TELEGRAM_ID: telegram_id,
            Employee().FULLNAME: fullname,
            Employee().USERNAME: username,
        }
    )
    con.commit() """

for phone in [79856955202, 79776611341]:
    cur.execute(
        query=UPDATE_EMPLOYEE_IS_ADMIN,
        params={
            "phone": str(phone),
            "is_admin": True,
            "is_executor": True}
    )
con.commit()
""" for phone in [79856955202, 79776611341]:
    cur.execute(
        query=UPDATE_EMPLOYEE_IS_EXECUTOR,
        params={
            "phone": str(phone),
            "is_executor": True}
    )
con.commit() """
res = cur.execute(
"""
SELECT
    *
FROM it.employee
WHERE is_executor = TRUE
ORDER BY id;
"""
)
print(res.statusmessage)
print([col.name for col in res.description])

for line in res.fetchall():
    print(line)
