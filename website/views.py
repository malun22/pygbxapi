from flask import Blueprint, request
from website.view_functionalities.get_challenge import GetChallenge
from website.view_functionalities.get_ghost import GetGhost
from website.view_functionalities.get_gbxdata import GetGbxData

views = Blueprint("views", __name__)


@views.route("/getghost", methods=["POST"])
def getghost():
    return GetGhost.post(request)


@views.route("/getgbxdata", methods=["POST"])
def getgbxdata():
    return GetGbxData.post(request)


@views.route("/getchallenge", methods=["POST"])
def getchallenge():
    return GetChallenge.post(request)
