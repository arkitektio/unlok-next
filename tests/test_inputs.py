"""Unit tests for the generated input models: no server involved.

They pin the wire shape the deployer relies on -- the manifest is mandatory on a
mint and every field travels under its GraphQL (camelCase) name.
"""

import pytest
from pydantic import ValidationError

from unlok.api.schema import ManifestInput, RedeemTokenInput, RequirementInput


def test_redeem_token_input_requires_a_manifest() -> None:
    """An app-minted token is always pinned; the client refuses to build an unpinned mint."""
    with pytest.raises(ValidationError, match="manifest"):
        RedeemTokenInput(expires_in_days=1)  # type: ignore[call-arg]


def test_redeem_token_input_serializes_under_graphql_names() -> None:
    """Snake-case attributes go out as the camelCase the schema declares."""
    manifest = ManifestInput(
        identifier="com.example.app",
        version="1.0.0",
        scopes=["read"],
        node_id="node-a",
        requirements=[RequirementInput(key="rekuest", service="live.arkitekt.rekuest", optional=False)],
    )

    wire = RedeemTokenInput(manifest=manifest, expires_in_days=1, max_redemptions=1).model_dump(
        by_alias=True, exclude_none=True
    )

    assert wire == {
        "manifest": {
            "identifier": "com.example.app",
            "version": "1.0.0",
            "scopes": ("read",),
            "nodeId": "node-a",
            "requirements": ({"key": "rekuest", "service": "live.arkitekt.rekuest", "optional": False},),
        },
        "expiresInDays": 1,
        "maxRedemptions": 1,
    }
