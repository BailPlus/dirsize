#!/usr/bin/python3
#Copyright Bail 2025
#dirsize 目录大小统计器 v1.0_1
#2025.3.22

from __future__ import annotations
import os

class DirScanner:
    dirpath:str     # 目录路径
    isdetail:bool   # 是否递归地列出所有子目录
    dirs:dict[str:DirScanner|int]   # 目录扫描结果
    files:dict[str:int]             # 文件扫描结果

    def __init__(self,dirpath:str,isdetail:bool=True):
        self.dirpath = dirpath
        self.isdetail = isdetail
        self.dirs = {}
        self.files = {}
    def __repr__(self):
        return f'<DirScanner dir={self.dirpath}, size={self._beautify_size(self.total)}>'
    def _get_dirs(self)->list[str]:
        dirs = []
        for file in os.listdir(self.dirpath):
            if os.path.isdir(file):
                dirs.append(file)
        return dirs
    @staticmethod
    def _beautify_size(size:int)->str:
        match size:
            case _ if size < 0:
                raise ValueError('怎么可能！')
            case _ if 0 <= size < 1024**1:
                return '%d B' % size
            case _ if 1024**1 <= size < 1024**2:
                return '%.3f KB' % (size/1024**1)
            case _ if 1024**2 <= size < 1024**3:
                return '%.2f MB' % (size/1024**2)
            case _ if 1024**3 <= size < 1024**4:
                return '%.1f GB' % (size/1024**3)
            case _:
                return '%d TB' % (size/1024**4)
    def scan(self):
        _,dirs,files = next(os.walk(self.dirpath))
        for i in dirs:
            dirobj = DirScanner(os.path.join(self.dirpath,i))
            dirobj.scan()
            self.dirs[i] = dirobj
        for i in files:
            path = os.path.join(self.dirpath,i)
            self.files[i] = os.lstat(path,dir_fd=None).st_size
    @property
    def total(self):
        res = 0
        for i in self.dirs.values():
            res += i.total
        for i in self.files.values():
            res += i
        return res
    def output(self,recurse_depth:int=0):
        for i in sorted(self.dirs,key=lambda x:self.dirs[x].total,reverse=True):
            dirobj = self.dirs[i]
            print('\033[33m'+'| '*recurse_depth+'|-',end='\033[32m')
            print(i+'/',self._beautify_size(dirobj.total),sep=' \033[31m',end='\033[0m\n')
            dirobj.output(recurse_depth+1)
        for i in sorted(self.files,key=self.files.get,reverse=True):
            print('\033[33m'+'| '*recurse_depth+'|-',end='\033[32m')
            print(i,self._beautify_size(self.files[i]),sep=' \033[31m',end='\033[0m\n')
