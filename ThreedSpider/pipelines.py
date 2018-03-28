# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import re

class ThreedSpiderPipeline(object):
    def open_spider(self, spider):
        self.file = open('test.txt', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        tool = Tool()
        title = item['title']
        content = tool.replace(item['content'])
        itemIndex = item['itemIndex']

        forum_post = "INSERT INTO `pre_forum_post` \
                      (`pid`, `fid`, `tid`, `first`, \
                      `author`, `authorid`, `subject`, \
                      `dateline`, `message`, `useip`, \
                      `port`, `invisible`, `anonymous`, \
                      `usesig`, `htmlon`, `bbcodeoff`, \
                      `smileyoff`, `parseurloff`, `attachment`, \
                      `rate`, `ratetimes`, `status`, \
                      `tags`, `comment`, `replycredit`, `position`)\
                       VALUES \
                       ( \
                        %(itemIndex)s,	45,	%(itemIndex)s,	1,\
                       	'admin',	1,	'%(title)s',	\
                        1521681273,	'%(content)s',	'27.223.78.171',\
                        46933,	0,	0,\
                        1,	0,	0,	\
                        -1,	0,	0,\
                         0,	0,	0, \
                         '',	0,	0,	1); \
                         "%{'itemIndex':itemIndex,'title':title,'content':content}
        forum_thread = "INSERT INTO `pre_forum_thread` (`tid`, `fid`, `posttableid`,\
                                 `typeid`, `sortid`, `readperm`, `price`, `author`, `authorid`, \
                                 `subject`, `dateline`, `lastpost`, `lastposter`, `views`, `replies`, \
                                 `displayorder`, `highlight`, `digest`, `rate`, `special`,\
                                  `attachment`, `moderated`, `closed`, `stickreply`, \
                                  `recommends`, `recommend_add`, `recommend_sub`, `heats`,\
                                   `status`, `isgroup`, `favtimes`, `sharetimes`, `stamp`,\
                                    `icon`, `pushedaid`, `cover`, `replycredit`, `relatebytag`,\
                                     `maxposition`, `bgcolor`, `comments`, `hidden`) VALUES \
                                        (%(itemIndex)s,	45,	0,	0,	0,	0,	0,	'admin', \
                                       	1,	'%(title)s',	'1521681273',	'1521442977',	'admin', \
                                       	13,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0, \
                                      	32,	0,	0,	0,	-1,	-1,	0,	0,	0,	'0',	1,	'',	0,	0);"%{'itemIndex':itemIndex,'title':title}
        forum_id = "INSERT INTO `pre_forum_post_tableid` (`pid`) VALUES (%(itemIndex)s);"%{'itemIndex':itemIndex}

        line = forum_post + "\n"
        line = line + forum_thread + "\n"
        line = line + forum_id + "\n"
        self.file.write(line)
        return item

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = x.replace('\'','')
        #strip()将前后多余内容删除
        return x.strip()
