#!/usr/bin/python
# -*- encoding: utf-8 -*-

#################################################################
# BRIEF:    Get Page Lib
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

def AutoCookie():
    '''Setup a Cookie Handler. It will help us handle cookie automatically.

    Args:
        None

    Returns:
        None
    '''

    cj = cookielib.LWPCookieJar() 
    cookie_support = urllib2.HTTPCookieProcessor(cj) 
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
    urllib2.install_opener(opener) 

def GetNormalPage(url, body=None, headers=None):
    '''Get Basic HTML Web Page, Without Ajax.

    Args:
        url:     Full path URL
        body:    POST data(if necessary)
        headers: More headers(if necessary)

    Returns:
        Web Content
    '''

    AutoCookie()

    post = (None if body is None else urllib.urlencode(body))
    request = urllib2.Request(url, post)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:45.0) Gecko/20100101 Firefox/45.0')
    if headers:
        for key in headers:
            request.add_header(key, headers[key])

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

def GetAjaxPage(url, body=None, headers=None):
    '''Get Web Page Using Ajax.

    Args:
        url:     Full path URL
        body:    POST data(if necessary)
        headers: More headers(if necessary)

    Returns:
        Web Content
    '''

    ajaxHeaders = headers
    ajaxHeaders['X-Requested-With'] = 'XMLHttpRequest'

    return GetNormalPage(url, body, ajaxHeaders)

##################################################
#                   Unit Test                    #
##################################################

if __name__ == "__main__":

    url = 'http://www.w3school.com.cn/example/jquery/demo_test_post.asp' 

    values = {
        'name' : 'Rashford', 
        'city' : 'Manchester'
    } 

    print GetNormalPage(url, values)

