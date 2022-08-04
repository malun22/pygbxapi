from flask import Request, jsonify
from website.helpers.file_helper import FileHelper
from pygbx import Gbx, GbxLoadError, GbxType
from website.models.gbx import Challenge, Ghost, Replay


class GetGbxData:
    @staticmethod
    def post(request: Request):

        # Take the file from the request
        if not "file" in request.files:
            return jsonify("Missing file"), 400

        file = request.files["file"]

        if not FileHelper.has_type(filename=file.filename, ending=".gbx"):
            return jsonify("Filetype not supported"), 400

        filepath = FileHelper.save_temp_file(file)

        replay_parsed = False
        try:
            with Gbx(filepath) as g:
                ghost = g.get_class_by_id(GbxType.CTN_GHOST)

                if not ghost:
                    raise Gbx.Break("Ghost not found")

                if not ghost.cp_times or not ghost.race_time:
                    raise Gbx.Break("Missing arguments")

                replay = g.get_class_by_id(GbxType.REPLAY_RECORD)
                if not replay:
                    replay = g.get_class_by_id(GbxType.REPLAY_RECORD_OLD)

                if not replay:
                    raise Gbx.Break("Replay not found")

                challenge = replay.track.get_class_by_id(GbxType.CHALLENGE)
                if not challenge:
                    challenge = replay.track.get_class_by_id(
                        GbxType.CHALLENGE_OLD)

                if not challenge or not challenge.map_uid:
                    raise Gbx.Break("Challenge not found")

                replay_parsed = True
        except GbxLoadError:
            pass

        FileHelper.delete_file(filepath)

        if not replay_parsed:
            return jsonify("Replay could not be parsed"), 400

        ghost = Ghost(
            cp_times=ghost.cp_times,
            is_maniaplanet=ghost.is_maniaplanet,
            game_version=ghost.game_version,
            login=ghost.login,
            race_time=ghost.race_time,
            stunts_score=ghost.stunts_score,
            uid=ghost.uid,
            control_entries=ghost.control_entries,
        )

        challenge = Challenge(
            environment=challenge.environment,
            map_author=challenge.map_author,
            map_name=challenge.map_name,
            map_size=challenge.map_size,
            map_uid=challenge.map_uid,
            mood=challenge.mood,
        )

        replay = Replay(
            driver_login=replay.driver_login, nickname=replay.nickname
        )

        return jsonify({
            "ghost": ghost.to_json(),
            "challenge": challenge.to_json(),
            "replay": replay.to_json(),
        }), 200
