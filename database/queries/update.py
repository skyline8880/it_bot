from secrets.secrets import Secrets

from database.tables.employee import Employee

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
