class Zone:
    ID = "id"
    NAME = "name"

    def __init__(self) -> None:
        self.salesdep = "Отдел продаж"
        self.servdep = "Отдел заботы"
        self.reciep = "Рецепция"
        self.hall = "Холл"
        self.bar = "Бар"
        self.cash = "Касса"
        self.kidclub = "Детский клуб"
        self.locker = "Раздевалки"
        self.gym = "Тренажерный зал"
        self.spa = "СПА"
        self.marts = "Клуб единоборств"
        self.shower = "Банный комплекс"
        self.ant = "Антресоль"
        self.tech = "Техническая зона"
        self.pool = "Бассейн"

    def __str__(self) -> str:
        return "zone"
