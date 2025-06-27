import pytest
from unlok_next.api.schema import list_services
from .conftest import DeployedUnlok


@pytest.mark.integration
@pytest.mark.skip
def test_list_user(deployed_app: DeployedUnlok) -> None:
    x = list_services()
    assert len(x) > 0, "Was not able to find any definitions"
