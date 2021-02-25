import logging
from http import HTTPStatus

from flask_restplus import Api
from vfb_connect_api.exception.api_exception import VfbApiException

log = logging.getLogger(__name__)

api = Api(version='Release 1.0', title='VFB_connect RESTful API',
          description='VFB_connect restful API that wraps data/knowledgeBase query endpoints and returns VFB_json')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.errorhandler(VfbApiException)
def handle_bad_request(error):
    log.exception(error.message)

    return {'message': error.message}, error.status_code


@api.errorhandler(ValueError)
def handle_value_error(error):
    log.exception(str(error))

    return {'message': str(error)}, HTTPStatus.BAD_REQUEST
