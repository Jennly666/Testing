"""
Простые тесты для демонстрации black-box тестирования
Тестируем функцию валидации имени пользователя напрямую
"""

import pytest


def validate_username(username: str) -> dict:
    """
    Простая функция валидации имени пользователя для black-box тестирования
    """
    errors = []
    
    # Проверка на пустоту
    if not username or username.strip() == "":
        errors.append("Имя пользователя не может быть пустым")
        return {"valid": False, "errors": errors}
    
    # Проверка длины
    if len(username) < 2:
        errors.append("Имя пользователя должно содержать минимум 2 символа")
    elif len(username) > 30:
        errors.append("Имя пользователя не должно превышать 30 символов")
    
    # Проверка на только цифры
    if username.isdigit():
        errors.append("Имя пользователя не может состоять только из цифр")
    
    # Проверка на алфавитно-цифровые символы
    if not username.isalnum():
        errors.append("Имя пользователя должно содержать только буквы и цифры")
    
    return {"valid": len(errors) == 0, "errors": errors}


class TestUsernameValidationBlackBox:
    """Black-box тесты для функции validate_username"""
    
    def test_valid_usernames_ec1(self):
        """
        Эквивалентный класс EC1: Валидные имена пользователей
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
            result = validate_username(username)
            assert result["valid"] == True, f"Валидное имя '{username}' не прошло валидацию: {result['errors']}"
            assert len(result["errors"]) == 0

    def test_empty_usernames_ec2(self):
        """
        Эквивалентный класс EC2: Пустые значения
        """
        empty_usernames = ["", "   ", "  "]
        
        for username in empty_usernames:
            result = validate_username(username)
            assert result["valid"] == False
            assert any("пустым" in error for error in result["errors"])

    def test_numeric_only_usernames_ec3(self):
        """
        Эквивалентный класс EC3: Только цифры
        """
        numeric_usernames = ["123", "999", "12345678"]
        
        for username in numeric_usernames:
            result = validate_username(username)
            assert result["valid"] == False
            assert any("только из цифр" in error for error in result["errors"])

    def test_special_characters_ec4(self):
        """
        Эквивалентный класс EC4: Содержат специальные символы
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
            result = validate_username(username)
            assert result["valid"] == False
            assert any("буквы и цифры" in error for error in result["errors"])

    def test_boundary_values(self):
        """
        Тестирование граничных значений
        """
        # BV1: Минимальная длина (2 символа)
        result = validate_username("ab")
        assert result["valid"] == True
        
        # BV2: Слишком короткое (1 символ)
        result = validate_username("a")
        assert result["valid"] == False
        assert any("минимум 2 символа" in error for error in result["errors"])
        
        # BV3: Максимальная длина (30 символов)
        long_name = "a" * 30
        result = validate_username(long_name)
        assert result["valid"] == True
        
        # BV4: Превышение максимальной длины (31 символ)
        too_long_name = "a" * 31
        result = validate_username(too_long_name)
        assert result["valid"] == False
        assert any("30 символов" in error for error in result["errors"])
        
        # BV5: Только одна цифра
        result = validate_username("1")
        assert result["valid"] == False
        # Должно быть две ошибки: длина и только цифры
        assert len(result["errors"]) >= 1

    def test_edge_cases(self):
        """
        Дополнительные крайние случаи
        """
        # Смешанные символы с цифрами в начале
        result = validate_username("1abc")
        assert result["valid"] == True
        
        # Смешанные символы с цифрами в конце
        result = validate_username("abc1")
        assert result["valid"] == True
        
        # Только буквы
        result = validate_username("abc")
        assert result["valid"] == True

    def test_summary_table(self):
        """
        Демонстрация результатов тестирования в табличном виде
        """
        test_cases = [
            ("user123", True, "EC1"),
            ("TestUser", True, "EC1"), 
            ("", False, "EC2"),
            ("123", False, "EC3"),
            ("user@123", False, "EC4"),
            ("test_user", False, "EC4"),
            ("ab", True, "BV1"),
            ("a", False, "BV2"),
            ("a" * 30, True, "BV3"),
            ("a" * 31, False, "BV4")
        ]
        
        print("\n=== РЕЗУЛЬТАТЫ BLACK-BOX ТЕСТИРОВАНИЯ ===")
        print("| Тест | Входные данные | Ожидаемый результат | Фактический результат | Класс | Статус |")
        print("|------|----------------|-------------------|---------------------|-------|--------|")
        
        all_passed = True
        for i, (input_data, expected_valid, test_class) in enumerate(test_cases, 1):
            result = validate_username(input_data)
            actual_valid = result["valid"]
            
            expected_str = "Успех" if expected_valid else "Ошибка"
            actual_str = "Успех" if actual_valid else "Ошибка"
            status = "✅ PASS" if expected_valid == actual_valid else "❌ FAIL"
            
            if expected_valid != actual_valid:
                all_passed = False
            
            # Обрезаем длинные входные данные для таблицы
            display_input = input_data if len(input_data) <= 10 else input_data[:7] + "..."
            
            print(f"| T{i:2}  | {display_input:<14} | {expected_str:<17} | {actual_str:<19} | {test_class:<5} | {status:<6} |")
        
        print(f"\n{'='*80}")
        print(f"ИТОГО: {'ВСЕ ТЕСТЫ ПРОШЛИ' if all_passed else 'ЕСТЬ ОШИБКИ'}")
        print(f"{'='*80}")
        
        assert all_passed, "Не все тесты прошли успешно"


class TestWhiteBoxSimple:
    """Простой white-box тест для демонстрации покрытия путей"""
    
    def test_all_paths_coverage(self):
        """
        Тест покрытия всех путей в функции validate_username
        
        Пути:
        1. Пустое имя -> return False
        2. Короткое имя -> добавить ошибку
        3. Длинное имя -> добавить ошибку  
        4. Только цифры -> добавить ошибку
        5. Спец. символы -> добавить ошибку
        6. Валидное имя -> return True
        """
        
        # Путь 1: Пустое имя
        result = validate_username("")
        assert not result["valid"]
        assert "пустым" in result["errors"][0]
        
        # Путь 2: Короткое имя
        result = validate_username("a")
        assert not result["valid"]
        assert any("минимум 2" in error for error in result["errors"])
        
        # Путь 3: Длинное имя
        result = validate_username("a" * 31)
        assert not result["valid"]
        assert any("30 символов" in error for error in result["errors"])
        
        # Путь 4: Только цифры
        result = validate_username("123")
        assert not result["valid"]
        assert any("только из цифр" in error for error in result["errors"])
        
        # Путь 5: Спец. символы
        result = validate_username("user@123")
        assert not result["valid"]
        assert any("буквы и цифры" in error for error in result["errors"])
        
        # Путь 6: Валидное имя
        result = validate_username("user123")
        assert result["valid"]
        assert len(result["errors"]) == 0
        
        print("✅ Все пути функции validate_username покрыты тестами")


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])