from rest_framework.exceptions import APIException


class ServiceNotFound(APIException):
    status_code = 404
    default_detail = "The requested service does not exist"
