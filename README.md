# Shops
注意：fork我的项目后，不要动master分支，在本地要有一个dev分支，和你github上的dev分支关联，平时工作在master和dev以外的分支进行，之后merge到dev上，推送到你的仓库，再向我发起pull request。我的master分支只发布稳定版本。
工程结构：
项目目录：shops
整体店铺管理模块（首页）：home
数据库信息：fixtures，可以用loaddata命令载入
静态文件：static
模版：templates

关于模版：对每个app在templates中建一个对应的子目录，把模版放那里面。建议都继承base.html，这样样式比较统一
关于url：我们统一采用'app-namespace:url-name'格式的url定位到模版，可以参照home/urls.py的写法

各个模块：
整体店铺管理：目前实现了首页的显示，按区域和分类搜索，以及显示统计信息。
单个店铺管理：在home.html中显示店铺信息的部分，需要把url定位到单个店铺页面
用户管理：1. Comment类目前还没记录评论对应的用户的信息，需要修改Comment以及fixture/comments.json，并且为用户类添加natural key。详见home/models.py中Comment类的介绍
2. base.html中要将登录、注册、我的账户的url定位到用户模块对应的页面
单个店铺部分和用户部分需要协调一下怎么写收藏和评论功能