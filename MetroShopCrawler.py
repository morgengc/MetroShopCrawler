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
from RequirePageLib import *

##################################################
#                   Functions                    #
##################################################

def ParseIndexPage(url):
    '''Crawl index page(normal page), then parse shop URLs.

    Args:
        url: Index page URL

    Returns:
        None
    '''

    print "Index Page: %s" %url
    indexPage = RequirePageWithHttp(url)
    PrintCookie()

    # Find all shops(every page got 4 shops)
    tree = html.fromstring(indexPage)
    shops = tree.xpath("//div[@class='search_wenzi']")
    for shop in shops:
        links = shop.xpath(".//div/a/@href")
        for link in links:
            print "Ajax Page: %s" %link 
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
    '''Crawl info page(Ajax page), then parse what you intrested.

    Args:
        url: Info page URL

    Returns:
        None
    '''

    # Send Ajax request to this page
    # However, you can still using `RequirePageWithHttp()` instead
    headers = { 'Referer' : 'http://www.cqpayeasy.com/search.php?module=2' }
    content = RequirePageWithAjax(url, None, headers)
    
    # Parse data
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

##################################################
#                   Application                  #
##################################################

if __name__ == "__main__":
    SetAutoCookie()
    ParseIndexPage('http://www.cqpayeasy.com/search.php?module=2&page=1')

