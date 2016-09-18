from flask_restplus import Namespace, Resource, fields
from flask import url_for
from restplus import api
import logging

sampleApi = Namespace('sample', description='Sample')
logger = logging.getLogger(__name__)

sample = sampleApi.model('Sample', {
    'id': fields.String(required=True, description='The sample identifier'),
    'name': fields.String(required=True, description='The sample name'),
})

SAMPLES = [
    {'id': 'felix', 'name': 'Felix'},
]


@api.route('/')
class SampleList(Resource):
    @api.doc('list_samples')
    @api.marshal_list_with(sample)
    def get(self):
        '''List all samples'''
        return SAMPLES


@api.route('/<id>')
@api.param('id', 'The sample identifier')
@api.response(404, 'Sample not found')
class Sample(Resource):
    @api.doc('get_sample')
    @api.marshal_with(sample)
    def get(self, id):
        '''Fetch a sample given its identifier'''
        for sample in SAMPLES:
            if sample['id'] == id:
                return sample
        api.abort(404)