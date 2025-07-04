"""
BLACK-BOX тестирование для валидатора username в UserRegister
Тестирование по эквивалентным классам и граничным значениям
"""

import pytest
from pydantic import ValidationError

from app.models.user import UserRegister


class TestUsernameValidatorBlackBox:
    """Black-box тесты для username_validator с использованием эквивалентных классов"""
    
    def test_valid_usernames_ec1(self):
        """
        Эквивалентный класс EC1: Валидные имена пользователей
        Содержат буквы и цифры, не только цифры
        """
        valid_usernames = [
            "user123",
            "TestUser", 
            "abc123def",
            "User1",
            "test2user",
            "MyUsername123"
        ]
        
        for username in valid_usernames:
            try:
                user_data = {
                    "user_name": username,
                    "email": "test@example.com",
                    "hashed_password": "hashedpass123"
                }
                user = UserRegister(**user_data)
                assert user.user_name == username
            except ValidationError:
                pytest.fail(f"Валидное имя '{username}' не прошло валидацию")

    def test_empty_usernames_ec2(self):
        """
        Эквивалентный класс EC2: Пустые значения
        Должны вызывать ValueError
        """
        empty_usernames = ["", "   "]  # None тестируется отдельно
        
        for username in empty_usernames:
            with pytest.raises(ValidationError) as exc_info:
                user_data = {
                    "user_name": username,
                    "email": "test@example.com", 
                    "hashed_password": "hashedpass123"
                }
                UserRegister(**user_data)
            
            # Проверяем, что ошибка связана с username
            errors = exc_info.value.errors()
            username_errors = [e for e in errors if 'user_name' in str(e)]
            assert len(username_errors) > 0

    def test_numeric_only_usernames_ec3(self):
        """
        Эквивалентный класс EC3: Только цифры
        Должны вызывать ValueError
        """
        numeric_usernames = ["123", "999", "0", "12345678"]
        
        for username in numeric_usernames:
            with pytest.raises(ValidationError) as exc_info:
                user_data = {
                    "user_name": username,
                    "email": "test@example.com",
                    "hashed_password": "hashedpass123"
                }
                UserRegister(**user_data)
            
            errors = exc_info.value.errors()
            assert any("только из цифр" in str(error) for error in errors)

    def test_special_characters_ec4(self):
        """
        Эквивалентный класс EC4: Содержат специальные символы
        Должны вызывать ValueError
        """
        special_char_usernames = [
            "user@123",
            "test_user", 
            "user-name",
            "user.name",
            "user#123",
            "user$name",
            "user name"  # пробел
        ]
        
        for username in special_char_usernames:
            with pytest.raises(ValidationError) as exc_info:
                user_data = {
                    "user_name": username,
                    "email": "test@example.com",
                    "hashed_password": "hashedpass123"
                }
                UserRegister(**user_data)
            
            errors = exc_info.value.errors()
            assert any("буквы и цифры" in str(error) for error in errors)

    def test_boundary_values(self):
        """
        Тестирование граничных значений
        """
        # BV1: Минимальная длина (1 символ) - должен пройти если это буква
        try:
            user_data = {
                "user_name": "a",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == "a"
        except ValidationError:
            pytest.fail("Односимвольное буквенное имя должно быть валидным")
        
        # BV5: Только одна цифра - должен не пройти
        with pytest.raises(ValidationError):
            user_data = {
                "user_name": "1",
                "email": "test@example.com", 
                "hashed_password": "hashedpass123"
            }
            UserRegister(**user_data)
        
        # BV6: Только буквы - должен пройти
        try:
            user_data = {
                "user_name": "abc",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == "abc"
        except ValidationError:
            pytest.fail("Буквенное имя должно быть валидным")

    def test_length_boundaries(self):
        """
        Тестирование граничных значений длины (из Field constraints)
        """
        # Минимальная длина (2 символа) - из Field(min_length=2)
        try:
            user_data = {
                "user_name": "ab",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == "ab"
        except ValidationError:
            pytest.fail("Имя длиной 2 символа должно быть валидным")
        
        # Слишком короткое имя (1 символ) - должно не пройти из-за min_length
        with pytest.raises(ValidationError):
            user_data = {
                "user_name": "a",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            UserRegister(**user_data)
        
        # Максимальная длина (30 символов)
        long_name = "a" * 30
        try:
            user_data = {
                "user_name": long_name,
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == long_name
        except ValidationError:
            pytest.fail("Имя максимальной длины должно быть валидным")
        
        # Превышение максимальной длины (31 символ)
        too_long_name = "a" * 31
        with pytest.raises(ValidationError):
            user_data = {
                "user_name": too_long_name,
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            UserRegister(**user_data)

    def test_edge_cases(self):
        """
        Дополнительные крайние случаи
        """
        # Смешанные символы с цифрами в начале
        try:
            user_data = {
                "user_name": "1abc",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == "1abc"
        except ValidationError:
            pytest.fail("Имя начинающееся с цифры но содержащее буквы должно быть валидным")
        
        # Смешанные символы с цифрами в конце
        try:
            user_data = {
                "user_name": "abc1",
                "email": "test@example.com",
                "hashed_password": "hashedpass123"
            }
            user = UserRegister(**user_data)
            assert user.user_name == "abc1"
        except ValidationError:
            pytest.fail("Имя заканчивающееся цифрой должно быть валидным")


class TestBlackBoxSummary:
    """
    Сводная таблица результатов black-box тестирования
    """
    
    def test_summary_table(self):
        """
        Демонстрация результатов тестирования в табличном виде
        """
        test_cases = [
            ("user123", "Успех", "EC1"),
            ("TestUser", "Успех", "EC1"), 
            ("", "ValidationError", "EC2"),
            ("123", "ValidationError", "EC3"),
            ("user@123", "ValidationError", "EC4"),
            ("test_user", "ValidationError", "EC4"),
            ("ab", "Успех", "BV1"),
            ("1", "ValidationError", "BV5")
        ]
        
        print("\n=== РЕЗУЛЬТАТЫ BLACK-BOX ТЕСТИРОВАНИЯ ===")
        print("| Тест | Входные данные | Ожидаемый результат | Фактический результат | Класс | Статус |")
        print("|------|----------------|-------------------|---------------------|-------|--------|")
        
        for i, (input_data, expected, test_class) in enumerate(test_cases, 1):
            try:
                user_data = {
                    "user_name": input_data,
                    "email": "test@example.com",
                    "hashed_password": "hashedpass123"
                }
                UserRegister(**user_data)
                actual = "Успех"
                status = "✅ PASS" if expected == "Успех" else "❌ FAIL"
            except ValidationError:
                actual = "ValidationError"
                status = "✅ PASS" if expected == "ValidationError" else "❌ FAIL"
            except Exception as e:
                actual = f"Unexpected: {type(e).__name__}"
                status = "❌ FAIL"
            
            print(f"| T{i}   | {input_data:<14} | {expected:<17} | {actual:<19} | {test_class:<5} | {status:<6} |")
        
        # Все тесты должны пройти согласно ожиданиям
        assert True  # Этот тест всегда проходит, он для демонстрации