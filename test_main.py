from fastapi.testclient import TestClient
from main import app



def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world"}

def test_register_user(client):
    response = client.post("/users/register", json={
        "username": "testuser",
        "age": 25,
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "hashed_password" not in data

def test_login_user(client):
    client.post("/users/register", json={
        "username": "loginuser",
        "age": 25,
        "email": "login@example.com",
        "password": "password123"
    })

    response = client.post("/users/login", data={
        "username": "loginuser",
        "password": "password123"
})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


#ТЕСТ НА ЗАХИЩЕНИЙ РОУТ, (ІДЕЯ: зробити запит без токена (401 очікуємо) і з токеном (200))
def test_create_product_requires_auth(client):
    #БЕЗ ТОКЕНА - МАЄ БУТИ 401
    response = client.post("/products/", json={
        "name": "Test Product",
        "price": 100,
        "in_stock": True,
        "category_id": 1
    })
    assert response.status_code == 401

def test_create_product_with_auth(client):
    #РЕЄСТРУЄМО І ЛОГІНИМОСЬ
    client.post("/users/register", json={
        "username": "productuser",
        "age": 25,
        "email": "product@example.com",
        "password": "password123"
    })
    login_response = client.post("/users/login", data={
        "username": "productuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

#СТВОРЮЄМО КАТЕГОРІЮ (ПОТРІБНА ДЛЯ CATEGORY_ID)
    category_response = client.post("/categories/", json={
        "name": "Electronics"},
        headers={"Authorization": f"Bearer {token}"}
    )
    category_id = category_response.json()["id"]

#ТЕПЕР СТВОРЮЄМО ПРОДУКТ З ТОКЕНОМ
    response = client.post("/products/", json={
        "name": "Test Product",
        "price": 100,
        "in_stock": True,
        "category_id": category_id
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data ["name"] == "Test Product"

