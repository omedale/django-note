import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
      # handle authenticated rendering errors
      errors = data.get('errors', None)

      token = data.get('token', None)

      if errors is not None:
        # Allow JSONRenderer handle rendering errors.
        return super(UserJSONRenderer, self).render(data)

      if token is not None and isinstance(token, bytes):
          # we will decode `token` if it is of type bytes to ensure
          # accurate rendering of the token
          data['token'] = token.decode('utf-8')

      # render our data under the "user" namespace.
      return json.dumps({
          'user': data
      })