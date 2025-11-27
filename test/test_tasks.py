import pytest
from app.auth import get_password_hash, create_access_token
from app.models import User, Task

def test_create_task_authenticated(client, test_db):
    """Test crear task con autenticación JWT"""
    
    user = User(
        email="testauth@example.com",
        hashed_password=get_password_hash("testpass")
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    token = create_access_token({"sub": user.email})
    
    
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task Auth",
            "description": "Task con autenticación",
            "completed": False
        }
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task Auth"
    assert data["user_id"] == user.id

def test_get_tasks_unauthorized(client):
    """Test que endpoints protegidos requieren autenticación"""

    response = client.get("/tasks")
    
    assert response.status_code == 403  

def test_user_only_sees_own_tasks(client, test_db):
    """Test que cada usuario solo ve sus propias tasks"""
  
    user1 = User(email="user1@example.com", hashed_password=get_password_hash("pass1"))
    user2 = User(email="user2@example.com", hashed_password=get_password_hash("pass2"))
    
    test_db.add_all([user1, user2])
    test_db.commit()
    test_db.refresh(user1)
    test_db.refresh(user2)
    
    
    task1 = Task(title="Task User 1", user_id=user1.id)
    task2 = Task(title="Task User 2", user_id=user2.id)
    test_db.add_all([task1, task2])
    test_db.commit()
    
    
    token1 = create_access_token({"sub": user1.email})
    token2 = create_access_token({"sub": user2.email})
    
   
    response1 = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1) == 1
    assert data1[0]["title"] == "Task User 1"
    assert data1[0]["user_id"] == user1.id

def test_create_task_unauthenticated(client):
    """Test que no se puede crear task sin autenticación"""
    
    response = client.post(
        "/tasks",
        json={"title": "Task sin auth", "completed": False}
    )
    
    
    assert response.status_code == 403