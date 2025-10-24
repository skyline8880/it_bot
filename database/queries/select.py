from secrets.secrets import Secrets

from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.zone import Zone
from database.tables.status import Status


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
