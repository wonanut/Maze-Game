# @Author: Howard Wonanut
# @Version: v1.0.7
# @Date: 2020-02-04

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from mazeGenerator import Maze
import pandas as pd
import numpy as np
from PIL import Image
import time
import copy
import math
import os

# import matplotlib.pyplot as plt
# import seaborn as sns


def draw_cell(canvas, row, col, color="#F2F2F2"):
    x0, y0 = col * cell_width, row * cell_width
    x1, y1 = x0 + cell_width, y0 + cell_width
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline =color, width = 0)


def draw_path(canvas, matrix, row, col, color, line_color):
    # 列
    if row + 1 < rows and matrix[row - 1][col] >= 1 and matrix[row + 1][col] >= 1:
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width
        x1, y1 = x0 + cell_width / 5, y0 + cell_width
    # 行
    elif col + 1 < cols and matrix[row][col - 1] >= 1 and matrix[row][col + 1] >= 1:
        x0, y0 = col * cell_width, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + cell_width, y0 + cell_width / 5
    # 左上角
    elif col + 1 < cols and row + 1 < rows and matrix[row][col + 1] >= 1 and matrix[row + 1][col] >= 1:
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + 3 * cell_width / 5, y0 + cell_width / 5
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = line_color, width = 0)
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + cell_width / 5, y0 + 3 * cell_width / 5
    # 右上角
    elif row + 1 < rows and matrix[row][col - 1] >= 1 and matrix[row + 1][col] >= 1:
        x0, y0 = col * cell_width, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + 3 * cell_width / 5, y0 + cell_width / 5
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = line_color, width = 0)
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + cell_width / 5, y0 + 3 * cell_width / 5
    # 左下角
    elif col + 1 < cols and matrix[row - 1][col] >= 1 and matrix[row][col + 1] >= 1:
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width
        x1, y1 = x0 + cell_width / 5, y0 + 3 * cell_width / 5
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = line_color, width = 0)
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + 3 * cell_width / 5, y0 + cell_width / 5
    # 右下角
    elif matrix[row - 1][col] >= 1 and matrix[row][col - 1] >= 1:
        x0, y0 = col * cell_width, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + 3 * cell_width / 5, y0 + cell_width / 5
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = line_color, width = 0)
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width
        x1, y1 = x0 + cell_width / 5, y0 + 3 * cell_width / 5
    else:
        x0, y0 = col * cell_width + 2 * cell_width / 5, row * cell_width + 2 * cell_width / 5
        x1, y1 = x0 + cell_width / 5, y0 + cell_width / 5
    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = line_color, width = 0)


def draw_maze(canvas, matrix, path, moves):
    """
    根据matrix中每个位置的值绘图：
    -1: 墙壁
    0: 空白
    1: 参考路径
    2: 移动过的位置
    """
    canvas.delete("all")
    matrix = copy.copy(matrix)
    for p in path:
        matrix[p[0]][p[1]] = 1
    for move in moves:
        matrix[move[0]][move[1]] = 2
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                draw_cell(canvas, r, c)
            elif matrix[r][c] == -1:
                draw_cell(canvas, r, c, '#525288')
            elif matrix[r][c] == 1:
                draw_cell(canvas, r, c)
                draw_path(canvas, matrix, r, c, '#bc84a8', '#bc84a8')
            elif matrix[r][c] == 2:
                draw_cell(canvas, r, c)
                draw_path(canvas, matrix, r, c, '#ee3f4d', '#ee3f4d')

    windows.title("Maze Level-{} Steps-{}".format(level, click_counter))
    set_label_text()


def update_maze(canvas, matrix, path, moves):
    windows.title("Maze Level-{} Steps-{}".format(level, click_counter))
    canvas.delete("all")
    matrix = copy.copy(matrix)
    for p in path:
        matrix[p[0]][p[1]] = 1
    for move in moves:
        matrix[move[0]][move[1]] = 2

    row, col = movement_list[-1]
    colors = ['#525288', '#F2F2F2', '#525288', '#F2F2F2', '#525288', '#F2F2F2', '#525288', '#F2F2F2']
    if map_mode > 0:
        colors = ['#232323', '#242424', '#2a2a32', '#424242', '#434368', '#b4b4b4', '#525288', '#F2F2F2']

    for r in range(rows):
        for c in range(cols):
            distance = (row - r) * (row - r) + (col - c) * (col - c)
            if distance >= 100:
                color = colors[0:2]
            elif distance >= 60:
                color = colors[2:4]
            elif distance >= 30:
                color = colors[4:6]
            else:
                color = colors[6:8]

            if matrix[r][c] == 0:
                draw_cell(canvas, r, c, color[1])
            elif matrix[r][c] == -1:
                draw_cell(canvas, r, c, color[0])
            elif matrix[r][c] == 1:
                draw_cell(canvas, r, c, color[1])
                draw_path(canvas, matrix, r, c, '#bc84a8', '#bc84a8')
            elif matrix[r][c] == 2:
                draw_cell(canvas, r, c, color[1])
                draw_path(canvas, matrix, r, c, '#ee3f4d', '#ee3f4d')
    set_label_text()
         

