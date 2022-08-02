from dataclasses import dataclass, field
from helpers.gbx_helper import GbxHelper
from typing import List


@dataclass
class Replay:
    driver_login: str
    nickname: str


@dataclass
class Challenge:
    environment: str
    map_author: str
    map_name: str
    map_uid: str
    map_size: field(default_factory=list)
    map_size: int
    mood: str


@dataclass
class ControlEntry:
    enabled: int
    event_name: str
    flags: int
    time: int


@dataclass
class Ghost:
    cp_times: field(default_factory=list)
    is_maniaplanet: bool
    game_version: str
    login: str
    race_time: int
    stunts_score: int
    uid: str
    control_entries: List[ControlEntry] = field(default_factory=list)

    # On init
    formatted_race_time: str = None
    num_respawns: int = None
    cp_respawns: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.formatted_race_time = GbxHelper.timestamp_to_time(self.race_time)
        self.num_respawns = GbxHelper.get_num_respawns(self.control_entries)
        self.cp_respawns = GbxHelper.get_respawns_per_cp(
            self.control_entries, self.cp_times
        )

        self.__convert_control_entries()

    def __convert_control_entries(self):

        new_entries = []

        for entry in self.control_entries:
            new_entries.append(
                ControlEntry(
                    enabled=entry.enabled,
                    event_name=entry.event_name,
                    flags=entry.flags,
                    time=entry.time,
                )
            )

        self.control_entries = new_entries
