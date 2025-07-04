"""
WHITE-BOX тестирование для метода UserRepository.update()
Тестирование всех независимых путей
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime

from app.repository.user_repository import UserRepository
from app.models.user import UserUpdate
from app.db.tables import User


class TestUserRepositoryUpdateWhiteBox:
    """White-box тесты для метода update() с покрытием всех путей"""
    
    @pytest.fixture
    def repository(self):
        return UserRepository()
    
    @pytest.fixture
    def mock_session(self):
        session = AsyncMock()
        return session
    
    @pytest.fixture
    def sample_user(self):
        user = User()
        user.id = 1
        user.user_name = "testuser"
        user.email = "test@example.com"
        user.updated_at = datetime.now()
        return user
    
    @pytest.fixture
    def user_update(self):
        return UserUpdate(user_name="newname", email="new@example.com")

    async def test_path_1_user_not_found(self, repository, mock_session, user_update):
        """
        Путь 1: 1→2→3 (пользователь не найден)
        Тестирует ветвление: if user is None
        """
        # Arrange
        repository.get_by_id = AsyncMock(return_value=None)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await repository.update(999, user_update, mock_session)
        
        assert exc_info.value.status_code == 404
        assert "не найден" in exc_info.value.detail

    async def test_path_2_update_without_email(self, repository, mock_session, sample_user):
        """
        Путь 2: 1→2→4→5→11→12→13→14 (обновление без email)
        Тестирует ветвление: if "email" in update_data (False)
        """
        # Arrange
        user_update = UserUpdate(user_name="newname")  # Без email
        repository.get_by_id = AsyncMock(return_value=sample_user)
        
        # Act
        result = await repository.update(1, user_update, mock_session)
        
        # Assert
        assert result.user_name == "newname"
        assert result.email == "test@example.com"  # email не изменился
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    async def test_path_3_email_already_taken(self, repository, mock_session, sample_user, user_update):
        """
        Путь 3: 1→2→4→5→6→7→8 (email уже занят)
        Тестирует ветвление: if existing_user and existing_user.id != id
        """
        # Arrange
        existing_user = User()
        existing_user.id = 2  # Другой пользователь
        existing_user.email = "new@example.com"
        
        repository.get_by_id = AsyncMock(return_value=sample_user)
        repository.get_by_email = AsyncMock(return_value=existing_user)
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await repository.update(1, user_update, mock_session)
        
        assert exc_info.value.status_code == 400
        assert "уже занят" in exc_info.value.detail

    async def test_path_4_update_with_email_success(self, repository, mock_session, sample_user, user_update):
        """
        Путь 4: 1→2→4→5→6→7→9→10→11→12→13→14 (обновление с email, цикл выполняется)
        Тестирует успешное обновление с email и выполнение цикла for
        """
        # Arrange
        repository.get_by_id = AsyncMock(return_value=sample_user)
        repository.get_by_email = AsyncMock(return_value=sample_user)  # Тот же пользователь
        
        # Act
        result = await repository.update(1, user_update, mock_session)
        
        # Assert
        assert result.user_name == "newname"
        assert result.email == "new@example.com"
        assert isinstance(result.updated_at, datetime)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    async def test_path_5_update_with_email_no_existing(self, repository, mock_session, sample_user, user_update):
        """
        Путь 5: 1→2→4→5→6→7→9→11→12→13→14 (обновление с email, существующий не найден)
        Тестирует случай, когда email не занят другим пользователем
        """
        # Arrange
        repository.get_by_id = AsyncMock(return_value=sample_user)
        repository.get_by_email = AsyncMock(return_value=None)  # Email свободен
        
        # Act
        result = await repository.update(1, user_update, mock_session)
        
        # Assert
        assert result.user_name == "newname"
        assert result.email == "new@example.com"
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    async def test_for_loop_coverage(self, repository, mock_session, sample_user):
        """
        Дополнительный тест для покрытия цикла for с множественными обновлениями
        """
        # Arrange
        user_update = UserUpdate(
            user_name="newname",
            phone="89991234567",
            bio="New bio"
        )
        repository.get_by_id = AsyncMock(return_value=sample_user)
        
        # Act
        result = await repository.update(1, user_update, mock_session)
        
        # Assert
        assert result.user_name == "newname"
        assert result.phone == "89991234567"
        assert result.bio == "New bio"
        mock_session.commit.assert_called_once()

    async def test_cyclomatic_complexity_coverage(self, repository, mock_session):
        """
        Тест для демонстрации покрытия всех решений (предикатов)
        Покрывает все 4 предикатных узла + 1 = цикломатическая сложность 5
        """
        # Тест всех предикатов:
        # 1. user is None - False
        # 2. "email" in update_data - True  
        # 3. existing_user and existing_user.id != id - False
        # 4. for loop - выполняется
        
        sample_user = User()
        sample_user.id = 1
        sample_user.user_name = "test"
        sample_user.email = "test@test.com"
        
        user_update = UserUpdate(email="new@test.com", user_name="newtest")
        
        repository.get_by_id = AsyncMock(return_value=sample_user)
        repository.get_by_email = AsyncMock(return_value=None)
        
        result = await repository.update(1, user_update, mock_session)
        
        assert result is not None
        mock_session.commit.assert_called_once()