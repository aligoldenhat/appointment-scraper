import json
import datetime
from seleniumwire.utils import decode as sw_decode
import pytz
import os


def get_all_requests_of_session(driver):
    return driver.requests

def get_specific_request_of_session(driver, url, property_return, all_requests=None):
    """
    Return a request to the 'url'
    :param all_requests: Previously caught requests
    :param url: Url of that specific request
    :param property_return: Use one of these: ['object', 'body', 'headers', 'response_body', 'host', 'path', 'url, 'date', 'ws']
    :return: Intercepted request
    """
    property_return = property_return.lower()

    if all_requests is None:
        #driver.wait_for_request(pat=url)
        all_requests = get_all_requests_of_session(driver)
    for request in all_requests:
        if url in request.url:
            if property_return == 'object':
                return request
            if property_return == 'body':
                return json.loads(request.body)
            elif property_return == 'headers':
                return request.headers
            elif property_return == 'response_body':
                data = sw_decode(request.response._body, request.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
            elif property_return == 'host':
                return request.host
            elif property_return == 'path':
                return request.path
            elif property_return == 'url':
                return request.url
            elif property_return == 'date':
                return request.host
            elif property_return == 'ws':
                return request.ws_messages
            else:
                raise Exception(f" 'property_return' argument is not supported")

def mock_response(request):
    if '/getSlot' in request.url:
        GMTtime = datetime.datetime.now(pytz.timezone('GMT'))
        dirhtml = os.path.join(os.path.dirname(__file__), './getslotR.html')
        with open (dirhtml, 'r') as html:
            body_ = html.read()
        request.create_response(
            status_code=201,
            headers=[('Date', f'{GMTtime.strftime("%A")[0:3]}, {GMTtime.day} {GMTtime.strftime("%B")[0:3]} {GMTtime.year} {str(GMTtime.time()).split(".")[0]} GMT'),
                     ('Server', 'Apache/2.4.6 (Red Hat Enterprise Linux) OpenSSL/1.0.2k-fips PHP/5.6.36'),
                     ('X-Powered-By', 'PHP/5.6.36'),
                     ('Cache-Control', 'max-age=0, must-revalidate, private'),
                     #('Content-Encoding', 'gzip'),
                     ('Vary', 'Accept-Encoding'),
                     ('Content-Length', f'{len(body_)}'),
                     ('Keep-Alive', 'timeout=5, max=100'),
                     ('Connection', 'Keep-Alive'),
                     ('Content-Type', 'text/html; charset=UTF-8')],
            body= body_
        )