def check_reach():
    global next_maze_flag
    if movement_list[-1] == maze.destination:
        print("Congratulations! You reach the goal! Steps used: {}".format(click_counter))
        save_logs(logs_path, set_log_data())
        x0, y0 = cols * cell_width / 2 - 200, 30
        x1, y1 = x0 + 400, y0 + 40
        canvas.create_rectangle(x0, y0, x1, y1, fill = '#F2F2F2', outline ='#525288', width = 3)
        canvas.create_text(cols * cell_width / 2, y0 + 20, text = "Congratulations! You reach the goal! Back steps: {}".format(back_counter), fill = "#525288")
        next_maze_flag = True


def draw_result():
    if len(history_data) == 0:
        showinfo(title='Oppose', message='当前没有任何历史数据')
        return
    sns.barplot(x='level', y='value', hue='name', data=history_data)
    plt.title("History score")
    plt.show()


def save_logs(path, text):
    with open(path, 'a+') as file:
        file.write(text)


def movement_update_handler(event):
    global movement_list
    global click_counter, back_counter

    cur_pos = movement_list[-1]
    ops = {'Left': [0, -1], 'Right': [0, 1], 'Up': [-1, 0], 'Down': [1, 0], 'a': [0, -1], 'd': [0, 1], 'w': [-1, 0], 's': [1, 0]}
    r_, c_ = cur_pos[0] + ops[event.keysym][0], cur_pos[1] + ops[event.keysym][1]
    if len(movement_list) > 1 and [r_, c_] == movement_list[-2]:
        click_counter += 1
        back_counter += 1
        movement_list.pop()
        if auto_mode:
            while True:
                cur_pos = movement_list[-1]
                counter = 0
                for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    r_, c_ = cur_pos[0] + d[0], cur_pos[1] + d[1]
                    if c_ >= 0 and maze.matrix[r_][c_] == 0:
                        counter += 1
                if counter != 2:
                    break
                movement_list.pop()
    elif r_ < maze.height and c_ < maze.width and maze.matrix[r_][c_] == 0:
        click_counter += 1
        if auto_mode:
            while True:
                movement_list.append([r_, c_])
                temp_list = []
                for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    r__, c__ = r_ + d[0], c_ + d[1]
                    if c__ < maze.width and maze.matrix[r__][c__] == 0 and [r__, c__] != cur_pos:
                        temp_list.append([r__, c__])
                if len(temp_list) != 1:
                    break
                cur_pos = [r_, c_]
                r_, c_ = temp_list[0]
        else:
            movement_list.append([r_, c_])
    maze.path = []
    update_maze(canvas, maze.matrix, maze.path, movement_list)
    check_reach()
        

def next_level():
    global click_counter, total_counter, back_counter
    global next_maze_flag
    global level
    global t1

    next_maze_flag = False
    t1 = int(time.time())
    level, total_counter, click_counter, back_counter = level + 1, total_counter + click_counter, 0, 0
    generate_matrix()


def _event_handler(event):
    if next_maze_flag:
        next_level()
    elif event.keysym in ['Left', 'Right', 'Up', 'Down', 'w', 'a', 's', 'd']:
        movement_update_handler(event)
    elif event.keysym == "F1":
        _open_map()
    elif event.keysym == 'F2':
        _save_map()
    elif event.keysym == 'F3':
        windows.quit()
    elif event.keysym == "F4":
        _back_to_start_point()
    elif event.keysym == "F5":
        generate_matrix()
    elif event.keysym == "F6":
        _man()
    elif event.keysym == "F7":
        _developer()


