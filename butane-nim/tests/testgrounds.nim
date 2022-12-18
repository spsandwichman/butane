# matrix and vector multiplication testing

# proc `**`(a, b: array[4,array[4,float]]): array[4,array[4,float]] = # 4x4 matrix * 4x4 matrix
#     for i in 0..3:
#         for j in 0..3:
#             result[i][j] = (a[i][0] * b[0][j]) + (a[i][1] * b[1][j]) + (a[i][2] * b[2][j]) + (a[i][3] * b[3][j])

# proc `**`(b: array[4,float], a: array[4,array[4,float]]): array[4,float] = # 4d vector * 4x4 matrix
#     for i in 0..3:
#             result[i] = (a[i][0] * b[0]) + (a[i][1] * b[1]) + (a[i][2] * b[2]) + (a[i][3] * b[3])

# proc dDown(x: array[4,float]): array[3,float] = #truncates 4d vector and returns 3d vector
#     result = [x[0],x[1],x[2]]

# proc dUp(x: array[3,float]): array[4,float] = #adds 1.0 element to 3d vector, returns 4d vector
#     result = [x[0],x[1],x[2],1.0]

# var identity =  [[1.0,0.0,0.0,0.0],  
#                 [0.0,1.0,0.0,0.0],
#                 [0.0,0.0,1.0,0.0],
#                 [0.0,0.0,0.0,1.0]]

# var matrix1 =  [[9.0,2.0,3.0,5.0],  
#                 [1.0,9.0,2.0,7.0],
#                 [0.0,6.0,4.0,3.0],
#                 [3.0,3.0,5.0,5.0]]

# var vector1 = [3.0,6.0,8.0]

# echo dDown(dUp(vector1) ** (identity ** matrix1))

import strfmt

type Matrix[M, N: static[int]] = array[M, array[N, float]]

let a = [[1.0,  1.0,  1.0,   1.0],
         [2.0,  4.0,  8.0,  16.0],
         [3.0,  9.0, 27.0,  81.0],
         [4.0, 16.0, 64.0, 256.0]]

let b = [[4.0],[-3.0],[1.0],[-10.0]]


proc `$`(m: Matrix): string =
  result = "(["
  for r in m:
    if result.len > 2: result.add "]\n ["
    for val in r: result.add val.format("8.2f")
  result.add "])"

proc `**`[M, P, N](a: Matrix[M, P]; b: Matrix[P, N]): Matrix[M, N] =
  for i in result.low .. result.high:
    for j in result[0].low .. result[0].high:
      for k in a[0].low .. a[0].high:
        result[i][j] += a[i][k] * b[k][j]

echo a
echo b
echo a ** b