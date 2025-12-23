from secrets.secrets import Secrets

from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.status import Status
from database.tables.zone import Zone

SELECT_DEPARTMENTS = f"""
    SELECT
        {Department().ID},
        {Department().NAME}
    FROM {Secrets.SCHEMA_NAME}.{Department()};
"""
SELECT_DEPARTMENT_BY_SIGN = f"""
    SELECT
        {Department().ID},
        {Department().NAME}
    FROM {Secrets.SCHEMA_NAME}.{Department()}
    WHERE {Department().ID}::VARCHAR = %(sign)s
    OR {Department().NAME}::VARCHAR = %(sign)s;
"""
SELECT_FLOOR_BY_SIGN = f"""
    SELECT
        {Floor().ID},
        {Floor().NAME}
    FROM {Secrets.SCHEMA_NAME}.{Floor()}
    WHERE {Floor().ID}::VARCHAR = %(sign)s
    OR {Floor().NAME}::VARCHAR = %(sign)s;
"""
SELECT_ZONE_BY_SIGN = f"""
    SELECT
        {Zone().ID},
        {Zone().NAME}
    FROM {Secrets.SCHEMA_NAME}.{Zone()}
    WHERE {Zone().ID}::VARCHAR = %(sign)s
    OR {Zone().NAME}::VARCHAR = %(sign)s;
"""
SELECT_BTYPE_BY_SIGN = f"""
    SELECT
        {Btype().ID},
        {Btype().NAME}
    FROM {Secrets.SCHEMA_NAME}.{Btype()}
    WHERE {Btype().ID}::VARCHAR = %(sign)s
    OR {Btype().NAME}::VARCHAR = %(sign)s;
"""
SELECT_EMPLOYEE_BY_SIGN = f"""
    SELECT
        {Employee().ID},
        {Employee().ISADMIN},
        {Employee().PHONE},
        {Employee().TELEGRAM_ID},
        {Employee().FULLNAME},
        {Employee().USERNAME},
        {Employee().ISEXECUTOR}
    FROM {Secrets.SCHEMA_NAME}.{Employee()}
    WHERE {Employee().PHONE}::VARCHAR = %(sign)s
    OR {Employee().TELEGRAM_ID}::VARCHAR = %(sign)s;
"""
SELECT_REQUEST_BY_SIGN = f"""
    WITH current_request AS (
        SELECT
            {Request().ID},
            {Request().CREATE_DATE},
            {Request().DEPARTMENT_ID},
            {Request().FLOOR_ID},
            {Request().ZONE_ID},
            {Request().BTYPE_ID},
            {Request().MESSAGE_ID},
            {Request().CREATOR},
            {Request().DESCRIPTION},
            {Request().FILEID},
            {Request().STATUS_ID},
            {Request().EXECUTOR_ID}
        FROM {Secrets.SCHEMA_NAME}.{Request()}
        WHERE {Request().MESSAGE_ID} = %({Request().MESSAGE_ID})s
        AND {Request().CREATOR} = %({Request().CREATOR})s)
    SELECT
        crt.{Request().ID},
        crt.{Request().CREATE_DATE},
        crt.{Request().DEPARTMENT_ID},
        dp.{Department().NAME},
        crt.{Request().FLOOR_ID},
        fl.{Floor().NAME},
        crt.{Request().ZONE_ID},
        zn.{Zone().NAME},
        crt.{Request().BTYPE_ID},
        bt.{Btype().NAME},
        crt.{Request().MESSAGE_ID},
        crt.{Request().CREATOR},
        cemp.{Employee().ID},
        cemp.{Employee().ISADMIN},
        cemp.{Employee().PHONE},
        cemp.{Employee().FULLNAME},
        cemp.{Employee().USERNAME},
        crt.{Request().DESCRIPTION},
        crt.{Request().FILEID},
        sts.{Status().ID},
        sts.{Status().NAME},
        eemp.{Employee().ID},
        eemp.{Employee().ISADMIN},
        eemp.{Employee().PHONE},
        eemp.{Employee().FULLNAME},
        eemp.{Employee().USERNAME}
    FROM current_request AS crt
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Department()} AS dp
        ON crt.{Request().DEPARTMENT_ID} = dp.{Department().ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Floor()} AS fl
        ON crt.{Request().FLOOR_ID} = fl.{Floor().ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Zone()} AS zn
        ON crt.{Request().ZONE_ID} = zn.{Zone().ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Btype()} AS bt
        ON crt.{Request().BTYPE_ID} = bt.{Btype().ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Employee()} AS cemp
        ON crt.{Request().CREATOR} = cemp.{Employee().TELEGRAM_ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Status()} AS sts
        ON crt.{Request().STATUS_ID} = sts.{Status().ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Employee()} AS eemp
        ON crt.{Request().EXECUTOR_ID} = eemp.{Employee().TELEGRAM_ID};
"""
SELECT_STATISTICS = f"""
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
SELECT_ADMINS = f"""
SELECT
    --{Employee().TELEGRAM_ID},
    {Employee().PHONE},
    COALESCE({Employee().FULLNAME}, 'Не указано'),
    COALESCE({Employee().USERNAME}, 'Не указано')
