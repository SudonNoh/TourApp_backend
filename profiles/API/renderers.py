from core.renderers import BaseJSONRenderer


class ProfileJSONRenderer(BaseJSONRenderer):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_object_count = 'profilesCount'