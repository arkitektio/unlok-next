from typing import Generator
import pytest
from dokker import local, Deployment
from dokker.log_watcher import LogWatcher
import os
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from unlok_next.unlok import Unlok
from unlok_next.rath import (
    UnlokRath,
    SplitLink,
    UnlokLinkComposition,
)
from graphql import OperationType
from dataclasses import dataclass


project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")
private_key = os.path.join(project_path, "private_key.pem")


async def token_loader():
    return "test"


@dataclass
class DeployedUnlok:
    deployment: Deployment
    unlok_watcher: LogWatcher
    unlok: Unlok


@pytest.fixture(scope="session")
def deployed_app() -> Generator[DeployedUnlok, None, None]:
    setup = local(docker_compose_file)
    setup.pull_on_enter = False
    setup.up_on_enter = False
    setup.add_health_check(
        url=lambda spec: f"http://localhost:{spec.find_service("lok").get_port_for_internal(80).published}/graphql",
        service="lok",
        timeout=5,
        max_retries=15,
    )

    watcher = setup.create_watcher("lok")

    with setup:
        setup.down()

        http_url = f"http://localhost:{setup.spec.find_service("lok").get_port_for_internal(80).published}/graphql"
        ws_url = f"ws://localhost:{setup.spec.find_service("lok").get_port_for_internal(80).published}/graphql"

        y = UnlokRath(
            link=UnlokLinkComposition(
                auth=ComposedAuthLink(token_loader=token_loader, token_refresher=token_loader),
                split=SplitLink(
                    left=AIOHttpLink(endpoint_url=http_url),
                    right=GraphQLWSLink(ws_endpoint_url=ws_url),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        )

        kab = Unlok(
            rath=y,
        )

        setup.up()

        setup.check_health()

        with kab as kab:
            deployed = DeployedUnlok(
                deployment=setup,
                unlok_watcher=watcher,
                unlok=kab,
            )

            yield deployed