FROM {Secrets.SCHEMA_NAME}.{Employee()}
WHERE {Employee().ISADMIN} = TRUE
ORDER BY {Employee().ID};
"""
SELECT_EXECUTORS = f"""
SELECT
    --{Employee().TELEGRAM_ID},
    {Employee().PHONE},
    COALESCE({Employee().FULLNAME}, 'Не указано'),
    COALESCE({Employee().USERNAME}, 'Не указано')
FROM {Secrets.SCHEMA_NAME}.{Employee()}
WHERE {Employee().ISEXECUTOR} = TRUE
ORDER BY {Employee().ID};
"""
SELECT_CUSTOM_REQUESTS = f"""
WITH requests_by_status AS (
    SELECT
        {Request().ID},
        {Request().CREATE_DATE},
        {Request().DEPARTMENT_ID},
        {Request().FLOOR_ID},
        {Request().ZONE_ID},
        {Request().BTYPE_ID},
        {Request().MESSAGE_ID},
        {Request().CREATOR},
        {Request().DESCRIPTION},
        {Request().FILEID},
        {Request().STATUS_ID},
        {Request().EXECUTOR_ID}
    FROM {Secrets.SCHEMA_NAME}.{Request()}
    WHERE (0 = %({Request().STATUS_ID})s
            OR {Request().STATUS_ID} = %({Request().STATUS_ID})s)
        AND (0 = %({Request().DEPARTMENT_ID})s
                OR {Request().DEPARTMENT_ID} = %({Request().DEPARTMENT_ID})s)
        AND {Request().CREATE_DATE} BETWEEN %(sdate)s AND %(edate)s)
SELECT
    --rbs.{Request().ID},
    rbs.{Request().CREATE_DATE},
    --rbs.{Request().DEPARTMENT_ID},
    dp.{Department().NAME},
    --rbs.{Request().FLOOR_ID},
    fl.{Floor().NAME},
    --rbs.{Request().ZONE_ID},
    zn.{Zone().NAME},
    --rbs.{Request().BTYPE_ID},
    bt.{Btype().NAME},
    rbs.{Request().MESSAGE_ID},
    rbs.{Request().CREATOR},
    --cemp.{Employee().ID},
    --cemp.{Employee().ISADMIN},
    cemp.{Employee().PHONE},
    cemp.{Employee().FULLNAME},
    cemp.{Employee().USERNAME},
    rbs.{Request().DESCRIPTION},
    rbs.{Request().FILEID},
    --sts.{Status().ID},
    sts.{Status().NAME},
    --eemp.{Employee().ID},
    --eemp.{Employee().ISADMIN},
    eemp.{Employee().PHONE},
    eemp.{Employee().FULLNAME},
    eemp.{Employee().USERNAME}
FROM requests_by_status AS rbs
LEFT JOIN {Secrets.SCHEMA_NAME}.{Department()} AS dp
    ON rbs.{Request().DEPARTMENT_ID} = dp.{Department().ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Floor()} AS fl
    ON rbs.{Request().FLOOR_ID} = fl.{Floor().ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Zone()} AS zn
    ON rbs.{Request().ZONE_ID} = zn.{Zone().ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Btype()} AS bt
    ON rbs.{Request().BTYPE_ID} = bt.{Btype().ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Employee()} AS cemp
    ON rbs.{Request().CREATOR} = cemp.{Employee().TELEGRAM_ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Status()} AS sts
    ON rbs.{Request().STATUS_ID} = sts.{Status().ID}
LEFT JOIN {Secrets.SCHEMA_NAME}.{Employee()} AS eemp
    ON rbs.{Request().EXECUTOR_ID} = eemp.{Employee().TELEGRAM_ID};
"""
