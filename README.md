## 1. 开发环境说明

- Pycharm

- 工程目录
> HongyiOJ_backend
> - HongyiOJ
> - HongyiOJ_backend
> - ...
> - manage.py
> 

### 常用命令

###### 在Anaconda命令行或其他能够执行pip命令的命令行中

- 切换到requirements.txt同一目录下（工程文件夹目录下），安装依赖包

`pip install -r requirements.txt`


###### 以下命令需要切换目录到manage.py同一目录下（工程文件夹目录下）

- 本地启动django服务器(默认启动地址为http://127.0.0.1:8000，可以在runserver后面加上期望的指定启动地址)

`python manage.py runserver`

- 在修改了HongyiOJ > models.py后，需要将更新同步迁移到数据库中

先`python manage.py makemigrations`看到发生了属性修改上的迁移, 再`python manage.py migrate`迁移变更

- 创建工程下新的应用,xxx为期望的应用名称

`python manage.py startapp xxx`

## 2. 开发方式

- 开发中

  在开发的过程中，鼓励频繁的 commit。但是 push 到远端前，强烈建议将多个 commit 合并。否则 commit 中会有很多无用信息。合并 commit 的命令为：

  `git base -i commit-id`

* 开发后

  强烈建议将多个相关的 commit 合并。

  `git rebase -i commit-id`

## 3. git 提交规范

- 规范

`feat` 增加新功能

`fix` 修复问题/BUG

`style` 代码风格相关无影响运行结果的

`perf` 优化/性能提升

`refactor` 重构

`revert` 撤销更改

`test` 测试相关

`docs` 文档/注释

`chore` 依赖更新/脚手架配置修改等

`workflow` 工作流改进

`ci` 持续集成

`types` 类型定义文件更改

`wip` 开发中

- 示例

```
fix: 修复综合搜索dem不能正常创建导出任务的问题

perf: 优化 heatMap 更高层级的聚合点显示
```

## 4.项目参数设定说明

- 近期通过题库提交的代码文件存储在`/HongyiOJ/Evaluation/submitCode`下
