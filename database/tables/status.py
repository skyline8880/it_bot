class Status:
    ID = "id"
    NAME = "name"

    def __init__(self) -> None:
        self.new = "Новый"
        self.in_process = "В работе"
        self.done = "Завершен"

    def __str__(self) -> str:
        return "status"
