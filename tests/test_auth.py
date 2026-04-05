class TestRegister:

    def test_register_success(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepass123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == "john@example.com"
        assert data["data"]["role"] == "VIEWER"

    def test_register_duplicate_email(self, client, admin_user):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Duplicate",
                "email": "admin@test.com",
                "password": "password123",
            },
        )
        assert response.status_code == 409

    def test_register_invalid_email(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Bad Email",
                "email": "not-an-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Short Pass",
                "email": "short@example.com",
                "password": "123",
            },
        )
        assert response.status_code == 422

    def test_register_missing_fields(self, client):
        response = client.post("/api/auth/register", json={})
        assert response.status_code == 422


class TestLogin:

    def test_login_success(self, client, admin_user):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "password": "admin123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"

    def test_login_wrong_password(self, client, admin_user):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    def test_login_nonexistent_email(self, client):
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nobody@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 401


class TestProfile:

    def test_get_profile_authenticated(self, client, admin_headers, admin_user):
        response = client.get("/api/auth/me", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["email"] == "admin@test.com"
        assert data["data"]["role"] == "ADMIN"

    def test_get_profile_unauthenticated(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_get_profile_invalid_token(self, client):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token-here"},
        )
        assert response.status_code == 401
