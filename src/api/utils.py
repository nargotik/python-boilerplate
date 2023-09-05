from flask import request
from flask_restx import Namespace, Resource, fields
from . import api




utils_namespace = Namespace('Utils Namespace', description='Namespace related operations')

@utils_namespace.route('/ping')
class UtilsList(Resource):

    def get(self):
        return {
            "message": "pong"
        }

