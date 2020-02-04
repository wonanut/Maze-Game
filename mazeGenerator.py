# @Author: Howard Wonanut
# @Version: v1.0.7
# @Date: 2020-02-04

import tkinter as tk

import numpy as np
import time
import random
import copy

class UnionSet(object):
	"""
	并查集实现，构造函数中的matrix是一个numpy类型
	"""
	def __init__(self, arr):
		self.parent = {pos: pos for pos in arr}
		self.count = len(arr)

	def find(self, root):
		if root == self.parent[root]:
			return root
		return self.find(self.parent[root])

	def union(self, root1, root2):
		self.parent[self.find(root1)] = self.find(root2)


class Maze(object):
	"""
	迷宫生成类
	"""
	def __init__(self, width = 11, height = 11):
		assert width >= 5 and height >= 5, "Length of width or height must be larger than 5."

		self.width = (width // 2) * 2 + 1
		self.height = (height // 2) * 2 + 1
		self.start = [1, 0]
		self.destination = [self.height - 2, self.width - 1]
		self.matrix = None
		self.path = []

	def print_matrix(self):
		matrix = copy.deepcopy(self.matrix)
		for p in self.path:
			matrix[p[0]][p[1]] = 1
		for i in range(self.height):
			for j in range(self.width):
				if matrix[i][j] == -1:
					print('□', end = '')
				elif matrix[i][j] == 0:
					print('  ', end = '')
				elif matrix[i][j] == 1:
					print('■', end = '')
				elif matrix[i][j] == 2:
					print('▲', end = '')
			print('')

	def generate_matrix(self, mode, new_matrix):
		assert mode in [-1, 0, 1, 2, 3], "Mode {} does not exist.".format(mode)
		if mode == -1:
			self.matrix = new_matrix
		elif mode == 0:
			self.generate_matrix_kruskal()
		elif mode == 1:
			self.generate_matrix_dfs()
		elif mode == 2:
			self.generate_matrix_prim()
		elif mode == 3:
			self.generate_matrix_split()

	def resize_matrix(self, width, height, mode, new_matrix):
		self.path = []
		self.width = (width // 2) * 2 + 1
		self.height = (height // 2) * 2 + 1
		self.start = [1, 0]
		self.destination = [self.height - 2, self.width - 1]
		self.generate_matrix(mode, new_matrix)

	def generate_matrix_dfs(self):
		# 地图初始化，并将出口和入口处的值设置为0
		self.matrix = -np.ones((self.height, self.width))
		self.matrix[self.start[0], self.start[1]] = 0
		self.matrix[self.destination[0], self.destination[1]] = 0

		visit_flag = [[0 for i in range(self.width)] for j in range(self.height)]

		def check(row, col, row_, col_):
			temp_sum = 0
			for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
				temp_sum += self.matrix[row_ + d[0]][col_ + d[1]]
			return temp_sum <= -3

		def dfs(row, col):
			visit_flag[row][col] = 1
			self.matrix[row][col] = 0
			if row == self.start[0] and col == self.start[1] + 1:
				return

			directions = [[0, 2], [0, -2], [2, 0], [-2, 0]]
			random.shuffle(directions)
			for d in directions:
				row_, col_ = row + d[0], col + d[1]
				if row_ > 0 and row_ < self.height - 1 and col_ > 0 and col_ < self.width - 1 and visit_flag[row_][col_] == 0 and check(row, col, row_, col_):
					if row == row_:
						visit_flag[row][min(col, col_) + 1] = 1
						self.matrix[row][min(col, col_) + 1] = 0
					else:
						visit_flag[min(row, row_) + 1][col] = 1
						self.matrix[min(row, row_) + 1][col] = 0
					dfs(row_, col_)

		dfs(self.destination[0], self.destination[1] - 1)
		self.matrix[self.start[0], self.start[1] + 1] = 0

	# 虽然说是prim算法，但是我感觉更像随机广度优先算法
	def generate_matrix_prim(self):
		# 地图初始化，并将出口和入口处的值设置为0
		self.matrix = -np.ones((self.height, self.width))

		def check(row, col):
			temp_sum = 0
			for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
				temp_sum += self.matrix[row + d[0]][col + d[1]]
			return temp_sum < -3
			
		queue = []
		row, col = (np.random.randint(1, self.height - 1) // 2) * 2 + 1, (np.random.randint(1, self.width - 1) // 2) * 2 + 1
		queue.append((row, col, -1, -1))
		while len(queue) != 0:
			row, col, r_, c_ = queue.pop(np.random.randint(0, len(queue)))
			if check(row, col):
				self.matrix[row, col] = 0
				if r_ != -1 and row == r_:
					self.matrix[row][min(col, c_) + 1] = 0
				elif r_ != -1 and col == c_:
					self.matrix[min(row, r_) + 1][col] = 0
				for d in [[0, 2], [0, -2], [2, 0], [-2, 0]]:
					row_, col_ = row + d[0], col + d[1]
					if row_ > 0 and row_ < self.height - 1 and col_ > 0 and col_ < self.width - 1 and self.matrix[row_][col_] == -1:
						queue.append((row_, col_, row, col))

		self.matrix[self.start[0], self.start[1]] = 0
		self.matrix[self.destination[0], self.destination[1]] = 0

	def generate_matrix_split(self):
		# 地图初始化，并将出口和入口处的值设置为0
		self.matrix = -np.zeros((self.height, self.width))
		self.matrix[0, :] = -1
		self.matrix[self.height - 1, :] = -1
		self.matrix[:, 0] = -1
		self.matrix[:, self.width - 1] = -1

		# 随机生成位于(start, end)之间的偶数
		def get_random(start, end):
			rand = np.random.randint(start, end)
			if rand & 0x1 ==  0:
				return rand
			return get_random(start, end)

		# split函数的四个参数分别是左上角的行数、列数，右下角的行数、列数，墙壁只能在偶数行，偶数列
		def split(lr, lc, rr, rc):
			if rr - lr < 2 or rc - lc < 2:
				return

			# 生成墙壁,墙壁只能是偶数点
			cur_row, cur_col = get_random(lr, rr), get_random(lc, rc)
			for i in range(lc, rc + 1):
				self.matrix[cur_row][i] = -1
			for i in range(lr, rr + 1):
				self.matrix[i][cur_col] = -1
			
			# 挖穿三面墙得到连通图，挖孔的点只能是偶数点
			wall_list = [
				("left", cur_row, [lc + 1, cur_col - 1]),
				("right", cur_row, [cur_col + 1, rc - 1]), 
				("top", cur_col, [lr + 1, cur_row - 1]),
				("down", cur_col, [cur_row +  1, rr - 1])
			]
			random.shuffle(wall_list)
			for wall in wall_list[:-1]:
				if wall[2][1] - wall[2][0] < 1:
					continue
				if wall[0] in ["left", "right"]:
					self.matrix[wall[1], get_random(wall[2][0], wall[2][1] + 1) + 1] = 0
				else:
					self.matrix[get_random(wall[2][0], wall[2][1] + 1), wall[1] + 1] = 0

			# self.print_matrix()
			# time.sleep(1)
			# 递归
			split(lr + 2, lc + 2, cur_row - 2, cur_col - 2)
			split(lr + 2, cur_col + 2, cur_row - 2, rc - 2)
			split(cur_row + 2, lc + 2, rr - 2, cur_col - 2)
			split(cur_row + 2, cur_col + 2, rr - 2, rc - 2) 

			self.matrix[self.start[0], self.start[1]] = 0
			self.matrix[self.destination[0], self.destination[1]] = 0

		split(0, 0, self.height - 1, self.width - 1)

	# 最小生成树算法-kruskal（选边法）思想生成迷宫地图，这种实现方法最复杂。
	def generate_matrix_kruskal(self):
		# 地图初始化，并将出口和入口处的值设置为0
		self.matrix = -np.ones((self.height, self.width))

		def check(row, col):
			ans, counter = [], 0
			for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
				row_, col_ = row + d[0], col + d[1]
				if row_ > 0 and row_ < self.height - 1 and col_ > 0 and col_ < self.width - 1 and self.matrix[row_, col_] == -1:
					ans.append([d[0] * 2, d[1] * 2])
					counter += 1
			if counter <= 1:
				return []
			return ans

		nodes = set()
		row = 1
		while row < self.height:
			col = 1
			while col < self.width:
				self.matrix[row, col] = 0
				nodes.add((row, col))
				col += 2
			row += 2

		unionset = UnionSet(nodes)
		while unionset.count > 1:
			row, col = nodes.pop()
			directions = check(row, col)
			if len(directions):
				random.shuffle(directions)
				for d in directions:
					row_, col_ = row + d[0], col + d[1]
					if unionset.find((row, col)) == unionset.find((row_, col_)):
						continue
					nodes.add((row, col))
					unionset.count -= 1
					unionset.union((row, col), (row_, col_))

					if row == row_:
						self.matrix[row][min(col, col_) + 1] = 0
					else:
						self.matrix[min(row, row_) + 1][col] = 0
					break

		self.matrix[self.start[0], self.start[1]] = 0
		self.matrix[self.destination[0], self.destination[1]] = 0

	# 迷宫寻路算法dfs
	def find_path_dfs(self, destination):
		visited = [[0 for i in range(self.width)] for j in range(self.height)]

		def dfs(path):
			visited[path[-1][0]][path[-1][1]] = 1
			if path[-1][0] == destination[0] and path[-1][1] == destination[1]:
				self.path = path[:]
				return
			for d in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
				row_, col_ = path[-1][0] + d[0], path[-1][1] + d[1]
				if row_ > 0 and row_ < self.height - 1 and col_ > 0 and col_ < self.width and visited[row_][col_] == 0 and self.matrix[row_][col_] == 0:
					dfs(path + [[row_, col_]])

		dfs([[self.start[0], self.start[1]]])
	
	# 迷宫寻路算法bfs
	# def find_path_bfs(self, destination):
	# 	visited = [[0 for i in range(self.width)] for j in range(self.height)]

	# 	queue = [(self.start[0], self.start[1])]
	# 	visited[self.start[0]][self.start[1]] = 1
	# 	while len(queue) != 0:
	# 		row, col = queue.pop(0)
	# 		if 

if __name__ == '__main__':
	maze = Maze(51, 51)
	maze.generate_matrix_prim()
	maze.print_matrix()
	maze.find_path_dfs(maze.destination)
	print("answer", maze.path)
	maze.print_matrix()


