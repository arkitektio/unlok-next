import json
import pytest
from unlok.api.schema import (
    FlowFragment,
)
import yaml
from .utils import build_relative


@pytest.fixture
def add_three_flow():
    with open(build_relative("flowjsons/add_three_flow.json"), "r") as f:
        g = json.load(f)
        print(g)

    return FlowFragment(**g)
