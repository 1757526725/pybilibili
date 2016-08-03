# coding:utf-8
"""
    pybilibili.pybilibili
    ----------------------

    程序主文件

    :copyright: (c) 2016 Shi Shushun
    :license: BSD

"""
import os
import cmd
import sys
import dicts
import webbrowser
from bs4 import BeautifulSoup
from colorama import init, Fore
from network import Network
from myargparser import MyArgparser

network = Network()

class PyBilibili(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = Fore.LIGHTRED_EX + '[@Bilibili]: ' + Fore.RESET

    def do_video(self, arg = str()):
        args = arg.split(' ')
        #[@Bilibili]: video [av]5512579
        aid = args[0]
        if aid[:2] == 'av':
            network.print_video_stat(aid[2:])
        else:
            network.print_video_stat(aid)
    
    def help_video(self):
        print('''video: video av号
\t显示某个av号视频的信息''')



    def do_people(self, arg):
        args = arg.split(' ')
        #people uid
        uid = args[0]
        network.print_people_info(uid)

    def help_people(self):
        print('''people: people uid
\t显示某个uid用户的信息''')

    

    def do_download(self, args = str()):
        args = args.split(' ')
        action = args[0]
        if action == 'danmu':
            #download danmu 5512579 -o danmu.xml
            argparser = MyArgparser(args)
            output = argparser.get_arg(['-o', '--output'])
            if output is None:
                network.download_danmu(args[1])
                return
            if '.' not in output:
                output += '.xml'
            network.download_danmu(args[1], output)
        elif action == 'video':
            #download video 5551896 -q 2 -t mp4 -o video.mp4
            argparser = MyArgparser(args)
            aid = args[1]

            quality = argparser.get_arg(['-q', '--quality'])
            if quality is None:
                print('请选择视频质量:\n1. 流畅\n2. 高清')
                quality = input(Fore.GREEN + '请输入(1/2): ' + Fore.RESET)
            while quality != '1' and quality != '2':
                print(Fore.RED + 'ERROR: 视频质量只能为1(流畅)或2(高清)')
                quality = input(Fore.GREEN + '请重新输入(1/2): ' + Fore.RESET)

            type = argparser.get_arg(['-t', '--type'])
            if type is None:
                print('请选择视频格式:\n')
                type = input(Fore.GREEN + '(mp4 / flv): ' + Fore.RESET)
            while type != 'mp4' and type != 'flv':
                print(Fore.RED + 'ERROR: 视频格式只能为mp4或flv')
                type = input(Fore.GREEN + '请重新输入(mp4/flv): ' + Fore.RESET)

            output = argparser.get_arg(['-o', '--output'])
            if output is None:
                output = ''
            
            network.download_video(aid, quality, type, output)

    def help_download(self):
        print('''download: download [danmu|video] <aid> [arguments..]
\tdanmu: 下载某个av号下xml格式的弹幕文件
\targuments:
\t\t-o --output \t输出文件名\n
\tvideo: 下载某个av号的视频
\targuments:
\t\t-q --quality \t视频质量 1(流畅)或2(高清)
\t\t-t --type \t视频格式 mp4或flv
\t\t-o --output \t输出文件名''')

    def do_ranking(self, arg):
        args = arg.split(' ')
        #[@Bilibili]: ranking [--recent] all all 3   
        if len(args) == 1:
            #无参数时args = ['']
            ranking_list_name = 'all'
            category_name = 'all'
            scope = 3
            is_recent = False
        else:
            try:
                if '--recent' not in args:
                    ranking_list_name = args[0]
                    category_name = args[1]
                    scope = args[2]
                    is_recent = False
                else:
                    ranking_list_name = args[1]
                    category_name = args[2]
                    scope = args[3]
                    is_recent = True
            except IndexError:
                pass

        if scope != '1' and scope != '3' and scope != '7':
            #错误处理
           print('Error: The scope can only be 1, 3 or 7')
           return
        #打印排行榜
        network.print_ranking_list(ranking_list_name, category_name, is_recent, scope)   

    def help_ranking(self):
        print('''ranking: ranking [--recent] 排行榜名 分区名 时间范围
\t显示某个排行榜下前100名视频的信息\n
\t排行榜名\tall(全站), origin(原创), bangumi(新番), rookie(新人)
\t分区名\t\tall, anim, music, dance, game, tech, life...
\t时间范围\t1, 3, 7, 30
\t--recent\t近期投稿, 否则为全部投稿''')

    def do_open(self, arg):
        args = arg.split(' ')
        if args[0] == '':
            webbrowser.open('http://www.bilibili.com')
        elif args[0] in dicts.link_mapping:
            webbrowser.open(dicts.link_mapping[args[0]])
        elif args[0] == 'video':
            aid = args[1]
            if aid[:2] == 'av':
                aid = args[2:]
            webbrowser.open('http://www.bilibili.com/video/av%s' % aid)
        elif args[0] == 'people':
            uid = args[1]
            webbrowser.open('http://space.bilibili.com/%s/#!/index' % uid)
        elif args[0] == 'live':
            id = args[1]
            webbrowser.open('http://live.bilibili.com/%s' % id)
            
    
    def help_open(self):
        print('''open: open [分区名|功能名|video|people|live] [av号|用户id|直播间id]
\t用默认浏览器打开某个分区|功能|视频|用户|直播间的页面
\t不加参数即打开bilibili主页''')

    def do_quit(self, arg):
        sys.exit(1)

    def help_quit(self):
        print('quit: quit the program')    
    do_q = do_quit
    def help_q(self):
        print('q: quit the program')

def start():
    os.system('cls')
    init(autoreset=True)
    print(Fore.LIGHTBLUE_EX + 
"""      ~))))))            )))))
       ))))))))       ))))))))     
   ))))))))))))))))))))))))))))))  
))))))))))))))))))))))))))))))))))1
)))))))                      ))))))
)))))                          ))))
)))))    )))))        )))))    ))))
)))))    )))))        )))))    ))))
)))))    )))))        )))))    ))))
)))))    )))))        )))))    ))))
)))))                          ))))
))))))                        )))))
)))))))))))))))))))))))))))))))))))
  1))))))))))))))))))))))))))))))1 
""")
    
    web_online = network.get_web_online()
    print("当前在线人数: %s" % web_online)

    print("欢迎使用Bilibili终端版  ( ゜- ゜)つロ  乾杯~\nAuthor: Big Mad Dog | Version: 0.1\n")

    

def main():
    start()

    PyBilibili().cmdloop()

if __name__ == "__main__":
    main()