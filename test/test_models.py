import pytest
from app.auth import get_password_hash
from app.models import User, Task

def test_user_creation(test_db):
    """Test que un usuario se crea correctamente en la base de datos"""
  
    user_data = {
        "email": "test@example.com",
        "hashed_password": get_password_hash("testpassword123")
    }
    
   
    user = User(**user_data)
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.created_at is not None
    assert user.hashed_password != "testpassword123"  

def test_task_creation(test_db):
    """Test que una task se crea correctamente"""
   
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash("password123")
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    
    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        user_id=user.id
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)
    
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.completed == False
    assert task.user_id == user.id
    assert task.created_at is not None

def test_user_task_relationship(test_db):
    """Test la relación entre User y Task"""
    
    user = User(
        email="reltest@example.com", 
        hashed_password=get_password_hash("relpassword")
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    
    task1 = Task(title="Task 1", user_id=user.id)
    task2 = Task(title="Task 2", user_id=user.id)
    
    test_db.add_all([task1, task2])
    test_db.commit()
    test_db.refresh(user)
    
   
    user_tasks = test_db.query(Task).filter(Task.user_id == user.id).all()
    
    assert len(user_tasks) == 2
    assert user_tasks[0].title == "Task 1"
    assert user_tasks[1].title == "Task 2"
    assert user_tasks[0].user_id == user.id
    assert user_tasks[1].user_id == user.id

def test_user_email_unique_constraint(test_db):
    """Test que el email debe ser único"""
   
    user1 = User(
        email="unique@example.com",
        hashed_password=get_password_hash("pass1")
    )
    test_db.add(user1)
    test_db.commit()
    
    
    user2 = User(
        email="unique@example.com",  # Mismo email
        hashed_password=get_password_hash("pass2")
    )
    test_db.add(user2)
    
    with pytest.raises(Exception):  
        test_db.commit()