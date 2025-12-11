from faker import Faker
fake = Faker()

# Генерация простых данных
print(fake.name())
print(fake.address())
print()

fake_ru = Faker('ru_RU')
print(fake_ru.name())
print(fake_ru.address())
print(fake_ru.email())
print(fake_ru.phone_number())
print(fake_ru.date_of_birth())
print(fake_ru.snils())
print()
print(fake_ru.passport_number())
print(fake_ru.passport_owner())





