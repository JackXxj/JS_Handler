# coding:utf-8
__author__ = 'xxj'

import sys
import time
import math
import os
from rediscluster import StrictRedisCluster
import json
import re
import Queue
import lxml.etree
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
from bs4 import BeautifulSoup
import requests
from excute_js import excu_js

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

headers1 = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'wanplus_token=36119a190d033d01b3703134f1eca2f2; wanplus_csrf=_csrf_tk_1512233019;',
        'pragma': 'no-cache',
        'referer': 'https://www.wanplus.com/lol/ranking',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'x-csrf-token': '1529010235',
        'x-requested-with': 'XMLHttpRequest'
    }


headers2 = {
    'accept': 'text/html, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '39',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'UM_distinctid=166e2bc0954625-0f2756a4c40391-594c2a16-144000-166e2bc0955335; wp_pvid=6822851968; wanplus_token=36119a190d033d01b3703134f1eca2f2; wanplus_storage=lf4m67eka3o; wanplus_sid=98261dfe32cdac3a19bf00b9314cf212; wanplus_csrf=_csrf_tk_1512233019; wp_info=ssid=s9720033955; isShown=1; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1555386424; CNZZDATA1275078652=1757417873-1541401658-https%253A%252F%252Fwww.baidu.com%252F%7C1555901273; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1555902260; gameType=0',
    'origin': 'https://www.wanplus.com',
    'pragma': 'no-cache',
    # 'referer': 'https://www.wanplus.com/lol/ranking',
    'referer': 'https://www.wanplus.com/csgo/ranking',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-csrf-token': '1529010235',
    'x-requested-with': 'XMLHttpRequest',
}


def get(url, headers, count, des, proxies=None):
    for i in xrange(count):
        response = r(url, headers, i, des, proxies)
        if response is None:    # 异常
            pass
        elif response.status_code != 200:
            pass
        elif response.status_code == 200:
            return response
    return None


def r(url, headers, i, des, proxies):
    try:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), des, url, 'count：', i
        response = requests.get(url=url, headers=headers, timeout=10, verify=False, proxies=proxies)
    except BaseException as e:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'BaseException', 'url：', url, 'message：', e
        response = None
        time.sleep(2)
    return response


def post(url, headers, data, count, des, proxies=None):
    for i in xrange(count):
        response = p_r(url, headers, data, i, des, proxies)
        if response is None:    # 异常
            pass
        elif response.status_code != 200:
            pass
        elif response.status_code == 200:
            return response
    return None


def p_r(url, headers, data, i, des, proxies):
    try:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), des, url, 'count：', i
        response = requests.post(url=url, headers=headers, data=data, timeout=10, verify=False, proxies=proxies)
    except BaseException as e:
        print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'BaseException', 'url：', url, 'message：', e
        response = None
        time.sleep(2)
    return response


def team_page():
    '''
    获取游戏战队的总页数
    :return:
    '''
    game_rank = {
        '英雄联盟': 'https://www.wanplus.com/lol/ranking',
        '王者荣耀': 'https://www.wanplus.com/kog/ranking',
        'DOTA2': 'https://www.wanplus.com/dota2/ranking',
        'CS:GO': 'https://www.wanplus.com/csgo/ranking'
    }    # 游戏排行榜
    game_page = {}    # 游戏与游戏战队总页数字典
    for game_name, game_rank_url in game_rank.items():
        # url = 'https://www.wanplus.com/lol/ranking'    # 获取游戏战队的总页数
        # print time.strftime('[%Y-%m-%d %H:%M:%S]'), '获取游戏排行榜中战队的总页数url：', game_rank_url
        # response = requests.get(url=game_rank_url, headers=headers, timeout=10, verify=False)
        response = get(game_rank_url, headers, 10, '获取游戏排行榜中战队的总页数url：')
        if response is not None:
            response_text = response.text
            page_search_obj = re.search(r'var teamTotalPages = (\d+);', response_text, re.S)
            if page_search_obj:
                page = int(page_search_obj.group(1))
                print '获取相应游戏的战队项的总页数：', page
            else:
                page = None
                print '获取总页数的正则表达式需改动....'
            game_page[game_name] = page
        else:
            print '获取游戏排行榜中战队的总页数response is None'
    print '游戏与游戏战队总页数的对应关系：', game_page
    return game_page


