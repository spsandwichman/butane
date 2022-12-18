# bLine - linear algebra library

import strfmt

type Matrix*[R,C: static(int)] = array[R, array[C,float]] #R: number of rows, C: number of columns
type ColVector*[E: static(int)] = Matrix[E,1]
type RowVector*[E: static(int)] = Matrix[1,E]

proc `$`*(m: Matrix): string =
    result = "[["
    for r in m:
        if result.len > 2: result.add "]\n ["
        for val in r: result.add val.format("8.4f")
    result.add "]]"
        
# --------------------------------- transpose -------------------------------- #
proc t*[R,C](m: var Matrix[R,C]): Matrix[R,C] =
    for i in 0..(R-1):
        for j in 0..(C-1):
            result[i][j] = m[j][i]

proc t*[E](v: var RowVector[E]): ColVector[E] =
    for i in 0..(E-1):
            result[i][0] = v[0][i]

proc t*[E](v: var ColVector[E]): RowVector[E] =
    for i in 0..(E-1):
            result[0][i] = v[i][0]

# ---------------------------------- length ---------------------------------- #



# -------------------------------- determinant ------------------------------- #
proc det*[E](m: Matrix[E,E]): float =
    result = 0.0

var vec: RowVector[5] = [[1.0,2.0,3.0,4.0,5.0]]

var mat: Matrix[5,5] = [
    [1.0,2.0,3.0,4.0,5.0],
    [2.0,3.0,4.0,5.0,6.0],
    [3.0,4.0,5.0,6.0,7.0],
    [4.0,5.0,6.0,7.0,8.0],
    [5.0,6.0,7.0,8.0,9.0],
]


echo mat
echo mat.t
echo vec
echo vec.t