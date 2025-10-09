import pytest
from constants import BASE_URL
from faker import Faker

faker = Faker()


class TestBookings:
    def test_put_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"


        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"


        new_booking_data = {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }



        print()
        print(create_booking.json()['booking'])
        get_put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=new_booking_data)
        print(get_put_booking.json())

        # Проверяем, что бронирование можно получить по ID
        get_put_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_put_booking.status_code == 200, "Бронь не найдена"
        # Проверяем, что все значения обновились
        for key in new_booking_data: # Без цикла проверяет за 2,5 сек. С циклом так же.
            assert get_put_booking.json()[key] == new_booking_data[key], "Заданная фамилия не совпадает"


        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_put_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_put_booking.status_code == 404, "Бронь не удалилась"
