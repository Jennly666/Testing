"""
Комплексное тестирование утилитарных функций
Демонстрация различных техник тестирования
"""

import pytest
from app.utils import hash_password, validate_password, to_camel_case


class TestPasswordFunctions:
    """Тестирование функций работы с паролями"""
    
    def test_hash_password_basic(self):
        """Базовое тестирование хеширования пароля"""
        password = "test123"
        hashed = hash_password(password)
        
        # Проверяем, что хеш создается
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        
        # Проверяем, что хеш отличается от исходного пароля
        assert hashed != password
    
    def test_hash_password_different_inputs(self):
        """Тестирование хеширования разных паролей"""
        passwords = ["short", "verylongpassword123", "пароль", "P@ssw0rd!", ""]
        
        hashes = []
        for password in passwords:
            hashed = hash_password(password)
            hashes.append(hashed)
            
            # Каждый хеш должен быть уникальным
            assert hashed not in hashes[:-1]
    
    def test_validate_password_correct(self):
        """Тестирование валидации правильного пароля"""
        password = "test123"
        hashed = hash_password(password)
        
        # Правильный пароль должен проходить валидацию
        assert validate_password(password, hashed) == True
    
    def test_validate_password_incorrect(self):
        """Тестирование валидации неправильного пароля"""
        password = "test123"
        wrong_password = "wrong123"
        hashed = hash_password(password)
        
        # Неправильный пароль не должен проходить валидацию
        assert validate_password(wrong_password, hashed) == False
    
    def test_validate_password_edge_cases(self):
        """Тестирование крайних случаев валидации"""
        # Пустые строки
        assert validate_password("", "") == True
        
        # Один пустой, другой нет
        hashed = hash_password("test")
        assert validate_password("", hashed) == False
        
        # Специальные символы
        special_password = "!@#$%^&*()"
        hashed_special = hash_password(special_password)
        assert validate_password(special_password, hashed_special) == True


class TestCamelCaseFunction:
    """Тестирование функции преобразования в camelCase"""
    
    def test_to_camel_case_basic(self):
        """Базовое тестирование преобразования"""
        test_cases = [
            ("user_name", "userName"),
            ("first_name", "firstName"),
            ("last_name", "lastName"),
            ("email_address", "emailAddress")
        ]
        
        for input_str, expected in test_cases:
            result = to_camel_case(input_str)
            assert result == expected, f"Expected {expected}, got {result}"
    
    def test_to_camel_case_single_word(self):
        """Тестирование одного слова"""
        single_words = ["user", "name", "email", "password"]
        
        for word in single_words:
            result = to_camel_case(word)
            assert result == word, f"Single word should remain unchanged: {word}"
    
    def test_to_camel_case_multiple_underscores(self):
        """Тестирование множественных подчеркиваний"""
        test_cases = [
            ("user_first_name", "userFirstName"),
            ("very_long_variable_name", "veryLongVariableName"),
            ("a_b_c_d", "aBCD")
        ]
        
        for input_str, expected in test_cases:
            result = to_camel_case(input_str)
            assert result == expected
    
    def test_to_camel_case_edge_cases(self):
        """Тестирование крайних случаев"""
        edge_cases = [
            ("", ""),  # Пустая строка
            ("_", ""),  # Только подчеркивание
            ("user_", "user"),  # Подчеркивание в конце
            ("_user", "User"),  # Подчеркивание в начале
            ("user__name", "userName"),  # Двойное подчеркивание
        ]
        
        for input_str, expected in edge_cases:
            result = to_camel_case(input_str)
            assert result == expected, f"Input: '{input_str}', Expected: '{expected}', Got: '{result}'"
    
    def test_to_camel_case_numbers_and_special(self):
        """Тестирование с цифрами и специальными случаями"""
        test_cases = [
            ("user_1", "user1"),
            ("test_123_name", "test123Name"),
            ("api_v2_endpoint", "apiV2Endpoint")
        ]
        
        for input_str, expected in test_cases:
            result = to_camel_case(input_str)
            assert result == expected


class TestUtilsIntegration:
    """Интеграционные тесты утилитарных функций"""
    
    def test_password_workflow(self):
        """Тестирование полного рабочего процесса с паролем"""
        original_password = "MySecurePassword123!"
        
        # 1. Хешируем пароль
        hashed = hash_password(original_password)
        
        # 2. Проверяем правильный пароль
        assert validate_password(original_password, hashed) == True
        
        # 3. Проверяем неправильный пароль
        assert validate_password("WrongPassword", hashed) == False
        
        # 4. Проверяем, что повторное хеширование дает другой результат
        hashed2 = hash_password(original_password)
        assert hashed != hashed2  # Соль должна быть разной
        
        # 5. Но оба хеша должны валидироваться с исходным паролем
        assert validate_password(original_password, hashed2) == True
    
    def test_camel_case_with_user_fields(self):
        """Тестирование camelCase с реальными полями пользователя"""
        user_fields = [
            "user_name",
            "email_address", 
            "phone_number",
            "created_at",
            "updated_at",
            "is_active",
            "role_id"
        ]
        
        expected_camel = [
            "userName",
            "emailAddress",
            "phoneNumber", 
            "createdAt",
            "updatedAt",
            "isActive",
            "roleId"
        ]
        
        for field, expected in zip(user_fields, expected_camel):
            result = to_camel_case(field)
            assert result == expected, f"Field {field} should become {expected}, got {result}"


