from secrets.secrets import Secrets
from database.database import Database
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.zone import Zone
from database.tables.status import Status

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
WITH new_requests AS (
        SELECT
            {Request().DEPARTMENT_ID},
            COUNT({Request().ID})
        FROM {Secrets.SCHEMA_NAME}.{Request()}
        WHERE {Request().STATUS_ID} = 1
        GROUP BY {Request().DEPARTMENT_ID}
        ORDER BY {Request().DEPARTMENT_ID}),
    inwork_requests AS (
        SELECT
            {Request().DEPARTMENT_ID},
            COUNT({Request().ID})
        FROM {Secrets.SCHEMA_NAME}.{Request()}
        WHERE {Request().STATUS_ID} = 2
        GROUP BY {Request().DEPARTMENT_ID}
        ORDER BY {Request().DEPARTMENT_ID}),
    done_requests AS (
        SELECT
            {Request().DEPARTMENT_ID},
            COUNT({Request().ID})
        FROM {Secrets.SCHEMA_NAME}.{Request()}
        WHERE {Request().STATUS_ID} = 3
        GROUP BY {Request().DEPARTMENT_ID}
        ORDER BY {Request().DEPARTMENT_ID}),
    all_requests AS (
        SELECT
            {Request().DEPARTMENT_ID},
            COUNT({Request().ID})
        FROM {Secrets.SCHEMA_NAME}.{Request()}
        GROUP BY {Request().DEPARTMENT_ID}
        ORDER BY {Request().DEPARTMENT_ID})
SELECT
    dep.{Department().NAME} AS department,
    CASE
        WHEN nreq.count IS NULL THEN 0
        ELSE nreq.count
    END AS new,
    CASE
        WHEN ireq.count IS NULL THEN 0
        ELSE ireq.count
    END AS inwork,
    CASE
        WHEN dreq.count IS NULL THEN 0
        ELSE dreq.count
    END AS done,
    CASE
        WHEN areq.count IS NULL THEN 0
        ELSE areq.count
    END AS all
FROM {Secrets.SCHEMA_NAME}.{Department()} AS dep
LEFT JOIN new_requests AS nreq
    ON dep.id = nreq.department_id
LEFT JOIN inwork_requests AS ireq
    ON dep.id = ireq.department_id
LEFT JOIN done_requests AS dreq
    ON dep.id = dreq.department_id
LEFT JOIN all_requests AS areq
    ON dep.id = areq.department_id;
"""
)

print([col.name for col in res.description])
print(res.fetchall())
