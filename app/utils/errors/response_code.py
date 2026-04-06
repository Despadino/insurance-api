from enum import Enum

from fastapi import status


class CustomCodeBase(Enum):
    """Базовый класс пользовательскоих кодов состояния"""

    @property
    def http_code(self):
        """
        Получить код ошибки http
        """
        return self.value[0]

    @property
    def code(self):
        """
        Получить код статуса
        """
        return self.value[1]

    @property
    def msg(self):
        """
        Получить информацию о коде состояния
        """
        return self.value[2]


class CustomErrorCode(CustomCodeBase):
    """Пользовательский код состояния ошибки"""

    HTTP_401_UNAUTHORIZED = (
        status.HTTP_401_UNAUTHORIZED,
        40100,
        "Неавторизован",
    )

    HTTP_403_FORBIDDEN = (
        status.HTTP_403_FORBIDDEN,
        40300,
        "Недостаточно прав или недействительный пользователь",
    )

    HTTP_404_NOT_FOUND = (
        status.HTTP_404_NOT_FOUND,
        40400,
        "Не найден",
    )

    HTTP_409_CONFLICT = (
        status.HTTP_409_CONFLICT,
        40900,
        "Невозможно создать ",
    )

    HTTP_500_INTERNAL_SERVER_ERROR = (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        50000,
        "Неизвестная ошибка. Обратитесь к разработчикам",
    )