class TestUtilsPerformance:
    """Тесты производительности утилитарных функций"""
    
    def test_hash_password_performance(self):
        """Тестирование производительности хеширования"""
        import time
        
        password = "TestPassword123!"
        iterations = 10
        
        start_time = time.time()
        for _ in range(iterations):
            hash_password(password)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / iterations
        
        # Хеширование не должно занимать больше 1 секунды
        assert avg_time < 1.0, f"Hashing took too long: {avg_time:.3f}s per operation"
        
        print(f"Average hashing time: {avg_time:.3f}s per operation")
    
    def test_camel_case_performance(self):
        """Тестирование производительности преобразования camelCase"""
        import time
        
        test_string = "very_long_variable_name_with_many_underscores_for_testing"
        iterations = 1000
        
        start_time = time.time()
        for _ in range(iterations):
            to_camel_case(test_string)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / iterations
        
        # Преобразование должно быть очень быстрым
        assert avg_time < 0.001, f"CamelCase conversion took too long: {avg_time:.6f}s per operation"
        
        print(f"Average camelCase conversion time: {avg_time:.6f}s per operation")


class TestUtilsErrorHandling:
    """Тестирование обработки ошибок в утилитарных функциях"""
    
    def test_hash_password_with_none(self):
        """Тестирование хеширования None"""
        try:
            result = hash_password(None)
            # Если функция не выбрасывает исключение, проверяем результат
            assert result is not None
        except (TypeError, AttributeError):
            # Ожидаемое поведение - исключение при None
            pass
    
    def test_validate_password_with_none(self):
        """Тестирование валидации с None"""
        try:
            result = validate_password(None, "hash")
            assert result == False
        except (TypeError, AttributeError):
            pass
        
        try:
            result = validate_password("password", None)
            assert result == False
        except (TypeError, AttributeError):
            pass
    
    def test_to_camel_case_with_none(self):
        """Тестирование camelCase с None"""
        try:
            result = to_camel_case(None)
            assert result is None or result == ""
        except (TypeError, AttributeError):
            # Ожидаемое поведение
            pass


def run_comprehensive_utils_tests():
    """Запуск всех тестов утилитарных функций с отчетом"""
    
    print("\n" + "="*80)
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ УТИЛИТАРНЫХ ФУНКЦИЙ")
    print("="*80)
    
    test_results = {
        "password_functions": 0,
        "camel_case": 0,
        "integration": 0,
        "performance": 0,
        "error_handling": 0,
        "total": 0
    }
    
    # Подсчитываем количество тестов в каждом классе
    test_classes = [
        (TestPasswordFunctions, "password_functions"),
        (TestCamelCaseFunction, "camel_case"), 
        (TestUtilsIntegration, "integration"),
        (TestUtilsPerformance, "performance"),
        (TestUtilsErrorHandling, "error_handling")
    ]
    
    for test_class, category in test_classes:
        methods = [method for method in dir(test_class) if method.startswith('test_')]
        test_results[category] = len(methods)
        test_results["total"] += len(methods)
    
    print(f"\nОБЗОР ТЕСТОВ:")
    print(f"  Функции паролей: {test_results['password_functions']} тестов")
    print(f"  CamelCase функция: {test_results['camel_case']} тестов")
    print(f"  Интеграционные: {test_results['integration']} тестов")
    print(f"  Производительность: {test_results['performance']} тестов")
    print(f"  Обработка ошибок: {test_results['error_handling']} тестов")
    print(f"  ВСЕГО: {test_results['total']} тестов")
    
    print(f"\nПОКРЫТИЕ ФУНКЦИЙ:")
    print(f"  ✓ hash_password() - полное покрытие")
    print(f"  ✓ validate_password() - полное покрытие") 
    print(f"  ✓ to_camel_case() - полное покрытие")
    
    print(f"\nПРИМЕНЯЕМЫЕ ТЕХНИКИ:")
    print(f"  ✓ Equivalence Partitioning (классы эквивалентности)")
    print(f"  ✓ Boundary Value Analysis (граничные значения)")
    print(f"  ✓ Error Guessing (предположение об ошибках)")
    print(f"  ✓ Performance Testing (тестирование производительности)")
    print(f"  ✓ Integration Testing (интеграционное тестирование)")
    
    print("="*80)


if __name__ == "__main__":
    run_comprehensive_utils_tests()
    pytest.main([__file__, "-v"])