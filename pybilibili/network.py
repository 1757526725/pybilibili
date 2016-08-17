# coding:utf-8
"""
    pybilibili.network
    ----------------------

    所有爬虫函数

    :copyright: (c) 2016 Shi Shushun
    :license: BSD

"""
from bs4 import BeautifulSoup
from colorama import Fore, Style
import dicts
import json
import urllib
import requests
import time
import re
import os
import math
import sys

class Network:
    def  __init__(self):
        self.homepage_res = requests.get('http://www.bilibili.com')
        self.homepage_cont = self.homepage_res.content
        self.homepage_soup = BeautifulSoup(self.homepage_cont, 'html.parser', from_encoding='utf-8')

    def _clear_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
   
    def _print_or_output(self, content, output, filename):
        if output == False:
            print(content)
        else:
            for f in vars(Fore).items():
                content = content.replace(f[1], '')
            file = open(filename, 'a')
            file.write(content)
            file.close()
            print(Fore.LIGHTWHITE_EX + '下载完成! 文件路径: ' + Fore.GREEN + os.path.abspath(filename))
                

    def get_web_online(self):
        return self.homepage_soup.find('a', href='/video/online.html').em.string

    def print_video_stat(self, aid, filename, newfile):
        json_res = requests.get('http://api.bilibili.com/archive_stat/stat?aid=%s' % aid)
        json_str = json_res.content
        json_list = json.loads(json_str.decode('utf-8'))
        data = json_list['data']

        html_res = requests.get('http://www.bilibili.com/video/av%s/' % aid)
        html_cont = html_res.content.decode('utf-8')
        html_soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        title = html_soup.find('div', class_='v-title').string
        author = html_soup.find('div', class_='usname').a.string
        time_ = html_soup.find('time', itemprop="startDate").i.string
        category_list = html_soup.find_all('a', rel='v:url')
        category = str()

        output = False
        if filename is not None:
            output = True
            if newfile:
                self._clear_file(filename)
         
        for a in category_list[1:]:
            category += a.string
            if category_list.index(a) != len(category_list) - 1:
                category += ' > '
        self._print_or_output(Fore.CYAN + '[av%s] ' % aid + 
              Fore.RESET + '%s ' % title + 
              Fore.YELLOW + '作者: ' + Fore.RESET + '%s' % author + '\n', output, filename)
        self._print_or_output(Fore.WHITE + time_ + Fore.RESET + 
              ' | ' + Fore.WHITE + category + '\n', output, filename)
        self._print_or_output(Fore.GREEN + '播放: ' + Fore.RESET + '%d ' % data['view'] + 
              Fore.GREEN + '弹幕: ' + Fore.RESET + '%d ' % data['danmaku'] + 
              Fore.GREEN + '评论: ' + Fore.RESET + '%d ' % data['reply'] + 
              Fore.GREEN + '收藏: ' + Fore.RESET + '%d ' % data['favorite'] + 
              Fore.GREEN + '硬币: ' + Fore.RESET + '%d ' % data['coin'] + 
              Fore.GREEN + '分享: ' + Fore.RESET + '%d ' % data['share'], output, filename) 

        # [av123456] 感觉身体被掏空by彩虹室内合唱团 作者:上海彩虹室内合唱团
        # 2016-07-27 10:07 | 音乐 > 原创音乐
        # 播放:1407731 弹幕:4167 评论:15916 收藏:15916 硬币:21166 分享:8637

    def print_people_info(self, uid, filename, newfile):
        req_info = requests.get('http://space.bilibili.com/ajax/member/GetInfo?mid=%s' % uid)
        json_info_str = req_info.content
        json_info_list = json.loads(json_info_str.decode('utf-8'))
        data = json_info_list['data']

        req_video = requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&tid=0' % uid)
        json_video_str = req_video.content
        json_video_list = json.loads(json_video_str.decode('utf-8'))
        # [3875443] 哟唷喲yo Lv4 | 闲的无聊转转视频，做做视频(╯‵□′)╯︵┴─┴
        # 性别: 男 注册于: 2014-4-7 生日: 01-01 地址: 未填写
        # 投稿视频: 1 | 关注: 61 粉丝: 4
        regtime = time.gmtime(data['regtime'])
        place = data['place']
        if place == '':
            place = '未填写'

        sign = data['sign']
        if sign == '':
            sign = '无简介'
        
        output = False
        if filename is not None:
            output = True
            if newfile:
                self._clear_file(filename)   
        
        self._print_or_output(Fore.CYAN + '[%s] ' % uid + 
              Fore.RESET + '%s ' % data['name'] + 
              Fore.LIGHTYELLOW_EX + 'Lv%s ' % data['level_info']['current_level'] + 
              Fore.LIGHTWHITE_EX + '| ' + 
              Fore.RESET + '%s' % sign + '\n', output, filename)
        self._print_or_output(Fore.GREEN + '性别: ' + Fore.RESET + '%s ' % data['sex'] + 
              Fore.GREEN + '注册于: ' + Fore.RESET + '%d-%d-%d ' % (regtime[0], regtime[1], regtime[2]) + 
              Fore.GREEN + '生日: ' + Fore.RESET + '%s ' % data['birthday'] + 
              Fore.GREEN + '地址: ' + Fore.RESET + '%s ' % place + '\n', output, filename)
        self._print_or_output(Fore.GREEN + '投稿视频: ' + Fore.RESET + '%d ' % json_video_list['data']['count'] + Fore.LIGHTWHITE_EX + '| ' + Fore.LIGHTRED_EX + '关注: ' + Fore.RESET + '%d ' % data['friend'] + Fore.LIGHTRED_EX + '粉丝: ' + Fore.RESET + '%d' % data['fans'] + '\n', output, filename)

    def print_ranking_list(self, ranking_name, category_fenqu, is_recent, scope, filename, newfile):
        try:
            ranking_list_name = dicts.ranking_list_name[ranking_name]
            category_name = dicts.ranking_category_name[category_fenqu]
        except:
            #TODO: 错误处理
            pass
        if is_recent == True:
            scope = '0' + scope

        output = False
        if filename is not None:
            output = True     
            if newfile:
                self._clear_file(filename)    

        res = requests.get('http://www.bilibili.com/index/rank/%s-%s-%s.json' % (ranking_list_name, scope, category_name))
        json_str = res.content

        json_list = json.loads(json_str.decode('utf-8'))
        ranking = 1
        for video in json_list['rank']['list']:
            # 1: [av123456] 【多素材】解开只穿一件衬衣的扣子 综合评分: 1147182
            #       播放: 666191 评论: 4160 作者: 科学超电磁炮F
            try:
                self._print_or_output(Fore.RED + "%d: " % ranking + 
                      Fore.CYAN + "[av%d] " % video['aid'] + 
                      Fore.RESET + "%s " % video['title'] + 
                      Fore.YELLOW + "综合评分: %d" % video['pts'] + '\n' + 
                      Fore.GREEN + "\t播放: " + Fore.RESET + "%d" % video['play'] + 
                      Fore.GREEN + " 评论: " + Fore.RESET + "%d" % video['video_review'] + 
                      Fore.GREEN + " 作者: " + Fore.RESET + video['author'] + '\n', output, filename)
            except UnicodeEncodeError:
                pass
            ranking += 1

    def download_danmu(self, aid, filename):
        req_video = requests.get('http://www.bilibili.com/video/av%s/' % aid)
        html = req_video.content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = soup.find('div', class_='v-title').h1.string
        player = soup.find(text = re.compile('^EmbedPlayer'))
        cid = ''
        for i in player.string[(player.string.find('cid') + 4):]:
            if i == '&':
                break
            cid += i
        req_xml = requests.get('http://comment.bilibili.com/%s.xml' % cid)
        xml = req_xml.content

        if filename == '':
            filename = '弹幕_av%s.xml' % aid

        f = open(filename, 'w', encoding = 'utf-8')
        try:
            f.writelines(xml.decode('utf-8'))
        except UnicodeEncodeError:
            pass
        f.close()
        
        result = ''

        #删除空行
        f = open(filename, 'r', encoding = 'utf-8')
        lines = f.readlines()
        for li in lines:
            if li.split():
                result += li
        f.close()
        f = open(filename, 'w', encoding = 'utf-8')
        f.writelines(result)
        f.close()

        print(Fore.LIGHTWHITE_EX + '下载完成! 文件路径: ' + Fore.GREEN + os.path.abspath(filename))


 
    def _download_schedule(self, a, b, c):
        per = 100.0 * a * b / c
        sys.stdout.write('\r')
        sys.stdout.write('[%-50s] %s' % ( '=' * int(math.floor(per / 2)), '%.2f%%' % per))  
        sys.stdout.flush()  
        if per >= 100:
            sys.stdout.write('\n')

    def download_video(self, aid, quality, type, output):
        """
            quality: 1=流畅 2=高清
            type: mp4 / flv
        """

        req_video = requests.get('http://www.bilibili.com/video/av%s/' % aid)
        html = req_video.content.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        title = soup.find('div', class_='v-title').string
        player = soup.find(text = re.compile('^EmbedPlayer'))
        cid = ''
        for i in player.string[(player.string.find('cid') + 4):]:
            if i == '&':
                break
            cid += i

        json_str = requests.get('http://interface.bilibili.com/playurl?otype=json&appkey=86385cdc024c0f6c&cid=%s&quality=%s&type=%s' % (cid, quality, type)).content
        json_list = json.loads(json_str.decode('utf-8'))
        time_length = json_list['timelength']
        size = json_list['durl'][0]['size']
        download_link = json_list['durl'][0]['url']

        length_all = float('%f' % (time_length / 1000 / 60))
        length_min = math.floor(float('%f' % (time_length / 1000 / 60)))
        length_sec = int(60 * (length_all - math.floor(length_all)))
        length_str = '%d:%d' % (length_min, length_sec)

        size_mb = '%.2fMB' % (size / (1024 * 1024))
        
        if type == 'mp4':
            type = 'hdmp4'
        if output == '':
            output = '%s.%s' % (title, type)

        # [av123456] 【史诗级误解】甲铁城x罪恶王冠的超同步套路剧场（吐血完整版）——.mp4
        # 时长: 12:43 | 大小: 119.0MB
        # 开始下载? (y/n):
        
        print(Fore.CYAN + '[av%s] ' % aid + Fore.RESET + title)
        print(Fore.GREEN + '时长: ' + Fore.RESET + length_str + 
              Fore.LIGHTWHITE_EX + ' | ' + 
              Fore.GREEN + '大小: ' + Fore.RESET + size_mb)

        confirm = input('开始下载? (y/n): ')
        if confirm == 'y':
            #Download
            urllib.request.urlretrieve(download_link, output, self._download_schedule)
            print(Fore.LIGHTWHITE_EX + '下载成功! 文件路径: ' + Fore.GREEN + os.path.abspath(output))