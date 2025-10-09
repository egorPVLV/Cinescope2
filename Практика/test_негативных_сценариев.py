import pytest
import requests
from constants import BASE_URL
from faker import Faker

faker = Faker()


class TestBookings:
    def test_negative_booking(self, auth_session, booking_data):
        # Создаём бронирование c ошибкой
        new_booking_data = booking_data.copy()
        new_booking_data.update({
            "firstname": 2})

        create_booking = auth_session.post(f"{BASE_URL}/booking", json=new_booking_data)
        assert create_booking.status_code == 500, "Здесь должен быть 500 код"

        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"


        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"




        #Обновляем бронирование с пустым значением
        new_booking_data = {}

        print()
        print(create_booking.json()['booking'])
        get_patch_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=new_booking_data)
        assert get_patch_booking.status_code == 400, "Здесь должен быть 400 код"
        # print(get_patch_booking.json())




        # Проверяем, что бронирование можно получить по ID
        get_patch_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_patch_booking.status_code == 200, "Бронь не найдена"
        # Проверяем, что все значения обновились
        for key in new_booking_data: # Без цикла проверяет за 2,5 сек. С циклом так же.
            assert get_patch_booking.json()[key] == new_booking_data[key], "Заданная фамилия не совпадает"



        # Удаляем бронирование без авторизации
        deleted_booking = requests.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 403, 'Не должно быть доступа на удаление'


        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_patch_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_patch_booking.status_code == 404, "Бронь не удалилась"
