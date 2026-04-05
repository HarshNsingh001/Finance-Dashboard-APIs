class TestSummary:

    def test_viewer_can_get_summary(self, client, viewer_headers, sample_records):
        response = client.get("/api/dashboard/summary", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["total_income"] == 6200.00  # 5000 + 1200
        assert data["total_expenses"] == 2070.00  # 1500 + 450 + 120
        assert data["net_balance"] == 4130.00
        assert data["total_records"] == 5

    def test_unauthenticated_cannot_access_summary(self, client):
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 401


class TestCategoryBreakdown:

    def test_viewer_can_get_breakdown(self, client, viewer_headers, sample_records):
        response = client.get(
            "/api/dashboard/category-breakdown", headers=viewer_headers
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) > 0
        for item in data:
            assert "category" in item
            assert "type" in item
            assert "total" in item
            assert "count" in item


class TestTrends:

    def test_analyst_can_access_trends(self, client, analyst_headers, sample_records):
        response = client.get("/api/dashboard/trends", headers=analyst_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) > 0
        for point in data:
            assert "month" in point
            assert "income" in point
            assert "expenses" in point
            assert "net" in point

    def test_admin_can_access_trends(self, client, admin_headers, sample_records):
        response = client.get("/api/dashboard/trends", headers=admin_headers)
        assert response.status_code == 200

    def test_viewer_cannot_access_trends(self, client, viewer_headers, sample_records):
        response = client.get("/api/dashboard/trends", headers=viewer_headers)
        assert response.status_code == 403


class TestRecentActivity:

    def test_viewer_can_get_recent_activity(
        self, client, viewer_headers, sample_records
    ):
        response = client.get("/api/dashboard/recent-activity", headers=viewer_headers)
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 5

    def test_limit_recent_activity(self, client, viewer_headers, sample_records):
        response = client.get(
            "/api/dashboard/recent-activity?count=2",
            headers=viewer_headers,
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data) == 2
