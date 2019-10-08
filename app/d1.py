
import cv2
import numpy as np

# Тут используется сегментация изоюражения
class Flow:
	img = np.empty(10, dtype = object)
	img[0] = cv2.imread('/Users/bisspector/green1.JPG')

	def __init__(self, fn):
		self.img[0] = cv2.imread(fn)
	
	a = 2
	hsv = cv2.cvtColor(img[0], cv2.COLOR_BGR2HSV) #Переводим фотографию в hsv параметры, поточу что на ней легче задать параметры цвета

	def f(self, x, y, nn, mm):         # Подсчитывам количество удовлетворяющих нас пикселей и плохих в данном квадрате     
		col = 0
		for i in range(x, min(x + self.a, nn - 1), 1):  # идем по квадрату
		
			for j in range(y, min(y + self.a, mm - 1), 1):
			
				#print(nn)
				#print('dew')
				#print(j)
				b = self.hsv.item(i, j, 0)  # Получаем значемния hsv значений
				g = self.hsv.item(i, j, 1)
				r = self.hsv.item(i, j, 2)
				if b >= 30 and b <= 90 and g >= 30 and g <= 255 and r >= 110 and r <= 255: # Удовлетворяет ли объект ашим параетрам
					col = col + 1
		return col

	def viewImage(self, image, name):   # Просмотр картинки
		cv2.namedWindow(name, cv2.WINDOW_NORMAL)
		cv2.imshow(name, image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def g(self, x, y, nn, mm): # Заполняем наш квадрат основным цветом (если в нем хороших пикселей больше чем плохих)
		for i in range(x, min(x + self.a, nn - 1), 1):
			for j in range(y, min(y + self.a, mm - 1), 1):
				b = self.hsv.item(i, j, 0)
				g = self.hsv.item(i, j, 1)
				r = self.hsv.item(i, j, 2)
				if b >= 30 and b <= 90 and g >= 30 and g <= 255 and r >= 110 and r <= 255:
					tit = 1
				else:
					self.hsv.itemset((i, j, 0), 40) # Присвоение пикселю значения
					self.hsv.itemset((i, j, 1), 50)
					self.hsv.itemset((i, j, 2), 130)

	def tt(self, x, y, nn, mm): # Заполняем квдарат побочгым цветом (если в нем плохих пикселей больше чем хороших)
		for i in range(x, min(x + self.a, nn - 1), 1):
			for j in range(y, min(y + self.a, mm - 1), 1):
				b = self.hsv.item(i, j, 0)
				g = self.hsv.item(i, j, 1)
				r = self.hsv.item(i, j, 2)
				if b > 0 and r > 0 and g > 0:
					self.hsv.itemset((i, j, 0), 255)
					self.hsv.itemset((i, j, 1), 255)
					self.hsv.itemset((i, j, 1), 255)

	def check(self, x, y, nn, mm, it): # Сколько плохих и сколько хороших пикселей в квадрате
			col = self.f(x, y, nn, mm)
			if (it > 2):
				if (col >= 3):
					self.g(x, y, nn, mm)
				else :
					if (col <= 1):
						self.tt(x, y, nn, mm)
			else:
				if (col < self.a * self.a / 2):
					self.tt(x, y, nn, mm)
				else:
					self.g(x, y, nn, mm)


	def solve(self):
		print(5)
		bb = self.hsv.item(200, 200, 0)

		# b 10 90
		# g 70 200
		# r 20 100
		self.img[0] = cv2.GaussianBlur(self.img[0], (41, 41), 0) # Немного размываем изображение

		self.hsv = cv2.cvtColor(self.img[0], cv2.COLOR_BGR2HSV) # Переводим в hsv координаты

		# g 100 255
		# r 30 140
		# b 10 110
		# 30, 30, 120]
		# 90, 255, 255]
		for t in range(3):     # Делаем сегментацию 3 раза
			print(t)
			if t > 0:
				pp = self.img[t - 1].shape        # размеры избражения
				rr = p[0]
				cc = p[1]
				self.img[t] = cv2.resize(self.img[t - 1], (int(rr / self.a), int(cc / self.a))) # уменьшаем разрешение изображения
				self.hsv = cv2.resize(self.hsv, (int(rr / self.a), int(cc / self.a)))
				print("09")
			p = self.img[t].shape
			rows = p[0]
			cols = p[1]
			print(rows)
			print(cols)
			for i in range(0, rows):            #Сегментация по кважратам (если i % a == 0 and j % a == 0 , то эта клетка - левый верхний угол квадрата)
				for j in range(0, cols):
					if i % self.a == 0 and j % self.a == 0:
						self.check(i, j, rows , cols, t)

			#for i in range(0, rows):
			#	for j in range(0, cols):
			#		if i % self.a == 1 and j % self.a == 1:
			#			self.check(i, j, rows, cols, t)

		self.img[t] = self.hsv.copy()
		self.viewImage(self.hsv, 'res')  # Просмартиваем изображение

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()

p1 = Flow(filename)
p1.solve()  #Запускаем наш клас