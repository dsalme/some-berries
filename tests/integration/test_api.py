import httpx
import pytest
from unittest.mock import Mock, patch

from poke_berries.berries import cache


class TestHomeApi:
    def test_home_page(self, client):
        req = client.get("/")
        assert req.status_code == 200


class TestBerriesApi:

    def test_berries_page_success(self, client):
        req = client.get("/allBerryStats")
        assert req.status_code == 200

    @patch("berries_client.berries_client.client.session.get")
    def test_berries_page_404(self, mock_get, client):
        cache.clear()

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error",
            request=Mock(),
            response=Mock()
        )

        mock_get.return_value = mock_response

        req = client.get("/allBerryStats")
        assert req.status_code == 404

