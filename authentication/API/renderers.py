from core.renderers import BaseJSONRenderer


class UserJSONRenderer(BaseJSONRenderer):
    object_label = 'user'
    pagination_object_count = 'usersCount'
    pagination_object_label = 'users'
    
    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('access_token', None)
        if token is not None and isinstance(token, bytes):
            data['access_token'] = token.decode('utf-8')
            
        return super(UserJSONRenderer, self).render(data)