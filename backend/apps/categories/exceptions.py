from rest_framework.exceptions import APIException


class CategoryNotFound(APIException):
    status_code = 404
    default_detail = "The requested category does not exist"
