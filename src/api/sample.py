from flask import request
from flask_restx import Namespace, Resource, fields
from . import api
from pandas_sample import SampleGenerate, SampleGenerate2
from typing import Union
import time



sample_namespace = Namespace('Sample Namespace', description='Namespace related operations')


Sample1 = api.model('Sample1', {
    'arg1': fields.String(required=True, description='Arg1', default='sample'),
    'arg2': fields.Integer(required=False, description='Arg2'),
    'ret_data': fields.Boolean(required=True, description='Return Data'),
})
@sample_namespace.route('/sample1')
@api.doc(description="This is a description of Sample1, it requires database conection.")
class Sample1(Resource):
    @api.expect(Sample1)
    def post(self):
        args = request.json
        arg1: Union[str, None] = args.get('arg1')

        ret_data = args.get('ret_data')
        arg2 = args.get('arg2')

        if not isinstance(ret_data, bool):
            return {"error": "Field 'ret_data' must be bollean (true ou false)"}, 400

        sample = SampleGenerate(arg1, ret_data)
        return {
            "time": 1,
            "message": sample,
            "arg2": arg2,

        }, sample['status']


Sample2 = api.model('Sample2', {
    'arg1': fields.String(required=True, description='Arg1', default='sample'),
    'arg2': fields.Integer(required=False, description='Arg2'),
    'ret_data': fields.Boolean(required=True, description='Return Data'),
})
@sample_namespace.route('/sample2')
@api.doc(description="This is a description of Sample2, it requires database conection.")
class Sample2(Resource):
    @api.expect(Sample2)
    def post(self):
        args = request.json
        arg1: Union[str, None] = args.get('arg1')

        ret_data = args.get('ret_data')
        arg2 = args.get('arg2')

        if not isinstance(ret_data, bool):
            return {"error": "Field 'ret_data' must be bollean (true ou false)"}, 400


        sample = SampleGenerate(arg1, ret_data)

        return {
            "message": sample,
            "arg2": arg2,
            "args": args
        }, sample['status']



Sample3 = api.model('Sample3', {
    'arg1': fields.Integer(required=True, description='Arg1', default=1),
    'arg2': fields.Integer(required=True, description='Arg2', default=2),
    'ret_data': fields.Boolean(required=True, description='Return Data'),
})
@sample_namespace.route('/sample3')
@api.doc(description="This is a description of Sample3, it does not requires database conection.")
class Sample3(Resource):
    @api.expect(Sample3)
    def post(self):
        args = request.json
        arg1 = args.get('arg1')
        arg2 = args.get('arg2')
        ret_data = args.get('ret_data')

        if not isinstance(arg1, int) or not isinstance(arg2, int):
            return {'error': 'Both arg1 and arg2 must be integers'}, 400

        if not isinstance(ret_data, bool):
            return {"error": "Field 'ret_data' must be bollean (true ou false)"}, 400


        sample = SampleGenerate2(arg1, arg2, ret_data)

        return {
            "message": sample,
            "args": args
        }, sample['status']