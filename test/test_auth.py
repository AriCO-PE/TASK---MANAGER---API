from app.auth import get_password_hash, verify_password

def test_password_hashing():
    
    plain_password = "my_secure_password"
    
  
    hashed_password = get_password_hash(plain_password)
    
    
    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrong_password", hashed_password) == False