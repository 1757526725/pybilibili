# coding:utf-8
"""
    pybilibili.myargparser
    ----------------------

    一个超级简单的参数解析器

    :copyright: (c) 2016 Shi Shushun
    :license: BSD

"""
class MyArgparser(object):
    def __init__(self, args = []):
        self.args = args

    def get(self, arg_names = []):
        for arg in arg_names:
            if arg in self.args:
                return self.args[self.args.index(arg) + 1]        
        #没有此参数
        return None

    def exists(self, arg_names = []):
        for arg in arg_names:
            if arg in self.args:
                return True
        return False