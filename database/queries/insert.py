from secrets.secrets import Secrets

from database.tables.employee import Employee
from database.tables.request import Request

INSERT_INTO_EMPLOYEE = f"""
    INSERT INTO {Secrets.SCHEMA_NAME}.{Employee()} (
        {Employee().PHONE},
        {Employee().TELEGRAM_ID},
        {Employee().FULLNAME},
        {Employee().USERNAME}
    )
    VALUES (
        %({Employee().PHONE})s,
        %({Employee().TELEGRAM_ID})s,
        %({Employee().FULLNAME})s,
        %({Employee().USERNAME})s
    )
    ON CONFLICT ({Employee().PHONE}) DO UPDATE
        SET {Employee().TELEGRAM_ID} = %({Employee().TELEGRAM_ID})s,
            {Employee().FULLNAME} = %({Employee().FULLNAME})s,
            {Employee().USERNAME} = %({Employee().USERNAME})s
    RETURNING
        {Employee().ID},
        {Employee().ISADMIN},
        {Employee().PHONE},
        {Employee().TELEGRAM_ID},
        {Employee().FULLNAME},
        {Employee().USERNAME};
"""
INSERT_INTO_REQUEST = f"""
    INSERT INTO {Secrets.SCHEMA_NAME}.{Request()} (
        {Request().DEPARTMENT_ID},
        {Request().FLOOR_ID},
        {Request().ZONE_ID},
        {Request().BTYPE_ID},
        {Request().MESSAGE_ID},
        {Request().CREATOR},
        {Request().DESCRIPTION},
        {Request().FILEID}
    )
    VALUES (
        %({Request().DEPARTMENT_ID})s,
        %({Request().FLOOR_ID})s,
        %({Request().ZONE_ID})s,
        %({Request().BTYPE_ID})s,
        %({Request().MESSAGE_ID})s,
        %({Request().CREATOR})s,
        %({Request().DESCRIPTION})s,
        %({Request().FILEID})s
    )
    ON CONFLICT ({Request().MESSAGE_ID}, {Request().CREATOR}) DO UPDATE
        SET {Request().DEPARTMENT_ID} = %({Request().DEPARTMENT_ID})s,
            {Request().FLOOR_ID} = %({Request().FLOOR_ID})s,
            {Request().ZONE_ID} = %({Request().ZONE_ID})s,
            {Request().BTYPE_ID} = %({Request().BTYPE_ID})s,
            {Request().DESCRIPTION} = %({Request().DESCRIPTION})s,
            {Request().FILEID} = %({Request().FILEID})s
    RETURNING
        {Request().MESSAGE_ID},
        {Request().CREATOR};
"""
