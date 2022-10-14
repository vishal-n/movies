# pylint: disable=trailing-whitespace
import time

from logging import getLogger
from moviesapp.models import UserVisit

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


class SaveRequest:
    def __init__(self, get_response):
        self.get_response = get_response

        self.prefixs = [
            '/example'
        ]

    def __call__(self, request):
        _t = time.time()
        response = self.get_response(request)
        _t = int((time.time() - _t)*1000)    

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        # (Remove these two lines below to log everything)
        if not list(filter(request.get_full_path().startswith, self.prefixs)): 
            return response 

        # Create instance of our model and assign values
        request_log = UserVisit(
            endpoint=request.get_full_path(),
            remote_address=self.get_client_ip(request),
            exec_time=_t,
        )

        # Save log in db
        request_log.save() 
        return response

    # get clients ip address
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            _ip = x_forwarded_for.split(',')[0]
        else:
            _ip = request.META.get('REMOTE_ADDR')
        return _ip
