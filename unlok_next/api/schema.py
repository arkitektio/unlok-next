from unlok_next.funcs import asubscribe, aexecute, subscribe, execute
from typing_extensions import Literal
from typing import Optional, AsyncIterator, List, Iterator
from pydantic import BaseModel, Field
from unlok_next.rath import UnlokRath
from unlok_next.traits import RoomListener
from enum import Enum


class StructureInput(BaseModel):
    object: str
    identifier: str

    class Config:
        """A config class"""

        frozen = True
        extra = "forbid"
        use_enum_values = True


class MessageFragmentAgentRoom(RoomListener, BaseModel):
    """Room(id, title, description, creator)"""

    typename: Optional[Literal["Room"]] = Field(alias="__typename", exclude=True)
    id: str

    class Config:
        """A config class"""

        frozen = True


class MessageFragmentAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Optional[Literal["Agent"]] = Field(alias="__typename", exclude=True)
    id: str
    room: MessageFragmentAgentRoom

    class Config:
        """A config class"""

        frozen = True


class MessageFragment(BaseModel):
    typename: Optional[Literal["Message"]] = Field(alias="__typename", exclude=True)
    id: str
    text: str
    "A clear text representation of the rich comment"
    agent: MessageFragmentAgent
    "The user that created this comment"

    class Config:
        """A config class"""

        frozen = True


class ListMessageFragmentAgent(BaseModel):
    """Agent(id, room, name, app, user)"""

    typename: Optional[Literal["Agent"]] = Field(alias="__typename", exclude=True)
    id: str

    class Config:
        """A config class"""

        frozen = True


class ListMessageFragment(BaseModel):
    typename: Optional[Literal["Message"]] = Field(alias="__typename", exclude=True)
    id: str
    text: str
    "A clear text representation of the rich comment"
    agent: ListMessageFragmentAgent
    "The user that created this comment"

    class Config:
        """A config class"""

        frozen = True


class RoomFragment(RoomListener, BaseModel):
    typename: Optional[Literal["Room"]] = Field(alias="__typename", exclude=True)
    id: str
    title: str
    "The Title of the Room"
    description: str

    class Config:
        """A config class"""

        frozen = True


class SendMutation(BaseModel):
    send: MessageFragment

    class Arguments(BaseModel):
        text: str
        room: str
        agent_id: str = Field(alias="agentId")
        attach_structures: Optional[List[StructureInput]] = Field(
            alias="attachStructures", default=None
        )

    class Meta:
        document = "fragment Message on Message {\n  id\n  text\n  agent {\n    id\n    room {\n      id\n    }\n  }\n}\n\nmutation Send($text: String!, $room: ID!, $agentId: String!, $attachStructures: [StructureInput!]) {\n  send(\n    input: {text: $text, room: $room, agentId: $agentId, attachStructures: $attachStructures}\n  ) {\n    ...Message\n  }\n}"


class CreateRoomMutation(BaseModel):
    create_room: RoomFragment = Field(alias="createRoom")

    class Arguments(BaseModel):
        title: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n}\n\nmutation CreateRoom($title: String, $description: String) {\n  createRoom(input: {title: $title, description: $description}) {\n    ...Room\n  }\n}"


class GetRoomQuery(BaseModel):
    room: RoomFragment

    class Arguments(BaseModel):
        id: str

    class Meta:
        document = "fragment Room on Room {\n  id\n  title\n  description\n}\n\nquery GetRoom($id: ID!) {\n  room(id: $id) {\n    ...Room\n  }\n}"


class WatchRoomSubscriptionRoom(BaseModel):
    typename: Optional[Literal["RoomEvent"]] = Field(alias="__typename", exclude=True)
    message: Optional[ListMessageFragment]

    class Config:
        """A config class"""

        frozen = True


class WatchRoomSubscription(BaseModel):
    room: WatchRoomSubscriptionRoom

    class Arguments(BaseModel):
        room: str
        agent_id: str = Field(alias="agentId")

    class Meta:
        document = "fragment ListMessage on Message {\n  id\n  text\n  agent {\n    id\n  }\n}\n\nsubscription WatchRoom($room: ID!, $agentId: ID!) {\n  room(room: $room, agentId: $agentId) {\n    message {\n      ...ListMessage\n    }\n  }\n}"


async def asend(
    text: str,
    room: str,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[UnlokRath] = None,
) -> MessageFragment:
    """Send


     send: Message represent the message of an agent on a room


    Arguments:
        text (str): text
        room (str): room
        agent_id (str): agentId
        attach_structures (Optional[List[StructureInput]], optional): attachStructures.
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        MessageFragment"""
    return (
        await aexecute(
            SendMutation,
            {
                "text": text,
                "room": room,
                "agentId": agent_id,
                "attachStructures": attach_structures,
            },
            rath=rath,
        )
    ).send


def send(
    text: str,
    room: str,
    agent_id: str,
    attach_structures: Optional[List[StructureInput]] = None,
    rath: Optional[UnlokRath] = None,
) -> MessageFragment:
    """Send


     send: Message represent the message of an agent on a room


    Arguments:
        text (str): text
        room (str): room
        agent_id (str): agentId
        attach_structures (Optional[List[StructureInput]], optional): attachStructures.
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        MessageFragment"""
    return execute(
        SendMutation,
        {
            "text": text,
            "room": room,
            "agentId": agent_id,
            "attachStructures": attach_structures,
        },
        rath=rath,
    ).send


async def acreate_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[UnlokRath] = None,
) -> RoomFragment:
    """CreateRoom


     createRoom: Room(id, title, description, creator)


    Arguments:
        title (Optional[str], optional): title.
        description (Optional[str], optional): description.
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        RoomFragment"""
    return (
        await aexecute(
            CreateRoomMutation, {"title": title, "description": description}, rath=rath
        )
    ).create_room


def create_room(
    title: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[UnlokRath] = None,
) -> RoomFragment:
    """CreateRoom


     createRoom: Room(id, title, description, creator)


    Arguments:
        title (Optional[str], optional): title.
        description (Optional[str], optional): description.
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        RoomFragment"""
    return execute(
        CreateRoomMutation, {"title": title, "description": description}, rath=rath
    ).create_room


async def aget_room(id: str, rath: Optional[UnlokRath] = None) -> RoomFragment:
    """GetRoom


     room: Room(id, title, description, creator)


    Arguments:
        id (str): id
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        RoomFragment"""
    return (await aexecute(GetRoomQuery, {"id": id}, rath=rath)).room


def get_room(id: str, rath: Optional[UnlokRath] = None) -> RoomFragment:
    """GetRoom


     room: Room(id, title, description, creator)


    Arguments:
        id (str): id
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        RoomFragment"""
    return execute(GetRoomQuery, {"id": id}, rath=rath).room


async def awatch_room(
    room: str, agent_id: str, rath: Optional[UnlokRath] = None
) -> AsyncIterator[WatchRoomSubscriptionRoom]:
    """WatchRoom



    Arguments:
        room (str): room
        agent_id (str): agentId
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        WatchRoomSubscriptionRoom"""
    async for event in asubscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room


def watch_room(
    room: str, agent_id: str, rath: Optional[UnlokRath] = None
) -> Iterator[WatchRoomSubscriptionRoom]:
    """WatchRoom



    Arguments:
        room (str): room
        agent_id (str): agentId
        rath (unlok_next.rath.UnlokRath, optional): The arkitekt rath client

    Returns:
        WatchRoomSubscriptionRoom"""
    for event in subscribe(
        WatchRoomSubscription, {"room": room, "agentId": agent_id}, rath=rath
    ):
        yield event.room
