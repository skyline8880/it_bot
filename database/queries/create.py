from secrets.secrets import Secrets

from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.status import Status
from database.tables.zone import Zone

CREATE = f"""
    CREATE SCHEMA IF NOT EXISTS {Secrets.SCHEMA_NAME};

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Department()} (
        {Department.ID} SERIAL,
        {Department.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Floor()} (
        {Floor.ID} SERIAL,
        {Floor.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Zone()} (
        {Zone.ID} SERIAL,
        {Zone.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Btype()} (
        {Btype.ID} SERIAL,
        {Btype.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Status()} (
        {Status.ID} SERIAL,
        {Status.NAME} VARCHAR(250) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Employee()} (
        {Employee.ID} SERIAL,
        {Employee.ISADMIN} BOOLEAN DEFAULT FALSE,
        {Employee.PHONE} VARCHAR(15) NOT NULL UNIQUE,
        {Employee.TELEGRAM_ID} BIGINT NOT NULL,
        {Employee.FULLNAME} VARCHAR(350) DEFAULT NULL,
        {Employee.USERNAME} VARCHAR(350) DEFAULT NULL,
        {Employee.ISEXECUTOR} BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS {Secrets.SCHEMA_NAME}.{Request()} (
        {Request.ID} SERIAL,
        {Request.CREATE_DATE} TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        {Request.DEPARTMENT_ID} SMALLINT NOT NULL,
        {Request.FLOOR_ID} SMALLINT NOT NULL,
        {Request.ZONE_ID} SMALLINT NOT NULL,
        {Request.BTYPE_ID} SMALLINT NOT NULL,
        {Request.MESSAGE_ID} BIGINT NOT NULL,
        {Request.CREATOR} BIGINT NOT NULL,
        {Request.DESCRIPTION} VARCHAR(2000) DEFAULT NULL,
        {Request.FILEID} VARCHAR(1000) DEFAULT NULL,
        {Request.STATUS_ID} SMALLINT NOT NULL DEFAULT 1,
        {Request.EXECUTOR_ID} BIGINT,
        PRIMARY KEY ({Request.MESSAGE_ID}, {Request.CREATOR})
    );
"""
