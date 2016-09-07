#!/usr/bin/python3

from lxml import html
import requests
from time import sleep
import json




base_url = "https://cran.r-project.org/"




def get_package_names(base_url, max_iter=10000):
    url = base_url + "web/packages/available_packages_by_name.html"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    
    result = []
    for i in range(2,max_iter):   
        pkg_xpath = '//tr[{0}]/td[1]/a/text()'
        pkg_name = tree.xpath(pkg_xpath.format(i))
        if pkg_name != []:
            result.append(str(pkg_name[0]))
            miss_count = 0
        else: # might be end, but might be just a skipped row
            miss_count += 1
            if miss_count == 2: # if two misses then call it quits
                break
    return result

def build_urls(base_url, package_names):
    
    if type(package_names) == list:
        urls = [base_url + 
                'web/packages/{0}/index.html'.format(x) 
                for x in package_names]
        return urls
    elif type(package_names) == str:
        urls = base_url + 'web/packages/{0}/index.html'.format(package_names) 
        return urls
    else:
        raise TypeError("package_names must be string or list")

def get_depends(base_url, package_names):
    
    
    i = 1
    result = {}
    
    for pkg in package_names:    
        url = build_urls(base_url, pkg)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        depends = tree.xpath("*//table[1]/tr[2]/td[2]/a/text()")
        result[pkg] = depends
        sleep(2)
        i += 1
        if i%100 == 0:
            print("retrieved {0} of {1} package dependencies"\
                  .format(i, len(package_names)))
    
    return(result)

if __name__ == "__main__":
    
    nms = get_package_names(base_url)

    d = get_depends(base_url, nms)
    
    with open('test.json', 'w') as fp:
        json.dump(d, fp)