def _paint_answer_path(event):
    global click_counter
    x, y = math.floor((event.y - 1) / cell_width), math.floor((event.x - 1) / cell_width)
    if maze.matrix[x][y] == 0:
        maze.find_path_dfs([x, y])
        click_counter += 20
        update_maze(canvas, maze.matrix, maze.path, movement_list)


def _reset_answer_path(event):
    maze.path = []
    update_maze(canvas, maze.matrix, maze.path, movement_list)


def generate_matrix():
    global movement_list
    global map_generate_mode
    global click_counter, back_counter

    if map_size_mode == -1:
        map_generate_mode = 0

    click_counter, back_counter = 0, 0
    movement_list = [maze.start]
    maze.generate_matrix(map_generate_mode, None)
    draw_maze(canvas, maze.matrix, maze.path, movement_list)


def _set_size():
    showinfo(title='上帝', message='对不起当前版本暂不支持此功能')


def _set_algo_0():
    global map_generate_mode
    map_generate_mode = 0
    generate_matrix()


def _set_algo_1():
    global map_generate_mode
    map_generate_mode = 1
    generate_matrix()


def _set_algo_2():
    global map_generate_mode
    map_generate_mode = 2
    generate_matrix()


def _set_algo_3():
    global map_generate_mode
    map_generate_mode = 3
    generate_matrix()


def _set_mode_0():
    global map_mode
    map_mode = 0


def _set_mode_1():
    global map_mode
    map_mode = 1


def _open_map():
    global map_generate_mode

    img_path = filedialog.askopenfilename(title='打开地图文件', filetypes=[('png', '*.png'), ('All Files', '*')])
    if img_path:
        image = Image.open(img_path)
        matrix = np.asarray(image) / -255
        assert len(matrix) <= 41 and len(matrix[0]) < 91
        map_generate_mode = -1
        _set_size(len(matrix[0]), len(matrix), -1, matrix)


def _save_map():
    path = "{}{}".format(os.getcwd(),image_save_path).replace('\\','/')
    if not os.path.exists(path):
        os.makedirs(path)
    imgs_len = len(os.listdir(path))
    image = Image.fromarray(-255 * maze.matrix).convert('L')
    image.save("{}map_{}.png".format(path,str(imgs_len), 'PNG'))
    showinfo(title='上帝', message='当前地图已经保存在{}'.format(path))
    image.show()


def _set_size(width, height, mode, matrix = None):
    global map_size_mode
    global rows, cols
    global movement_list
    global click_counter, back_counter

    click_counter, back_counter = 0, 0
    map_size_mode = mode
    movement_list = [maze.start]
    rows, cols = height, width
    canvas['width'] = width * cell_width
    canvas['height'] = height * cell_width
    if mode == -1:
        maze.resize_matrix(width, height, -1, matrix)
    else:
        maze.resize_matrix(width, height, map_generate_mode, matrix)
    draw_maze(canvas, maze.matrix, maze.path, movement_list)


def _set_size_31x31():
    _set_size(31, 31, 0)


def _set_size_41x41():
    _set_size(41, 41, 1)


def _set_size_37x81():
    _set_size(81, 37, 2)


def _back_to_start_point():
    global movement_list
    movement_list = [maze.start]
    draw_maze(canvas, maze.matrix, maze.path, movement_list)


def _set_auto_on():
    global auto_mode
    auto_mode = True


def _set_auto_off():
    global auto_mode
    auto_mode = False


def _developer():
    showinfo(title='开发者信息', message='当前版本：v 1.0.7\n开发时间：2020年2月\n开发者：Howard Wonanut')


def _man():
    showinfo(title='操作说明', message='控制移动：方向键\n查看提示：鼠标单击地图中空白处即可查看从起点到点击处的路径(查看一次提示增加20步)\n进入下一关：到达终点后按任意键进入下一关')


def set_label_text():
   message = " Mode: {}   Map size: {}   Algorithm: {}   Total steps: {}   Back steps: {}   Time: {}s".format( \
    "Simple" if map_mode == 0 else 'Roguelike', ['31x31', '41x41', '81x37'][map_size_mode] if map_size_mode >= 0 else "{}x{}".format(cols, rows), \
    ['Kruskal', 'Random DFS', 'Prim', 'Recursive Split'][map_generate_mode] if map_generate_mode >= 0 else 'Unknown', \
    click_counter + total_counter, back_counter, int(time.time() - t0))
   label["text"] = message
   return message


