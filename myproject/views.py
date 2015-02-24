from pyramid.view import view_config
# Let's use some Beautiful Soup
from bs4 import BeautifulSoup
# Python httpLib comes in handy
import httplib2

@view_config(route_name='home', request_method='GET', renderer='templates/index.jinja2')
def my_view(request):
    return {'project': 'MyProject'}


@view_config(route_name='home', request_method='POST', renderer='templates/index.jinja2')
def result_view(request):
    url = request.params['url']

    http = httplib2.Http()
    response = ''
    status_msgs = ''

    # what if can't access Wikipedia
    try:
        status, response = http.request(url)
    except:
        status_msgs = True
    extract = BeautifulSoup(response)
    # find class in Wikipedia page
    toc = extract.find_all(attrs={'class': 'mw-headline'})
    output = []
    # pile them up
    for span in toc:
        output.append(span.text)

    # then, render to template
    return {
            'extract': output,
            'query': url,
            'status': status_msgs,
            'h2s': toc,
            # the cue, not to display some things
            # things in view at some points
            'searched': True,
            'project': 'MyProject'
            }
