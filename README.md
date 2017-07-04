# Shops
注意：fork我的项目后，不要动master分支，在本地要有一个dev分支，和你github上的dev分支关联，平时工作在master和dev以外的分支进行，之后merge到dev上，推送到你的仓库，再向我发起pull request。我的master分支只发布稳定版本

工程结构：
项目目录：shops
整体店铺管理模块（首页）：home
数据库信息：fixtures，可以用loaddata命令载入
静态文件：static
模版：templates
做店铺搜索要用到的预处理文件：pre_process（这个可以无视）
不要删工程目录下的pre_process.0，那个是做搜索要用的

关于模版：对每个app在templates中建一个对应的子目录，把模版放那里面。建议都继承base.html，这样样式比较统一
关于url：我们统一采用'app-namespace:url-name'格式的url定位到模版，可以参照home/urls.py的写法

各个模块：
整体店铺管理：目前所有功能都基本完成，还有一些细节需要完善
单个店铺管理：在home.html中显示店铺信息的部分，需要把url定位到单个店铺页面。争取今天把必做部分做完，能实现功能即可。网页的各个模块可以用boostrap现成的components
用户管理：今天尝试一下写加好友和收藏的部分，对django的用户这部分我不太了解，感觉比我想象得复杂。如果我有时间的话会研究一下
单个店铺部分和用户部分需要协调一下怎么写收藏和评论功能

tips：
需要有这几个库：gensim, jieba, chardet
在pycharm打开你的工程可能会发现project那一栏好多文件都没有显示，我这边是把项目目录里的.idea文件夹（是一个隐藏文件夹）删掉，然后重新打开就没问题了
