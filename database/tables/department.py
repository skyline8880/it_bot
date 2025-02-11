class Department:
    ID = "id"
    NAME = "name"

    def __init__(self) -> None:
        self.msk = "Московский"
        self.vlk = "Волковский"
        self.nkr = "Некрасовка"
        self.btv = "Бyнинская"

    def __str__(self) -> str:
        return "department"
