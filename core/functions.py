from rest_framework.response import Response


class PmsResponse(Response):
    def __init__(self, data=None, status=None, exception=False, content_type=None, ):

        super(Response, self).__init__(None, status=status)

        if status == 200 or status == 201:
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

        self.data = response_data
        self.status = status
        self.content_type = content_type
        self.exception = exception
