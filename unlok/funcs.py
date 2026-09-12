"""Functions for executing queries and mutations using rath.

The generated API functions in :mod:`unlok.api.schema` route through these to
run their operations on the currently active :class:`UnlokRath`.

Arguments are serialised with ``exclude_unset=True``: an input field the caller
did not provide is left out of the variables rather than sent as ``null``, so the
server applies the default the schema declares for it (``requirements: [] = []``
on a manifest, say). Sending ``null`` for a non-nullable defaulted field is a
validation error on the server, which is what happened before this was added.
"""

from typing import Any, Dict, Generator, AsyncGenerator, Type
from unlok.rath import UnlokRath, current_unlok_rath
from koil import unkoil, unkoil_gen
from rath.turms.funcs import TOperation
from .errors import NoUnlokFound


def execute(
    operation: Type[TOperation],
    variables: Dict[str, Any],
    rath: UnlokRath | None = None,
) -> TOperation:
    """Executes a query or mutation using rath in a blocking way."""
    return unkoil(aexecute, operation, variables, rath)


async def aexecute(
    operation: Type[TOperation],
    variables: Dict[str, Any],
    rath: UnlokRath | None = None,
) -> TOperation:
    """Executes a query or mutation using rath in a non-blocking way."""
    rath = rath or current_unlok_rath.get()
    if not rath:
        raise NoUnlokFound(
            "No rath client found in context. Please provide a rath client."
        )

    x = await rath.aquery(
        operation.Meta.document,
        operation.Arguments(**variables).model_dump(by_alias=True, exclude_unset=True),
    )
    return operation(**x.data)


def subscribe(
    operation: Type[TOperation],
    variables: Dict[str, Any],
    rath: UnlokRath | None = None,
) -> Generator[TOperation, None, None]:
    """Subscribes to a query or mutation using rath in a blocking way."""
    return unkoil_gen(asubscribe, operation, variables, rath)


async def asubscribe(
    operation: Type[TOperation],
    variables: Dict[str, Any],
    rath: UnlokRath | None = None,
) -> AsyncGenerator[TOperation, None]:
    """Subscribes to a query or mutation using rath in a non-blocking way."""
    rath = rath or current_unlok_rath.get()
    if not rath:
        raise NoUnlokFound(
            "No rath client found in context. Please provide a rath client."
        )

    async for event in rath.asubscribe(
        operation.Meta.document,
        operation.Arguments(**variables).model_dump(by_alias=True, exclude_unset=True),
    ):
        yield operation(**event.data)
