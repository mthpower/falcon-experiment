#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from falcon import (
    API,
    HTTP_CREATED,
    HTTPBadRequest,
    HTTPNotAcceptable,
    HTTPNotFound,
    HTTPUnsupportedMediaType,
    Request,
    Response,
)

from falcon_experiment.models import User, UserSchema


class UserCollection(object):

    # def on_get(self, request, response):
    #     response.document = db.all()

    def on_post(self, request, response):
        schema = UserSchema()
        result = schema.load(request.document)
        user = result.data
        user.save()
        response.document = schema.dump(user).data
        response.status = HTTP_CREATED


class UserDetail(object):

    def on_get(self, request, response, key):
        schema = UserSchema()
        try:
            user = User.get(key)
        except KeyError:
            raise HTTPNotFound
        else:
            response.document = schema.dump(user).data

    # def on_post(self, request, response, username):
    #     response.body = 'Detail Endpoint'
    #     response.status = HTTP_CREATED


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


api = application = API(
    middleware=[
        RequireJSON(),
    ],
    request_type=JSONRequest,
    response_type=JSONResponse,
)
api.add_route('/users', UserCollection())
api.add_route('/users/{key}', UserDetail())

if __name__ == '__main__':
    # For debugging and development
    from werkzeug.serving import run_simple
    run_simple(
        hostname='localhost',
        port=8000,
        application=application,
        use_reloader=True,
    )
