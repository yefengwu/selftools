#!/usr/bin/python3.8
#coding=utf-8
"""
 利用api.githu.com获取个人的repos,并下载
"""
import json
import requests
import urllib3
from urllib.request import urlopen
import os
import math
from time import sleep

def find_repos(USER, perpage=30.0):
    """
    #params@USER:需要下载的用户名
    #params@perpage:每页下载个数，用于计算多少页，最多30
    #return@用户repos的地址列表
    """
    #调用api.github.com来获取用户repo信息
    userurl = urlopen('https://api.github.com/users/' + USER)
    #解析url,接口返回json
    public_gists = json.load(userurl)
    #'public_repos'字段是个数
    gistcount = public_gists['public_repos']
    print("Found gists : " + str(gistcount))
    #计算页数，用于遍历
    pages = int(math.ceil(float(gistcount)/perpage))
    print("Found pages : " + str(pages))
    #保存所有的repo链接
    repos = []
    for page in range(pages):
        pageNumber = str(page + 1)
        print ("Processing page number " + pageNumber)
        #查找第i页
        pageUrl = 'https://api.github.com/users/' + USER  + \
                  '/repos?page=' + pageNumber + '&per_page=' + \
                    str(int(perpage))
        u = urlopen (pageUrl)
        gists = json.load(u)
        #'html_url'字段是repo的链接
        for gist in gists:
            repos.append(str(gist['html_url']))
    return repos

def del_repo(repolist):
    for reponame in repolist:
        repolink = f'https://api.github.com/repos/{username}/{reponame}'
        print(f"This repo will delete: {repolink}")
        headers = get_headers()
        ret = requests.delete(repolink, headers=headers)
        if(ret.status_code == 204):
            print("delete success!")
        sleep(2)

def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}", # 此处的XXX代表上面的token
        "X-OAuth-Scopes": "repo"
    }
    return headers

   
def main():
    global username,token
    username = input("please input yout github username: ")
    print("username:", username) 
    colours = find_repos(username)
    for i in range(0, len(colours)):
        print(i, colours[i])
    option = input("Do you want to do (remove:rm/download:dl): ")
    while(option != "rm" and option != "dl"):
        option = input("Input Error, please input your select again: ")
    if (option == "rm"):
        token = input("please input the token that you have permission: ")
        input_list = input("please input the repolist you want to delete: ")
        repolist = input_list.split()
        del_repo(repolist)
    elif(option == "dl"):
        print("this function is making")
        
if __name__ == "__main__":
    main()
