import tkinter as tk
from tkinter.messagebox import showinfo
from mazeGenerator import Maze
import time
import copy
import math
import numpy as np

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
    for p in path:
        matrix[p[0]][p[1]] = 1
    for move in moves:
        matrix[move[0]][move[1]] = 2

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
    if level > 2:
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
        print("Congratulations! You reach the goal! The step used: {}".format(click_counter))
        x0, y0 = width / 2 - 200, 30
        x1, y1 = x0 + 400, y0 + 40
        canvas.create_rectangle(x0, y0, x1, y1, fill = '#F2F2F2', outline ='#525288', width = 3)
        canvas.create_text(width / 2, y0 + 20, text = "Congratulations! You reach the goal! Steps used: {}".format(click_counter), fill = "#525288")
        next_maze_flag = True


def _eventHandler(event):
    global movement_list
    global click_counter, total_counter
    global next_maze_flag
    global level

    if not next_maze_flag and event.keysym  in ['Left', 'Right', 'Up', 'Down']:
        cur_pos = movement_list[-1]
        ops = {'Left': [0, -1], 'Right': [0, 1], 'Up': [-1, 0], 'Down': [1, 0]}
        r_, c_ = cur_pos[0] + ops[event.keysym][0], cur_pos[1] + ops[event.keysym][1]
        if len(movement_list) > 1 and [r_, c_] == movement_list[-2]:
            click_counter += 1
            movement_list.pop()
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
        maze.path = []
        update_maze(canvas, maze.matrix, maze.path, movement_list)
        check_reach()
    elif next_maze_flag:
        next_maze_flag = False
        total_counter += click_counter
        click_counter = 0
        generate_matrix()
        maze.path = []
        level += 1
    

def _paint(event):
    global click_counter
    x, y = math.floor((event.y - 1) / cell_width), math.floor((event.x - 1) / cell_width)
    if maze.matrix[x][y] == 0:
        maze.find_path_dfs([x, y])
        click_counter += 20
        update_maze(canvas, maze.matrix, maze.path, movement_list)

def _reset(event):
    maze.path = []
    update_maze(canvas, maze.matrix, maze.path, movement_list)

def generate_matrix():
    global movement_list
    movement_list = [maze.start]
    if map_generate_mode == 0:
        maze.generate_matrix_kruskal()
    elif map_generate_mode == 1:
        maze.generate_matrix_dfs()
    elif map_generate_mode == 2:
        maze.generate_matrix_prim()
    elif map_generate_mode == 3:
        maze.generate_matrix_split()
    draw_maze(canvas, maze.matrix, maze.path, movement_list)

def _set_size():
    showinfo(title='设置地图大小', message='对不起当前版本暂不支持此功能')

def _set_algo_0():
    global map_generate_mode
    map_generate_mode = 0

def _set_algo_1():
    global map_generate_mode
    map_generate_mode = 1

def _set_algo_2():
    global map_generate_mode
    map_generate_mode = 2

def _set_algo_3():
    global map_generate_mode
    map_generate_mode = 3

def _open_map():
    pass

def _save_map():
    pass

def _developer():
    showinfo(title='开发者信息', message='当前版本：v 1.0.5\n开发时间：2020年2月\n开发者：Howard Wonanut')

def _man():
    showinfo(title='操作说明', message='控制移动：方向键\n查看提示：鼠标单击地图中空白处即可查看从起点到点击处的路径(查看一次提示增加20步)\n进入下一关：到达终点后按任意键进入下一关')

def set_label_text():
   message = "  Mode: {}     Algorithm: {}     Level: {}     Total steps: {}     Time: {}s".format("Simple" if level <= 2 else 'Roguelike', \
    ['Kruskal', 'Random DFS', 'Prim', 'Recursive Split'][map_generate_mode], level, click_counter + total_counter, int(time.time() - t0))
   label["text"] = message


if __name__ == '__main__':
    # 基础参数
    cell_width = 20
    rows = 37
    cols = 71
    height = cell_width * rows
    width = cell_width * cols
    level = 1
    click_counter, total_counter = 0, 0
    next_maze_flag = False

    # 地图生成算法：0-kruskal，1-dfs，2-prim，3-split
    map_generate_mode = 0

    windows = tk.Tk()
    windows.title("Maze")
    windows.resizable(0, 0)
    t0 = time.time()

    #　创建菜单栏
    menubar = tk.Menu(windows)

    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=filemenu)
    filemenu.add_command(label='打开地图', command=_open_map)
    filemenu.add_command(label='保存地图', command=_save_map)
    filemenu.add_separator()
    filemenu.add_command(label='退出', command=windows.quit)
     
    editmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='设置', menu=editmenu)
    editmenu.add_command(label='换个地图', command=generate_matrix)
    editmenu.add_command(label='尺寸设置', command=_set_size)

    algomenu = tk.Menu(editmenu, tearoff=0) 
    editmenu.add_cascade(label='生成算法', menu=algomenu)
    algomenu.add_command(label='Kruskal最小生成树算法', command=_set_algo_0)
    algomenu.add_command(label='随机深度优先算法', command=_set_algo_1)
    algomenu.add_command(label='prim最小生成树算法', command=_set_algo_2)
    algomenu.add_command(label='递归分割算法', command=_set_algo_3)

    helpmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='帮助', menu=helpmenu)
    helpmenu.add_command(label='操作说明', command=_man)
    helpmenu.add_command(label='开发者信息', command=_developer)

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
    
    canvas.bind("<Button-1>", _paint)
    canvas.bind("<Button-3>", _reset)
    canvas.bind_all("<KeyPress>", _eventHandler)
    windows.mainloop()
