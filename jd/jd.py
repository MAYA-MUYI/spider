#!/usr/bin/env python
# -*- coding：utf-8 -*-

import requests
import re
import json
import csv
import time

product_url = 'https://item.jd.com/3995645.html'

product_comment_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv{commentVersion}&productId={productID}&score={score}&sortType={sortType}&page={pageNum}&pageSize=10&isShadowSku=0&fold=1'


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp
    else:
        return None


# 获取commentVersion，用于构造评论页的url
def get_comment_version(resp):
    pattern = re.compile(r"commentVersion:'(.*?)'")
    commentVersion = re.search(pattern, resp).group(1)
    return commentVersion


# 解析网页内容，获取下一页的链接
def get_next_page_url(current_url):
    left_url = current_url.split('page=')[0]
    # print(left_url)
    right_url = '&'.join(current_url.split('page=')[-1].split('&')[1:])
    # print(right_url)
    current_page_num = int(current_url.split('page=')[-1].split('&')[0])
    # print(current_page_num)
    next_page_num = current_page_num + 1
    next_page_url = left_url + 'page=' + str(next_page_num) + '&' + right_url
    return next_page_url


# 根据参数生成商品评论url
def generate_product_comment_url(product_url, score, sortType, page):
    commentVersion = get_comment_version(get_html(product_url))
    productID = product_url.split('/')[-1].split('.')[0]
    return product_comment_url.format(
        commentVersion=commentVersion, productID=productID, score=0, sortType=6, page=1)


# 爬取单页的评论信息
def parse_comment_info(resp):
    # fetchJSON_comment98vv13288();
    if resp.text:
        comments_json = resp.text[len('fetchJSON_comment98vv13288('):][:-2]
        with open('comment.json', 'w') as f:
            f.write(comments_json)
        comments = json.loads(comments_json).get('comments')
        for comment in comments:
            comment_info = []
            # 商品名称
            comment_info.append(comment.get('referenceName'))
            # 商品ID
            comment_info.append(comment.get('referenceId'))
            # 评论内容
            comment_info.append(comment.get('content'))
            # 评论时间
            comment_info.append(comment.get('creationTime'))
            # 评论人昵称
            comment_info.append(comment.get('nickname'))
            # 顾客会员等级
            comment_info.append(comment.get('userLevelName'))
            # 购物使用的平台
            comment_info.append(comment.get('userClientShow'))
            with open('comments.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(comment_info)
        return comments_json
    else:
        return None


def get_all_comments(url):
    print('获取第{}页评论'.format(int(url.split('page=')[-1].split('&')[0]) + 1), '<>', url)
    parse_comment_info(get_html(url))
    time.sleep(2)
    next_page = get_next_page_url(url)
    if get_html(url).text:
        get_all_comments(next_page)


def main():
    with open('comments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['商品名称', '商品ID', '评论内容', '评论时间', '评论人昵称', '顾客会员等级', '购物使用的平台'])
    get_all_comments(
        'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv13308&productId=3995645&score=0&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1')


if __name__ == '__main__':
    main()

