from numpy import *

m1 = matrix([
		[5, 3, 9, 3],
		[4, 1, 6, 5],
		[6, 2, 4, 8],
		[2, 1, 3, 4]])

m2 = matrix([
		[7, 3, 9, 3],
		[4, 1, 6, 5],
		[6, 2, 4, 6],
		[2, 1, 3, 8]])
Arr = array([-1, 6, 1, 4])

print(matmul(matmul(m1,m2),Arr))
print(m1*m2*Arr)