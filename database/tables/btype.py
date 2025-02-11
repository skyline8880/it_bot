class Btype:
    ID = "id"
    NAME = "name"

    def __init__(self) -> None:
        self.network = "Интернет"
        self.pcs = "Компьютер"
        self.phone = "Телефония"
        self.tvs = "Телевизор"
        self.printer = "Принтер"
        self.elcash = "Электронный кассир"
        self.sound = "Музыка"
        self.tablet = "Планшет"
        self.accont = "СКУД"

    def __str__(self) -> str:
        return "btype"
