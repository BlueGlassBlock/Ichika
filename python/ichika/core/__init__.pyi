import datetime
from dataclasses import dataclass
from types import ModuleType
from typing import Callable, Sequence, TypedDict, TypeVar

from typing_extensions import Any

from ..client import Client
from . import events as events

# region: build info

__Build_RustInfo = TypedDict(
    "_RustInfo",
    {
        "rustc": str,
        "rustc-version": str,
        "opt-level": str,
        "debug": bool,
        "jobs": int,
    },
)
__Build_HostInfo = TypedDict("__Build_HostInfo", {"triple": str})
__Build_TargetInfo = TypedDict(
    "__Build_TargetInfo",
    {
        "arch": str,
        "os": str,
        "family": str,
        "env": str,
        "triple": str,
        "endianness": str,
        "pointer-width": str,
        "profile": str,
    },
)
__BuildInfo = TypedDict(
    "_BuildInfo",
    {
        "build": __Build_RustInfo,
        "info-time": datetime.datetime,
        "dependencies": dict[str, str],
        "features": list[str],
        "host": __Build_HostInfo,
        "target": __Build_TargetInfo,
    },
)

__version__: str
__build__: __BuildInfo

# endregion: build info

def init_log(m: ModuleType, /) -> None: ...

class Account:
    event_callbacks: list[Callable[[Any], Any]]
    def __init__(self, uin: int, data_folder: str, protocol: str) -> None: ...  # TODO: Literal
    async def login(self, method: dict[str, Any]) -> Client: ...

# region: client

internal_repr = dataclass(frozen=True, init=False)

@internal_repr
class __AccountInfo:
    nickname: str
    age: int
    gender: int

@internal_repr
class __OtherClientInfo:
    app_id: int
    instance_id: int
    sub_platform: str
    device_kind: str

@internal_repr
class Friend:
    uin: int
    nick: str
    remark: str
    face_id: int
    group_id: int

@internal_repr
class FriendGroup:
    group_id: int
    name: str
    total_count: int
    online_count: int
    seq_id: int

@internal_repr
class FriendList:
    total_count: int
    online_count: int
    def friends(self) -> tuple[Friend, ...]: ...
    def find_friend(self, uin: int) -> Friend | None: ...
    def friend_groups(self) -> tuple[FriendGroup, ...]: ...
    def find_friend_group(self, group_id: int) -> FriendGroup | None: ...

@internal_repr
class Group:
    uin: int
    name: str
    memo: str
    owner_uin: int
    create_time: int
    level: int
    member_count: int
    max_member_count: int
    global_mute_timestamp: int
    mute_timestamp: int
    last_msg_seq: int

_T = TypeVar("_T")

VTuple = tuple[_T, ...]

@internal_repr
class RawMessageReceipt:
    seqs: VTuple[int]
    rands: VTuple[int]
    time: int

class PlumbingClient:
    # [impl 1]
    async def keep_alive(self) -> None: ...
    @property
    def uin(self) -> int: ...
    @property
    def online(self) -> bool: ...
    async def get_account_info(self) -> __AccountInfo: ...
    async def get_other_clients(self) -> VTuple[__OtherClientInfo]: ...
    # [impl 2]
    async def get_friend_list(self) -> FriendList: ...
    async def get_friend_list_raw(self) -> FriendList: ...
    async def get_friends(self) -> VTuple[Friend]: ...
    async def find_friend(self, uin: int) -> Friend | None: ...
    async def poke_friend_raw(self, uin: int) -> None: ...
    # [impl 3]
    async def get_groups(self) -> VTuple[Group]: ...
    async def find_group(self, group_uin: int) -> Group | None: ...
    async def find_groups(self, group_uins: Sequence[int]) -> dict[int, Group]: ...
    async def poke_member_raw(self, group_uin: int, member_uin: int) -> None: ...
    # [impl 4]
    async def send_friend_message_raw(self, uin: int, chain: list[dict[str, Any]]) -> RawMessageReceipt: ...
    async def send_group_message_raw(self, group_uin: int, chain: list[dict[str, Any]]) -> RawMessageReceipt: ...

# endregion: client

def face_id_from_name(name: str) -> int | None: ...
def face_name_from_id(id: int) -> str: ...
def preview_raw_chain(chain: list[dict[str, Any]]) -> str: ...
