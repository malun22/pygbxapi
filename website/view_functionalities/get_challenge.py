from flask import Request, jsonify
from website.helpers.file_helper import FileHelper
from pygbx import Gbx, GbxLoadError, GbxType
from website.models.gbx import Challenge, Ghost, Replay


class GetChallenge:
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
                challenge = g.get_class_by_id(GbxType.CHALLENGE)
                if not challenge:
                    challenge = g.get_class_by_id(
                        GbxType.CHALLENGE_OLD)

                if not challenge or not challenge.map_uid:
                    raise Gbx.Break("Challenge not found")

                replay_parsed = True
        except GbxLoadError:
            pass

        FileHelper.delete_file(filepath)

        if not replay_parsed:
            return jsonify("Challenge could not be parsed"), 400

        challenge = Challenge(
            environment=challenge.environment,
            map_author=challenge.map_author,
            map_name=challenge.map_name,
            map_size=challenge.map_size,
            map_uid=challenge.map_uid,
            mood=challenge.mood,
        )

        return challenge.to_json(), 200
