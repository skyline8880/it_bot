from secrets.secrets import Secrets

from database.tables.employee import Employee
from database.tables.request import Request

UPDATE_EMPLOYEE_USERNAME_FULLNAME = f"""
    UPDATE {Secrets.SCHEMA_NAME}.{Employee()}
        SET {Employee().FULLNAME} = %({Employee().FULLNAME})s,
            {Employee().USERNAME} = %({Employee().USERNAME})s
    WHERE {Employee().TELEGRAM_ID} = %({Employee().TELEGRAM_ID})s;
"""
UPDATE_EMPLOYEE_PHONE = f"""
    UPDATE {Secrets.SCHEMA_NAME}.{Employee()}
        SET {Employee().PHONE} = %({Employee().PHONE})s,
            {Employee().FULLNAME} = %({Employee().FULLNAME})s,
            {Employee().USERNAME} = %({Employee().USERNAME})s
    WHERE {Employee().TELEGRAM_ID} = %({Employee().TELEGRAM_ID})s;
"""
UPDATE_EMPLOYEE_IS_ADMIN = f"""
    UPDATE {Secrets.SCHEMA_NAME}.{Employee()}
        SET {Employee().ISADMIN} = %({Employee().ISADMIN})s,
            {Employee().ISEXECUTOR} = %({Employee().ISEXECUTOR})s
    WHERE {Employee().PHONE} = %({Employee().PHONE})s;
"""
UPDATE_EMPLOYEE_IS_EXECUTOR = f"""
    UPDATE {Secrets.SCHEMA_NAME}.{Employee()}
        SET {Employee().ISEXECUTOR} = %({Employee().ISEXECUTOR})s
    WHERE {Employee().PHONE} = %({Employee().PHONE})s;
"""
UPDATE_REQUEST_STATUS_AND_EXECUTOR = f"""
    UPDATE {Secrets.SCHEMA_NAME}.{Request()}
        SET {Request().STATUS_ID} = %({Request().STATUS_ID})s,
            {Request().EXECUTOR_ID} = %({Request().EXECUTOR_ID})s
    WHERE {Request().MESSAGE_ID} = %({Request().MESSAGE_ID})s
        AND {Request().CREATOR} = %({Request().CREATOR})s;
"""