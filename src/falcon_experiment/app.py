#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from falcon import (
    API,
    HTTPBadRequest,
    HTTPNotAcceptable,
    HTTPUnsupportedMediaType,
    Request,
    Response,
)

from falcon_experiment import models
from falcon_experiment.db import Session, engine
from falcon_experiment.resources import (
    UserCollection,
    UserDetail,
    GroupCollection,
    GroupDetail,
)


class DBSession(object):

    def process_resource(self, request, response, resource):
        # Only create a session if we are routed to a resource
        if resource is not None:
            Session()

    def process_response(self, request, response, resource):
        # Check to see if we have done any work
        if Session.dirty or Session.new:
            Session.commit()

        # Always remove and close the session
        Session.remove()


class RequireJSON(object):

    def process_request(self, request, response):
        if not request.client_accepts_json:
            raise HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
            )

        if request.method in ('POST', 'PUT', 'PATCH'):
            if 'application/json' not in request.content_type:
                raise HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                )


class JSONRequest(Request):

    __slots__ = ('_document',)

    @property
    def document(self):
        # Short circuit if we've already deserialised
        try:
            return self._document
        except AttributeError:
            pass

        # Client did not set content length header, so short circuit
        if not self.content_length:
            return

        body = self.stream.read()
        if not body:
            raise HTTPBadRequest(
                'Empty request body',
                'A valid JSON document is required.'
            )

        try:
            self._document = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise HTTPBadRequest(
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect or not encoded as '
                'UTF-8.'
            )
        else:
            return self._document


class JSONResponse(Response):

    __slots__ = ('_document',)

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value
        self.data = json.dumps(self._document).encode('utf-8')

    @document.deleter
    def document(self):
        del self._document


# Create all our Models in the DB
models.Model.metadata.create_all(engine)

api = application = API(
    # Ordering of middleware is important
    middleware=[
        RequireJSON(),
        DBSession(),
    ],
    # Custom request and response objects
    request_type=JSONRequest,
    response_type=JSONResponse,
)

# Configure routes
api.add_route('/user', UserCollection())
api.add_route('/user/{email}', UserDetail())
api.add_route('/group', GroupCollection())
api.add_route('/group/{id}', GroupDetail())

if __name__ == '__main__':
    # For debugging and development
    from werkzeug.serving import run_simple
    run_simple(
        hostname='localhost',
        port=8000,
        application=application,
        use_reloader=True,
    )
