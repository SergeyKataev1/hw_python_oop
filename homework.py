import sys
from typing import Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: float = 60
    action: float = None

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = type(self).__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed: float = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:  # не трогать по ТЗ
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        self.get_distance()
        self.get_mean_speed()
        self.get_spent_calories()
        self.info = InfoMessage(self.training_type,
                                self.duration,
                                self.distance_km,
                                self.mean_speed,
                                self.get_spent_calories())
        return self.info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    MIN_IN_H: float = 60

    def get_spent_calories(self) -> float:
        duration_time: float = self.duration * self.MIN_IN_H
        self.calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                * self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SHIFT)
                                * self.weight / self.M_IN_KM
                                * duration_time)
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    MIN_IN_H: float = 60
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_time: float = self.duration * self.MIN_IN_H
        speed_in_ms: float = self.get_mean_speed() * self.KMH_IN_MSEC
        height_m: float = self.height / self.CM_IN_M
        self.calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                 * self.weight + (speed_in_ms**2 / height_m)
                                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                 * self.weight) * duration_time)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_WEIGHT_MULTIPLIER: int = 2
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.mean_speed: float = (self.length_pool * self.count_pool
                                  / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.get_mean_speed()
                                + self.MEAN_SPEED_MULTIPLIER)
                                * self.CALORIES_MEAN_WEIGHT_MULTIPLIER
                                * self.weight * self.duration)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_types:
        return sys.exit('Не удалось определить вид тренировки, приятного дня.')
    else:
        return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('ERR', [1000, 1000, 1000, 1000])  # тестовые ошибочные данные
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
