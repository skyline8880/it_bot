from secrets.secrets import Secrets

from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
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
        {Employee().USERNAME}
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
            {Request().FILEID}
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
        emp.{Employee().ID},
        emp.{Employee().ISADMIN},
        emp.{Employee().PHONE},
        emp.{Employee().FULLNAME},
        emp.{Employee().USERNAME},
        crt.{Request().DESCRIPTION},
        crt.{Request().FILEID}
    FROM current_request AS crt
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Department()} AS dp
        ON dp.{Department().ID} = crt.{Request().DEPARTMENT_ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Floor()} AS fl
        ON fl.{Floor().ID} = crt.{Request().FLOOR_ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Zone()} AS zn
        ON zn.{Zone().ID} = crt.{Request().ZONE_ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Btype()} AS bt
        ON bt.{Btype().ID} = crt.{Request().BTYPE_ID}
    LEFT JOIN {Secrets.SCHEMA_NAME}.{Employee()} AS emp
        ON emp.{Employee().TELEGRAM_ID} = crt.{Request().CREATOR};
"""
