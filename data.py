from typing import Union


class Departments:
    def __init__(self, department_id: Union[int, str]) -> None:
        self.department_id = int(department_id)
