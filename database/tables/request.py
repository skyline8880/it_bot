class Request:
    ID = "id"
    CREATE_DATE = "create_date"
    DEPARTMENT_ID = "department_id"
    FLOOR_ID = "floor"
    ZONE_ID = "zone_id"
    BTYPE_ID = "btype_id"
    MESSAGE_ID = "message_id"
    CREATOR = "telegram_id"
    DESCRIPTION = "description"
    FILEID = "file_id"
    STATUS_ID = "status_id"
    EXECUTOR_ID = "executor_id"

    def __str__(self) -> str:
        return "request"
