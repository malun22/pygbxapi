from flask import Request, jsonify
from helpers.file_helper import FileHelper
from pygbx import Gbx, GbxLoadError, GbxType


class Analyze:
    @staticmethod
    def post(request: Request):

        # Take the file from the request
        if not "file" in request.files:
            return {"error": "Missing file"}, 400

        file = request.files["file"]

        if not FileHelper.has_type(filename=file.filename, ending=".gbx"):
            return {"error": "Filetype not supported"}, 400

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

        if not replay_parsed:
            return {"error": "Replay could not be parsed"}, 400
