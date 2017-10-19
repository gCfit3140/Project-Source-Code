import urllib
import json as js
from wsgiref.simple_server import make_server
import trainedModel as tM
import time


# create app using WSGI
def app(environ, start_response):
    # get the parameters from the query string
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    # check which path the web page is up to
    path = environ['PATH_INFO']
    # set a default page
    if path == "/":
        path = "/index"
    # pass the index.html file to the default page
    if path == "/index":
        f = open('index.html', 'r')
        page = f.read()
        headers = [('content-type', 'text/html')]
        status = '200 OK'
        start_response(status, headers)
        return [page.encode()]
    # after obtained user's input
    if path == '/what.json':
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        # call our prediction function and pass in the user input
        result = tM.menu(params.get('region')[0], params.get('year')[0])
        # write the prediction results as a dictionary
        prediction = {"Population": str(result[1][0][0]), "Age": str(result[1][1][0]),
                      "Income": str(result[1][2][0]), "Density": str(result[1][3]),
                      "Slight": str(result[0][0][0]), "Medium": str(result[0][0][1]),
                      "Severe": str(result[0][0][2])}
        # convert the dict into json required format
        prediction = js.dumps(prediction)
        # write the results into the json file
        f = open('what.json', 'w')
        f.write(str(prediction))
        # read the results from the json file
        f = open('what.json', 'r')
        json = f.read()
        # encode the json file
        ret = [json.encode()]
        return ret

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
        for key, value in environ.items()]
    return ret


httpd = make_server('', 8000, app)
print("Serving HTTP on port 8000...")
# Respond to requests until process is killed
httpd.serve_forever()
# Alternative: serve one request, then exit
httpd.handle_request()
