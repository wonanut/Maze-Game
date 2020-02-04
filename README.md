# Maze-Game

current-version:  ***v1.0.5***

简单模式截图：

![](./imgs/img1.png)

迷雾模式截图：

![](./imgs/img2.png)



## Requirements

- `Python3`
- `Pandas`
- `Numpy`
- ~~`Seaborn`~~
- ~~`matplotlib`~~



## Download & Installation

### 1 Download

#### Git

使用Git克隆当前项目到本地：

```
git clone https://github.com/wonanut/Maze-Game.git
```

#### Download

直接下载当前项目到本地后解压



### 2 Installation

进入根目录：

```
cd Maze-game
```

在确保安装了上述python库之后，执行命令

```python
python Maze.py
```

如果执行上述命令不能打开且没有报错，多尝试几次即可。



## Log files

程序将会在根目录自动生成日志文件 `./maze_game.log` 



### Update information

- 2020-02-02 ***v1.0.5*** 版本上传，基础功能有
  1. 增加状态栏显示状态信息
  2. 作弊（查看提示）增加惩罚分数(当前作弊一次惩罚20分)
  3. 菜单栏，可用于设置地图生成算法，地图尺寸等（待完善）
  4. 增加迷雾模式
  5. 显示等级以及当前移动步数
  6. 随机生成游戏地图
  7. 按方向键后自动前进倒退（到分岔路停止）  
  8. 起点到任意位置辅助路径显示（鼠标左键单击空白地方显示路线）  移动次数计数 
  9. 到达终点后通关，按任意键进入下一关（目前没有难度设置，难度相同）



## Developer

Howard Wonanut：wonanut@foxmail.com
