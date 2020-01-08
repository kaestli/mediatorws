# -*- coding: utf-8 -*-
"""
Access limitation resource facilities.
"""

import logging

from flask_restful import Resource
from webargs.flaskparser import use_args

from eidangservices import settings
from eidangservices.utils import fdsnws
from eidangservices.utils.httperrors import FDSNHTTPError
from eidangservices.stationlite import __version__
from eidangservices.stationlite import misc
from eidangservices.stationlite.server import db, schema


class AccessLimitResource(Resource):
    """
    Resource implementation providing access limitation facilities.
    """

    LOGGER = 'flask.app.stationlite.alimit_resource'

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(self.LOGGER)

    @use_args(schema.AccessLimitSchema(), locations=('query',))
    @fdsnws.with_fdsnws_exception_handling(__version__)
    def get(self, args):
        """
        Process a GET request.
        """
        self.logger.debug('AccessLimitSchema: %s' % args)

        response = self._process_request(args)

        if not response:
            self._handle_nodata(args)

        return misc.get_response(response, settings.MIMETYPE_TEXT)

    def _process_request(self, args):
        """
        Process the request.
        """
        # TODO

    def _handle_nodata(self, args):
        raise FDSNHTTPError.create(
            int(args.get(
                'nodata', settings.FDSN_DEFAULT_NO_CONTENT_ERROR_CODE)))
