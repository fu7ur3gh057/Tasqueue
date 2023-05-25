from rest_framework.exceptions import APIException


class CustomerNotFound(APIException):
    status_code = 404
    default_detail = "The requested customer does not exist"


class NotYourCustomer(APIException):
    status_code = 403
    default_detail = "You can't edit a customer that doesn't belong to you"
