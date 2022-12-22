import strfmt,  std/math

type Matrix*[R,C: static(int)] = array[R, array[C,float]] #R: number of rows, C: number of columns
type Vector*[E: static(int)] = array[E, float]
type RowVector*[E: static(int)] = array[E, float]

proc toMatrix*[E](vector: RowVector[E]): Matrix[1,E] = #converts RowVector object to Matrix representation
    for i in 0..(E-1):
        result[0][i] = vector[i]
    
proc toMatrix*[E](vector: Vector[E]): Matrix[E,1] = #converts  Vector object to Matrix representation
    for i in 0..(E-1):
        result[i][0] = vector[i]

proc toRowVector*[E](matrix: Matrix[1,E]): RowVector[E] =
    for i in 0..(E-1):
        result[i] = matrix[0][i]

proc toVector*[E](matrix: Matrix[E,1]): Vector[E] =
    for i in 0..(E-1):
        result[i] = matrix[i][0]

proc `$`*(m: Matrix): string =
    result = "[["
    for r in m:
        if result.len > 2: result.add "]\n ["
        for val in r:
            result.add val.format("8.4f")
    result.add "]]"

proc `$`*(a: Vector): string = #its really for both column vectors and row vectors, just dont touch it
    let v = toMatrix(a)
    result = "[["
    for r in v:
        if result.len > 2: result.add "]\n ["
        for val in r:
            result.add val.format("8.4f")
    result.add "]]"

# --------------------------- get matrix dimensions -------------------------- #
proc rows*(m: Matrix): int = len(m)
proc cols*(m: Matrix): int = len(m[0])

# --------------------------- scalar multiplication -------------------------- #
proc `*`*[M, N](s: float, m: Matrix[M, N]): Matrix[M, N] =
    for i in 0..(M-1):
        for j in 0..(N-1):
            result[i][j] = s*m[i][j]

proc `*`*[E](s: float, v: RowVector[E]): RowVector[E] =
    for i in 0..(E-1):
        result[i] = s*v[i]

proc `*`*[E](s: float, v: Vector[E]): Vector[E] =
    for i in 0..(E-1):
        result[i] = s*v[i]

proc `/`*[M, N](m: Matrix[M, N], s: float): Matrix[M, N] =
    for i in 0..(M-1):
        for j in 0..(N-1):
            result[i][j] = m[i][j]/s

proc `/`*[E](v: RowVector[E], s: float): RowVector[E] =
    for i in 0..(E-1):
        result[i] = v[i]/s

proc `/`*[E](v: Vector[E], s: float): Vector[E] =
    for i in 0..(E-1):
        result[i] = v[i]/s

# ---------------------------- structure addition ---------------------------- #
proc `+`*[M, N](m1: Matrix[M, N], m2: Matrix[M, N]): Matrix[M, N] =
    for i in 0..(M-1):
        for j in 0..(N-1):
            result[i][j] = m1[i][j] + m2[i][j]

proc `+`*[E](v1: RowVector[E], v2: RowVector[E]): RowVector[E] =
    for i in 0..(E-1):
        result[i] = v1[i] + v2[i]

proc `+`*[E](v1: Vector[E], v2: Vector[E]): Vector[E] =
    for i in 0..(E-1):
        result[i] = v1[i] + v2[i]

proc `-`*[M, N](m1: Matrix[M, N], m2: Matrix[M, N]): Matrix[M, N] =
    for i in 0..(M-1):
        for j in 0..(N-1):
            result[i][j] = m1[i][j] - m2[i][j]

proc `-`*[E](v1: RowVector[E], v2: RowVector[E]): RowVector[E] =
    for i in 0..(E-1):
        result[i] = v1[i] - v2[i]

proc `-`*[E](v1: Vector[E], v2: Vector[E]): Vector[E] =
    for i in 0..(E-1):
        result[i] = v1[i] - v2[i]


# --------------------------------- transpose -------------------------------- #
proc t*[R,C](m: Matrix[R,C]): Matrix[C,R] =
    for i in 0..(R-1):
        for j in 0..(C-1):
            result[j][i] = m[i][j]

proc t*[E](v: RowVector[E]): Vector[E] =
    for i in 0..(E-1):
        result[i] = v[i]

proc t*[E](v: Vector[E]): RowVector[E] =
    for i in 0..(E-1):
        result[i] = v[i]

# --------------------------------- magnitude -------------------------------- #
proc mag*[E](v: Vector[E]): float =
    for i in 0..(E-1):
        result += (v[i])^2
    result = sqrt(result)

proc mag*[E](v: RowVector[E]): float =
    for i in 0..(E-1):
        result += (v[i])^2
    result = sqrt(result)

proc normalize*[E](v: Vector[E]): Vector[E] =
    result = v/mag(v)

proc normalize*[E](v: RowVector[E]): RowVector[E] =
    result = v/mag(v)

# --------------------------- cross and dot product -------------------------- #
proc cross*(a,b: Vector[3]): Vector[3] =
    result = [a[1]*b[2] - a[2]*b[1], a[2]*b[1] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

proc dot*[E](a,b: Vector[E]): float =
    for i in 0..(E-1):
        result += a[i]*b[i]

proc triNormal*(v0,v1,v2: Vector[3]) : Vector[3] =
    result = normalize(cross((v0-v1),(v1-v2)))
# --------------------------- submatrix + subvector -------------------------- #
# proc submatrix*[R,C](source: Matrix, sub: Matrix[R,C], startRow, startCol: int): Matrix[] =
#     if (startCol+subCols-1)>source.cols() or (startRow+subRows-1)>source.rows():
#         echo "error: submatrix is out of bounds of source matrix, returning blank"
#         return Matrix[subRows, subCols]

#     var a: Matrix[subRows, subCols] # initialize return submatrix
#     for subRow in 0..(subRows-1):
#         for subCol in 0..(subCols-1):
#             a[subRow][subCol] = source[subRow+startRow][subCol+startCol]
    
#     result = a



# --------------------------- matrix multiplication -------------------------- #
proc matmul*[M, P, N](a: Matrix[M, P], b: Matrix[P, N]): Matrix[M, N] =
    for i in result.low .. result.high:
        for j in result[0].low .. result[0].high:
            for k in a[0].low .. a[0].high:
                result[i][j] += a[i][k] * b[k][j]

proc `**`*[M, P, N](a: Matrix[M, P], b: Matrix[P, N]): Matrix[M, N] =
    result = matmul(a,b)

proc `**`*[M, P](a: Matrix[M, P], b: Vector[P]): Vector[M] =
    result = toVector(matmul(a,toMatrix(b)))

proc `**`*[M, P](a: Matrix[M, P], b: RowVector[M]): RowVector[P] =
    result = toRowVector(matmul(a,toMatrix(b)))