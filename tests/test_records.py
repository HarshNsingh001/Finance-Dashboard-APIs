class TestCreateRecord:

    def test_admin_can_create_record(self, client, admin_headers):
        response = client.post(
            "/api/records",
            json={
                "amount": 1500.00,
                "type": "INCOME",
                "category": "Salary",
                "date": "2024-06-15",
                "description": "Monthly salary",
            },
            headers=admin_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["amount"] == 1500.00
        assert data["data"]["type"] == "INCOME"

    def test_viewer_cannot_create_record(self, client, viewer_headers):
        response = client.post(
            "/api/records",
            json={
                "amount": 100.00,
                "type": "EXPENSE",
                "category": "Test",
                "date": "2024-01-01",
            },
            headers=viewer_headers,
        )
        assert response.status_code == 403

    def test_analyst_cannot_create_record(self, client, analyst_headers):
        response = client.post(
            "/api/records",
            json={
                "amount": 100.00,
                "type": "EXPENSE",
                "category": "Test",
                "date": "2024-01-01",
            },
            headers=analyst_headers,
        )
        assert response.status_code == 403

    def test_create_record_invalid_amount(self, client, admin_headers):
        response = client.post(
            "/api/records",
            json={
                "amount": -100.00,
                "type": "EXPENSE",
                "category": "Test",
                "date": "2024-01-01",
            },
            headers=admin_headers,
        )
        assert response.status_code == 422

    def test_create_record_missing_fields(self, client, admin_headers):
        response = client.post(
            "/api/records",
            json={
                "amount": 100.00,
            },
            headers=admin_headers,
        )
        assert response.status_code == 422


class TestListRecords:

    def test_viewer_can_list_records(self, client, viewer_headers, sample_records):
        response = client.get("/api/records", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 5

    def test_filter_by_type(self, client, viewer_headers, sample_records):
        response = client.get("/api/records?type=INCOME", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(r["type"] == "INCOME" for r in data["data"])

    def test_filter_by_category(self, client, viewer_headers, sample_records):
        response = client.get("/api/records?category=Rent", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()
        assert all("Rent" in r["category"] for r in data["data"])

    def test_filter_by_date_range(self, client, viewer_headers, sample_records):
        response = client.get(
            "/api/records?start_date=2024-02-01&end_date=2024-02-28",
            headers=viewer_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) > 0

    def test_pagination_meta(self, client, viewer_headers, sample_records):
        response = client.get("/api/records?page=1&limit=2", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["limit"] == 2
        assert data["meta"]["total"] == 5
        assert data["meta"]["has_next"] is True

    def test_unauthenticated_cannot_list(self, client, sample_records):
        response = client.get("/api/records")
        assert response.status_code == 401


class TestGetRecord:

    def test_viewer_can_get_record(self, client, viewer_headers, sample_records):
        record_id = sample_records[0].id
        response = client.get(f"/api/records/{record_id}", headers=viewer_headers)
        assert response.status_code == 200

    def test_get_nonexistent_record(self, client, viewer_headers):
        response = client.get("/api/records/nonexistent-id", headers=viewer_headers)
        assert response.status_code == 404


class TestUpdateRecord:

    def test_admin_can_update_record(self, client, admin_headers, sample_records):
        record_id = sample_records[0].id
        response = client.patch(
            f"/api/records/{record_id}",
            json={"amount": 6000.00, "description": "Updated salary"},
            headers=admin_headers,
        )
        assert response.status_code == 200
        assert response.json()["data"]["amount"] == 6000.00

    def test_viewer_cannot_update_record(self, client, viewer_headers, sample_records):
        record_id = sample_records[0].id
        response = client.patch(
            f"/api/records/{record_id}",
            json={"amount": 9999.00},
            headers=viewer_headers,
        )
        assert response.status_code == 403


class TestDeleteRecord:

    def test_admin_can_delete_record(self, client, admin_headers, sample_records):
        record_id = sample_records[0].id
        response = client.delete(f"/api/records/{record_id}", headers=admin_headers)
        assert response.status_code == 200
        response = client.get(f"/api/records/{record_id}", headers=admin_headers)
        assert response.status_code == 404

    def test_viewer_cannot_delete_record(self, client, viewer_headers, sample_records):
        record_id = sample_records[0].id
        response = client.delete(f"/api/records/{record_id}", headers=viewer_headers)
        assert response.status_code == 403
