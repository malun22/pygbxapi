import re
from typing import List


class GbxHelper:
    @staticmethod
    def remove_codes(value: str) -> str:
        value = re.sub("\$\$", "{insertdollarhere}", value)
        value = re.sub("(\$[A-F|a-f|0-9]{3})|(\$[G-Z|g-z])", "", value)
        return re.sub("{insertdollarhere}", "$", value)

    @staticmethod
    def count_cps(challenge) -> int:
        cp_counter = 0
        for block in challenge.blocks:
            if "Checkpoint" in block.name:
                cp_counter += 1

        return cp_counter

    @staticmethod
    def get_num_respawns(control_entries: List):
        rspwn = 0
        for entry in control_entries:
            if entry.event_name == "Respawn" and entry.enabled == 1:
                rspwn += 1
        return rspwn

    @staticmethod
    def timestamp_to_time(value: float) -> str:
        """Converts the number of milliseconds to HH:MM:SS,ms time"""
        if not value:
            return ""

        hours, remainder = divmod(value / 1000, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds = remainder
        ms = round((remainder % 1) * 100)

        if hours > 0:
            return "{:02}:{:02}:{:02}.{:02}".format(
                int(hours), int(minutes), int(seconds), int(ms)
            )
        else:
            return "{:02}:{:02}.{:02}".format(int(minutes), int(seconds), int(ms))

    @staticmethod
    def get_respawns(control_entries) -> List[int]:
        respawns = []
        for entry in control_entries:
            if entry.event_name == "Respawn" and entry.enabled == 1:
                respawns.append(entry)
        return respawns

    @staticmethod
    def get_respawns_per_cp(control_entries, cp_times):
        respawns = GbxHelper.get_respawns(control_entries)
        cp_times = cp_times
        cp = 0
        respawn_count = 1
        respawns_per_cp = [0] * len(cp_times)
        for respawn in respawns:
            while respawn.time > cp_times[cp]:
                # iterates through CPs and resets respawn count for current sector
                cp += 1
                respawn_count = 1
            respawns_per_cp[cp] = respawn_count
            respawn_count += 1
        return respawns_per_cp
