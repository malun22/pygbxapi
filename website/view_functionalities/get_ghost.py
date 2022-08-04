from flask import Request, jsonify
from website.helpers.file_helper import FileHelper
from pygbx import Gbx, GbxLoadError, GbxType
from website.models.gbx import Ghost


class GetGhost:
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

                replay_parsed = True
        except GbxLoadError:
            pass

        FileHelper.delete_file(filepath)

        if not replay_parsed:
            return "Replay could not be parsed", 400

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

        return ghost.to_json()