def set_log_data():
    return "[{}]Mode:{},Map-size:{},Algorithm:{},Level:{},Steps:{},Back-steps:{},Time-cost:{}\n".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))), "Simple" if map_mode == 0 else 'Roguelike', \
        ['31x31', '41x41', '81x37'][map_size_mode] if map_size_mode >= 0 else "{}x{}".format(cols, rows), \
        ['Kruskal', 'Random DFS', 'Prim', 'Recursive Split'][map_generate_mode] if map_generate_mode >= 0 else 'Unknown', \
        level, click_counter, back_counter, int(time.time() - t1))


if __name__ == '__main__':
    # 基础参数
    logs_path = './maze_game.log'
    image_save_path = '/maze_map/'
    cell_width = 20
    rows = 37
    cols = 81
    height = cell_width * rows
    width = cell_width * cols
    level = 1
    click_counter, total_counter, back_counter = 0, 0, 0
    next_maze_flag = False
    history_data = pd.DataFrame(columns=['level', 'name', 'value'])

    # 地图生成算法：0-kruskal，1-dfs，2-prim，3-split
    map_generate_mode = 0
    # 游戏模式：0-简单模式，1-迷雾模式
    map_mode = 0
    # 地图大小：0-31x31, 1-41x41, 2-81x37
    map_size_mode = 2
    # 自动前进模式，默认开
    auto_mode = True

    windows = tk.Tk()
    windows.title("Maze")
    windows.resizable(0, 0)
    t0 = int(time.time())
    t1 = t0

    #　创建菜单栏
    menubar = tk.Menu(windows)

    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=filemenu)
    filemenu.add_command(label='打开地图', command=_open_map, accelerator='F1')
    filemenu.add_command(label='保存地图', command=_save_map, accelerator='F2')
    filemenu.add_separator()
    filemenu.add_command(label='退出', command=windows.quit, accelerator='F3')
     
    editmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='设置', menu=editmenu)
    editmenu.add_command(label='回到起点', command=_back_to_start_point, accelerator='F4')
    editmenu.add_command(label='换个地图', command=generate_matrix, accelerator='F5')

    sizemenu = tk.Menu(editmenu, tearoff=0)
    editmenu.add_cascade(label='尺寸设置', menu=sizemenu)
    sizemenu.add_command(label='31x31', command=_set_size_31x31)
    sizemenu.add_command(label='41x41', command=_set_size_41x41)
    sizemenu.add_command(label='37x81', command=_set_size_37x81)

    automenu = tk.Menu(editmenu, tearoff=0)
    editmenu.add_cascade(label='自动前进', menu=automenu)
    automenu.add_command(label='开', command=_set_auto_on)
    automenu.add_command(label='关', command=_set_auto_off)

    modemenu = tk.Menu(editmenu, tearoff=0)
    editmenu.add_cascade(label='游戏模式', menu=modemenu)
    modemenu.add_command(label='普通模式', command=_set_mode_0)
    modemenu.add_command(label='迷雾模式', command=_set_mode_1)

    algomenu = tk.Menu(editmenu, tearoff=0)
    editmenu.add_cascade(label='生成算法', menu=algomenu)
    algomenu.add_command(label='Kruskal最小生成树算法', command=_set_algo_0)
    algomenu.add_command(label='随机深度优先算法', command=_set_algo_1)
    algomenu.add_command(label='prim最小生成树算法', command=_set_algo_2)
    algomenu.add_command(label='递归分割算法', command=_set_algo_3)

    scoremenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='统计', menu=scoremenu)
    scoremenu.add_command(label='历史成绩', command=draw_result)

    helpmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='帮助', menu=helpmenu)
    helpmenu.add_command(label='操作说明', command=_man, accelerator='F6')
    helpmenu.add_command(label='开发者信息', command=_developer, accelerator='F7')

    windows.config(menu=menubar)
    # end 创建菜单栏

    # 创建状态栏
    label = tk.Label(windows, text="Maze Game", bd=1, anchor='w')  # anchor left align W -- WEST
    label.pack(side="bottom", fill='x')
    set_label_text()

    canvas = tk.Canvas(windows, background="#F2F2F2", width = width, height = height)
    canvas.pack()

    maze = Maze(cols, rows)
    movement_list = [maze.start]
    generate_matrix()
    
    canvas.bind("<Button-1>", _paint_answer_path)
    canvas.bind("<Button-3>", _reset_answer_path)
    canvas.bind_all("<KeyPress>", _event_handler)
    windows.mainloop()