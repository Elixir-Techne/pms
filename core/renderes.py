from rest_framework.renderers import JSONRenderer


class PmsJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        if response.status_code == 200 or response.status_code == 201:
            response_data = {
                "success": True,
                "result": {
                    "data": data
                }
            }
        else:
            response_data = {
                "success": False,
                "result": {
                    "msg": data.get('detail') or data.get('msg') or data.get('email') or data if data else ""
                }
            }
        return super(PmsJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
