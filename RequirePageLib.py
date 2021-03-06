#!/usr/bin/python
# -*- encoding: utf-8 -*-

#################################################################
# BRIEF:    Require Page Lib
# AUTHOR:   gaochao.morgen@gmail.com
# V1.0      2016-04-28  Create
#################################################################

import json
import urllib 
import urllib2 
import cookielib 

##################################################
#                   Interface                    #
##################################################

def SetAutoCookie():
    '''Setup a cookie handler. It will help us handle cookie automatically.

    Args:
        None

    Returns:
        None
    '''

    global GCJ
    GCJ = cookielib.LWPCookieJar() 
    cookie_support = urllib2.HTTPCookieProcessor(GCJ) 
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
    urllib2.install_opener(opener) 

def PrintCookie():
    '''Print cookies.

    Args:
        None

    Returns:
        None
    '''

    for index, cookie in enumerate(GCJ):
        print '[',index, ']',cookie;
    print '-'*80;

def RequirePageWithHttp(url, body=None, headers=None):
    '''Require web page using HTTP, and return the page content.

    Args:
        url:     Full path URL
        body:    POST data(if necessary)
        headers: More headers(if necessary)

    Returns:
        Page Content
    '''

    post = (None if body is None else urllib.urlencode(body))
    request = urllib2.Request(url, post)

    httpHeaders = {'User-Agent' : 'Mozilla/5.0 (Windows NT 5.1; rv:45.0) Gecko/20100101 Firefox/45.0'}
    if headers is not None:
        httpHeaders.update(headers)

    for key in httpHeaders:
        request.add_header(key, httpHeaders[key])

    try:
        response = urllib2.urlopen(request)
        content = response.read()
        if len(content) > 0:
            return content
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request."
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server."
        print "Reason: ", e.reason
    except:
        print "Unknown Exception."
        
    return None

def RequirePageWithAjax(url, body=None, headers=None):
    '''Require web page using Ajax, and return the page content.

    Args:
        url:     Full path URL
        body:    POST data(if necessary)
        headers: More headers(if necessary)

    Returns:
        Page Content
    '''

    ajaxHeaders = {'X-Requested-With' : 'XMLHttpRequest'}
    if headers is not None:
        ajaxHeaders.update(headers)
    return RequirePageWithHttp(url, body, ajaxHeaders)

##################################################
#                   Unit Test                    #
##################################################

if __name__ == "__main__":

    url = 'http://www.w3school.com.cn/example/jquery/demo_test_post.asp' 

    values = {
        'name' : 'Rashford', 
        'city' : 'Manchester'
    } 

    print RequirePageWithHttp(url, values)

    print "------"

    print RequirePageWithAjax(url, values)