def team(fileout):
    '''
    战队信息
    :param fileout:
    :return:
    '''
    game_team = {
        '英雄联盟': '2',
        '王者荣耀': '6',
        'DOTA2': '1',
        'CS:GO': '4'
    }  # 游戏序号
    game_page = team_page()  # 获取游戏战队的总页数接口
    # time.sleep(2)
    for game_name, all_page in game_page.items():
        game_type = game_team.get(game_name)  # 游戏序号
        for page in xrange(1, all_page + 1):    # 遍历游戏类别下的每一页
            url_demo = 'https://www.wanplus.com/ajax/detailranking?country=0&type=1&teamPage={teamPage}&game={game}'
            url = url_demo.format(teamPage=page, game=game_type)  # 战队信息url
            team_one_page(fileout, url, game_name)    # 游戏类别的一页数据接口


def team_one_page(fileout, url, game_name):
    '''
    游戏类别下一页的战队信息
    :return:
    '''
    # print time.strftime('[%Y-%m-%d %H:%M:%S]'), '战队信息url：', url
    # response = requests.get(url=url, headers=headers1, timeout=10, verify=False)
    response = get(url, headers1, 5, '战队信息url：')
    if response is not None:
        # print response.status_code
        response_json = response.json()
        datas = response_json.get('data')
        if datas:
            data1 = datas[0]
            rank = data1.get('rank')
            if isinstance(rank, float):    # float数据类型是无效的数据，unicode是有效数据
                print '该页面的数据是无效数据'
                return team_one_page(fileout, url, game_name)    # 进行重试
            else:
                for data in datas:
                    print '游戏名：', game_name
                    country = data.get('country')    # 国家名
                    print '国家名：', country
                    teamid = data.get('teamid')    # team_id(战队id)
                    rank = data.get('rank')    # 排名
                    print '排名：', rank, type(rank)
                    team_detail_infor = team_detail_data(teamid, rank)    # 战队详细信息接口
                    if team_detail_infor is not None:
                        team_detail_infor.insert(0, str(game_name))
                        team_detail_infor.insert(1, country)
                        # 游戏名称、国家、战队名称、战力值、全球排行榜、国家排行榜、历史战绩、战绩、胜/平/负、战队成员
                        content = '\t'.join(team_detail_infor)
                        fileout.write(content)
                        fileout.write('\n')
                        fileout.flush()
    else:
        print '战队信息的response is not None'


