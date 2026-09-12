"""Smoke test: the enrolled client can talk to lok at all."""

import pytest

from unlok.api.schema import list_services

from .conftest import DeployedUnlok


@pytest.mark.integration
def test_enrolled_client_can_query(deployed_app: DeployedUnlok) -> None:
    """The session redeemed the stack's token and holds a working client.

    The test hub offers no services, so an empty tuple is the correct answer; what
    is under test is that the query is authenticated and answered at all.
    """
    services = list_services()

    assert isinstance(services, tuple)
