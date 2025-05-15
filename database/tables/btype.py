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
        self.emptablet = "Планшет для сотрудников"
        self.eclock = "Электронные часы"
        self.treader = "Считыватель полотенец"
        self.solar = "Солярий (планшет)"

    def __str__(self) -> str:
        return "btype"