def team_detail_data(teamid, rank):
    '''
    战队详细信息
    :param teamid:
    :param rank:
    :return:
    '''
    url = 'https://www.wanplus.com/ajax/teamdetail'    # 战队详细信息url
    data = {
        # '_gtk': '1529010235',
        'teamId': teamid,
        'teamRank': rank,
    }
    # print '战队详细信息url：', url
    # response = requests.post(url=url, data=data, headers=headers1, timeout=10, verify=False)
    response = post(url, headers1, data, 5, '战队详细信息url：')
    if response is not None:
        # print response.status_code
        response_text = response.text
        # print response_text
        response_xpath = lxml.etree.HTML(response_text)
        if response_xpath is not None:
            team_name = response_xpath.xpath('//div[@class="nation"]/a/span/text()')  # 战队名称
            if team_name:
                team_name = team_name[0]
            else:
                team_name = ''
            print '战队名称：', team_name
            strength_value = response_xpath.xpath('//div[@class="integral"]/p[2]/text()')  # 战力值
            if strength_value:
                strength_value = strength_value[0]
            else:
                strength_value = ''
            # print '战力值：', strength_value
            world_rank = response_xpath.xpath(
                '//ul[@class="clans-rank"]/li[1]/div[@class="clans-rank-number"]/i/text()')  # 全球排行榜
            if world_rank:
                world_rank = world_rank[0]
            else:
                world_rank = ''
            print '全球排行榜：', world_rank
            country_rank = response_xpath.xpath(
                '//ul[@class="clans-rank"]/li[2]/div[@class="clans-rank-number"]/i/text()')  # 国家排行榜
            if country_rank:
                country_rank = country_rank[0]
            else:
                country_rank = ''
            print '国家排行榜：', country_rank

            historical_record = response_xpath.xpath(
                '//div[@class="detail"]/ul/li[1]/span[@class="dt3"]/text()')  # 历史战绩
            if historical_record:
                historical_record = historical_record[0]
            else:
                historical_record = ''
            # print '历史战绩：', historical_record
            record = response_xpath.xpath('//div[@class="detail"]/ul/li[2]/span[@class="dt3"]/text()')  # 战绩
            if record:
                record = record[0]
            else:
                record = ''
            # print '战绩：', record
            win_flat_negative = response_xpath.xpath(
                '//div[@class="detail"]/ul/li[3]/span[@class="dt3"]/text()')  # 胜/平/负
            if win_flat_negative:
                win_flat_negative = win_flat_negative[0]
            else:
                win_flat_negative = ''
            # print '胜/平/负：', win_flat_negative
            team_members = response_xpath.xpath('//ul[@class="members"]/li//div[@class="name"]/a/text()')    # 战队成员
            team_members = '|er|'.join(team_members)
            # print '战队成员：', team_members
            # 战队名称、战力值、全球排行榜、国家排行榜、历史战绩、战绩、胜/平/负、战队成员
            team_detail_infor = [team_name, str(strength_value), str(world_rank), str(country_rank), historical_record, record,
                                 win_flat_negative, team_members]
        else:
            print '战队详细信息的response_xpath is None, 该战队无详细信息'
            team_detail_infor = []
        return team_detail_infor

    else:
        print '战队详细信息的response is None'


def get_cookies():
    '''
    获取cookie以及x-csrf-token
    :return:
    '''
    game_rank_url = 'https://www.wanplus.com/lol/ranking'
    response = get(game_rank_url, headers, 10, '获取cookies和x-csrf-token的url：')
    if response is not None:
        response_cookies = response.cookies
        wanplus_token = response_cookies.get('wanplus_token')    # wanplus_token
        print 'wanplus_token：', wanplus_token
        wanplus_csrf = response_cookies.get('wanplus_csrf')    # wanplus_csrf
        print 'wanplus_csrf：', wanplus_csrf
        cookie = 'wanplus_token={}; wanplus_csrf={}; gameType=0'.format(wanplus_token, wanplus_csrf)
        print 'cookie：', cookie

        csrf_token = excu_js('getToken', wanplus_token)    # 执行js代码接口
        headers1.update({'cookie': cookie, 'x-csrf-token': csrf_token})
        # headers2.update({'cookie': cookie, 'x-csrf-token': csrf_token})
        print 'headers1：', headers1
        # print 'headers2：', headers2
    else:
        print '获取cookies和x-csrf-token的response is None'


def main():
    print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'start'
    date = time.strftime('%Y%m%d')
    dest_path = '/ftp_samba/112/spider/fanyule_two/wanplus'  # linux上的文件目录
    # dest_path = os.getcwd()    # windows上的文件目录
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    dest_file_name = os.path.join(dest_path, 'wanplus_rank_' + date)
    tmp_file_name = os.path.join(dest_path, 'wanplus_rank_' + date + '.tmp')
    fileout = open(tmp_file_name, 'w')
    get_cookies()    # 获取cookie以及x-csrf-token接口
    team(fileout)    # 玩加电竞项目接口
    fileout.flush()
    fileout.close()
    print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'end'
    os.rename(tmp_file_name, dest_file_name)


if __name__ == '__main__':
    main()


