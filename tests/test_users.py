class TestListUsers:

    def test_admin_can_list_users(
        self, client, admin_headers, analyst_user, viewer_user
    ):
        response = client.get("/api/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 3  # admin + analyst + viewer

    def test_viewer_cannot_list_users(self, client, viewer_headers):
        response = client.get("/api/users", headers=viewer_headers)
        assert response.status_code == 403

    def test_analyst_cannot_list_users(self, client, analyst_headers):
        response = client.get("/api/users", headers=analyst_headers)
        assert response.status_code == 403

    def test_list_users_pagination(
        self, client, admin_headers, analyst_user, viewer_user
    ):
        response = client.get("/api/users?page=1&limit=2", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "meta" in data
        assert data["meta"]["limit"] == 2

    def test_list_users_filter_by_role(
        self, client, admin_headers, analyst_user, viewer_user
    ):
        response = client.get("/api/users?role=ANALYST", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(u["role"] == "ANALYST" for u in data["data"])


class TestGetUser:

    def test_admin_can_get_user(self, client, admin_headers, viewer_user):
        response = client.get(f"/api/users/{viewer_user.id}", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["data"]["email"] == "viewer@test.com"

    def test_get_nonexistent_user(self, client, admin_headers):
        response = client.get("/api/users/nonexistent-id", headers=admin_headers)
        assert response.status_code == 404


class TestUpdateUser:

    def test_admin_can_update_role(self, client, admin_headers, viewer_user):
        response = client.patch(
            f"/api/users/{viewer_user.id}",
            json={"role": "ANALYST"},
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["data"]["role"] == "ANALYST"

    def test_admin_can_deactivate_user(self, client, admin_headers, viewer_user):
        response = client.patch(
            f"/api/users/{viewer_user.id}",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["data"]["is_active"] is False

    def test_update_with_empty_body(self, client, admin_headers, viewer_user):
        response = client.patch(
            f"/api/users/{viewer_user.id}",
            json={},
            headers=admin_headers,
        )
        assert response.status_code == 400


class TestDeleteUser:

    def test_admin_can_delete_user(self, client, admin_headers, viewer_user):
        response = client.delete(f"/api/users/{viewer_user.id}", headers=admin_headers)
        assert response.status_code == 200

        # Verify user is no longer fetchable
        response = client.get(f"/api/users/{viewer_user.id}", headers=admin_headers)
        assert response.status_code == 404
