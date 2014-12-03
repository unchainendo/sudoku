import csv
import copy
import sys



sys.setrecursionlimit(10000000)


class Tui:
	def pos(self, x, y):
		sys.stdout.write("\033[%d;%dH" % (y + 1, x + 1))
		sys.stdout.flush()
		return self

	def clear(self):
		print("\033[2J")
		return self

	def out(self, s):
		print(s)
		return self


class matrix_stage:
	def __init__(self, csvList):
		self.mat = csvList
		self.checkmat = [[0 for x in range(9)] for x in range(9)]
		self.checkblo = [[0 for x in range(3)] for x in range(3)]
		self.checkbrank = [[0 for x in range(3)] for x in range(3)]
		self.prevalue = []
		self.endo = 0

	def check_rowcol(self, num):
		for i in range(9):
			if num in self.mat[i]:
				self.checkmat[i] = [num] * 9
			if num in [self.mat[x][i] for x in range(9)]:
				for x in range(9):
					self.checkmat[x][i] = num
		for i in range(9):
			for j in range(9):
				if self.mat[i][j] != 0:
					self.checkmat[i][j] = num

	def check_block(self, num):
		for i in range(9):
			for j in range(9):
				if self.mat[i][j] == num:
					self.checkblo[i // 3][j // 3] = 1

	def check_brank(self):
		for i in range(9):
			for j in range(9):
				if self.checkmat[i][j] == 0:
					self.checkbrank[i // 3][j // 3] += 1

	def fill(self, num):
		counter = 0
		for i in range(9):
			for j in range(9):
				if self.checkmat[i][j] == 0 and self.checkblo[i // 3][j // 3] == 0 and self.checkbrank[i // 3][j // 3] == 1:
					self.mat[i][j] = num
					counter += 1
		return counter

	def reset_mat(self):
		self.checkmat = [[0 for x in range(9)] for x in range(9)]
		self.checkblo = [[0 for x in range(3)] for x in range(3)]
		self.checkbrank = [[0 for x in range(3)] for x in range(3)]

	def check_fin(self):
		sum = 0
		for i in range(9):
			for j in range(9):
				sum += self.mat[i][j]
		if sum == 405:
			return 1
		else:
			return 0

	def check_rowcolblock(self, i, j, num):
		self.check_block(num)
		if num in self.mat[i]:
			return 0
		elif num in [self.mat[x][j] for x in range(9)]:
			return 0
		elif self.checkblo[i // 3][j // 3] == 1:
			return 0
		else:
			return 1

	def try_error(self, pre_num):
		flag = 0
		for i in range(9):
			for j in range(9):
				if self.mat[i][j] == 0:
					for num in range(pre_num + 1, 10):
						flag = self.check_rowcolblock(i, j, num)
						if flag == 1:
							self.mat[i][j] = num
							self.prevalue.append([i, j, num])
							self.reset_mat()
							return 0
						else:
							self.reset_mat()
					self.reset_mat()
					pre_i = self.prevalue[len(self.prevalue) - 1][0]
					pre_j = self.prevalue[len(self.prevalue) - 1][1]
					pre_num = self.prevalue[len(self.prevalue) - 1][2]
					self.mat[pre_i][pre_j] = 0
					del self.prevalue[len(self.prevalue) - 1]
					return pre_num


def main():
	argvs = sys.argv
	csv_name = argvs[1]
	f = open(csv_name, 'r')
	reader = csv.reader(f)
	data = [[int(elm) if elm != '' else 0 for elm in v] for v in reader]
	for row in data:
		print(row)
	print()
	sudoku = matrix_stage(data)
	while sudoku.check_fin() == 0:
		counter = 0
		for x in range(1, 10):
			sudoku.check_rowcol(x)
			sudoku.check_block(x)
			sudoku.check_brank()
			counter += sudoku.fill(x)
			sudoku.reset_mat()
		if counter == 0:
			pre = 0
			disp = Tui()
			while sudoku.check_fin() == 0:
				pre = sudoku.try_error(pre)
				disp.clear()
				disp.pos(0, 0)
				for x in range(9):
					print(sudoku.mat[x])
			sudoku.try_error(0)

	print('mat')
	for x in range(9):
		print(sudoku.mat[x])

if __name__ == '__main__':
	main()
