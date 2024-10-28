from arkitekt_next.base_models import Manifest
from unlok_next.unlok import Unlok
from unlok_next.rath import UnlokLinkComposition, UnlokRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts

from arkitekt_next.service_registry import Params
from arkitekt_next.base_models import Requirement


def init_services(service_builder_registry):

    class ArkitektNextUnlok(Unlok):
        rath: UnlokRath

    def build_arkitekt_unlok(
        fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        return ArkitektNextUnlok(
            rath=UnlokRath(
                link=UnlokLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(
                            fakts_group="lok", fakts=fakts, endpoint_url="FAKE_URL"
                        ),
                        right=FaktsGraphQLWSLink(
                            fakts_group="lok", fakts=fakts, ws_endpoint_url="FAKE_URL"
                        ),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    service_builder_registry.register(
        "unlok",
        build_arkitekt_unlok,
        Requirement(
            key="unlok",
            service="live.arkitekt.lok",
            description="An instance of ArkitektNext Lok to authenticate the user",
        ),
    )
