# MEETING-TABLE

---
## 环境配置

### 开发环境

在项目根目录下运行以下命令
```
docker-compose -f docker-compose-dev.yaml up -d
```

**注意**

运行前请务必注意预留出本机的80、3306、6379端口，请注意关闭占用了这些端口的docker容器、mysql等等。Windows下关闭mysql请打开任务管理器->服务，找到mysql服务并关闭。Mac请在活动监视器上搜索mysqld并关闭。

#### 使用方法

前端：进入容器后切换至`/root/frontend`，运行`npm run serve`，在宿主机上访问`localhost`(默认80端口)即可。

业务后端：进入容器后切换至`/root/backend/business-server`，运行`python3.7 manage.py runserver`，在宿主机上访问`localhost/api/`，即在原有的路径前面加上`/api`。

会议室服务器：进入容器后切换至`/root/backend/metting-room-server`，运行`go run main.go`，在宿主机上访问`localhost/ws/`，即在原有的路径前面加上`/ws`。

因为前后端使用同一个端口，暂时不用考虑跨域问题。

### 生产环境

待配置。

---
## 代码规范

- 代码编辑器统一使用`VSCode`，安装`Vetur`, `ESLint`, `Python`, `Go`，`EditorConfig for VS Code`插件，Windows请打开设置，找到`Files: Eol`，选择`\n`，。

- 编辑代码时，请使用VSCode打开相关部分的目录，而不是在仓库根目录下。例如编写前端代码时，请使用VSCode打开`metting-table/frontend/`目录，而不是`metting-table/`目录。

- 使用VSCode打开`metting-table/frontend/`目录，打开VSCode的设置，找到`ESLint > Format: Enable`，勾上`Enables ESLint as a formatter`.打开任意一个源文件，例如`src/main.js`，按下`cmd+shift+p`，Windows下按下`ctrl+shift+p`，输入`Format Document...`或者`Format Document With...`，选择格式化文档的方式，点击配置默认格式化程序，选择`ESLint`。

- 打开终端，使用pip安装pylint以及pylint-django。使用VSCode打开`metting-table/backend/business-server/`目录，打开VSCode设置，选择工作区，找到`Python > Language Server`，选择`Jedi`，找到`Python > Linting: Pylint Args`，添加两行：`--load-plugins=pylint_django`和`--django-settings-module=mt.settings`。

- VSCode中按下`option+shift+f`格式化当前页面的代码，Windows的按键是`alt+shift+f`，编写过程中建议频繁使用。

---
## Git使用规范

- 开发时请根据issue，从主分支上创建一个新分支，同时在issue中评论`/estimate [预计花费的时间]`。完成issue后在issue中评论`/spend [实际花费的时间]`，然后发起merge request，merge request标题最后加上`Ref #issueId`，merge request的描述中加上`Closes #issueId`以及`/spend [实际花费的时间]`，还有必要的描述。

- 开发中的各个阶段记得打开gitlab上的看板，将对应的issue拖动到对应的阶段，注意不要将issue拖动到Closed。

- 分支上第一次commit时，在commit message最后加上`Closes #issueId`，注意`Closes`前留个空格，之后commit的时候，在commit message后加上`Ref #issueId`，注意Ref与前面也要空格。

- 注意commit的频率，不要一次commit修改好几个功能，也不要修改一两行就commit一次，commit message使用英文，必须是完整句，描述清晰。最好是完成一个部分或者功能时commit一次。

- 提交的代码必须是格式化的代码，符合代码规范的代码。

---
## 项目开发文档

- https://www.yuque.com/books/share/a2855e09-49a4-43e1-bdce-e6c5dec055e6?# 《MeetingTable技术文档》
