#!/usr/bin/python
# -*- encoding: utf-8 -*-

#################################################################
# BRIEF:    Crawler for ChongQing Metro Shops
# SITE:     http://www.cqpayeasy.com/search.php?module=2
# AUTHOR:   gaochao.morgen@gmail.com
# V1.0      2016-04-28  Create
#################################################################

import sys
import json
import urllib2 
import cookielib 
from lxml import html

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

def GetNormalPage(url):
    '''Get HTML Based Web Page, Without Ajax.

    Args:
        url: Full path URL

    Returns:
        Web Content
    '''

    AutoCookie()
    request = urllib2.Request(url)

    try:
        response = urllib2.urlopen(request, timeout=15)
        content = response.read()
        if len(content) > 0:
            return content
    except urllib2.HTTPError, e:
        print "The server couldn't fulfill the request."
        print "Error code: ", e.code
    except urllib2.URLError, e:
        print "We failed to reach a server."
        print "Reason: ", e.reason
        GetNormalPage(url)
    except:
        print "Unknown Exception."
        
    return None

def GetAjaxPage(url, body=None, referer=None):
    '''Get Web Page Using Ajax.

    Args:
        url:     Full path URL
        body:    POST data(if necessary)
        referer: More referer(if necessary)

    Returns:
        Web Content
    '''

    AutoCookie()

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:45.0) Gecko/20100101 Firefox/45.0')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    if referer:
        request.add_header('Referer', referer)
    
    try:
        postBody = (None if body is None else json.dumps(body))
        response = urllib2.urlopen(request, postBody, timeout=15)
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

def ParseIndexPage(url):
    '''Crawl Index Page, Then Parse Shop Urls.

    Args:
        url: Index Page URL

    Returns:
        None
    '''

    print url
    indexPage = GetNormalPage(url)

    # Find all shops(every page got 4 shops)
    tree = html.fromstring(indexPage)
    shops = tree.xpath("//div[@class='search_wenzi']")
    for shop in shops:
        links = shop.xpath(".//div/a/@href")
        for link in links:
            print link 
            ParseInfoPage('http://www.cqpayeasy.com' + link)
            print "------"

    # Find next index page. NOTE Unicode 
    try:
        next = tree.xpath(u"//a[text()='下一页']/@href")
        nextUrl = 'http://www.cqpayeasy.com' + next[0]
        if nextUrl == url:
            return None
        ParseIndexPage(nextUrl)
    except:
        print "Can not find next page"
        return None

def ParseInfoPage(url):
    '''Crawl Info Page, Then Parse What You Intrested.

    Args:
        url: Info Page URL

    Returns:
        None
    '''

    # Send Ajax Request to This Page
    referer = 'http://www.cqpayeasy.com/search.php?module=2'
    content = GetAjaxPage(url, None, referer)
    
    # Parse Data
    infopage = html.fromstring(content)
    groups = infopage.xpath("//div[@class='sub_content_title']/p/text()")
    for group in groups:
        print group

    infos = infopage.xpath("//div[@class='sub_content2']")
    for info in infos:
        addresses = info.xpath(".//span/p/text()")
        for address in addresses:
            print address.strip()

        # Do not include <tbody>, it's added by browser.
        #regions = info.xpath(".//table/tbody/tr[1]/td/text()")
        regions = info.xpath(".//table/tr[1]/td/text()")
        for region in regions:
            print "Region: " + region

        functions = info.xpath(".//table/tr[2]/td/text()")
        for function in functions:
            print "Function: " + function

        # This field is filled by `search.js` according to debug. 
        # urllib2 can not render JavaScript, so this field will be always `None`.
        # you can try `PyQt4.QtWebKit` to render it.
        types = info.xpath(".//td[@id='typedesc']/text()")
        for type in types:
            print "Type: " + type

        withdraws = info.xpath(".//table/tr[4]/td/text()")
        for withdraw in withdraws:
            print "Withdraw: " + withdraw

        shops = info.xpath(".//table/tr[5]/td/text()")
        for shop in shops:
            print "Shop: " + shop

if __name__ == "__main__":
    ParseIndexPage('http://www.cqpayeasy.com/search.php?module=2&page=1')

