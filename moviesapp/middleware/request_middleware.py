from logging import getLogger
from urllib import request

#logger = getLogger(__name__)
NO_OF_REQUESTS_SERVED = 0

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        global NO_OF_REQUESTS_SERVED
        NO_OF_REQUESTS_SERVED += 1
        print("No of requests served: ", NO_OF_REQUESTS_SERVED)
        print("API called: ", request)
        response = get_response(request)
        return response

    return middleware