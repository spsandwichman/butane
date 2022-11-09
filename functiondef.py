from numpy import *

white = array([255, 255, 255])
black = array([0, 0, 0])
red = array([255, 0, 0])
green = array([0, 255, 0])
blue = array([0, 0, 255])


class Object:
    def __init__(self, position, rotation, scale, obj_space_vertex_table, edge_table, surface_table):
        self.pos = position
        self.rot = rotation
        self.scl = scale

        self.objSpaceVertexTable = obj_space_vertex_table
        self.wldSpaceVertexTable = obj_space_vertex_table
        self.edgeTable = edge_table
        self.surfaceTable = surface_table
        self.update_wld_space_vertex_table()

    def update_wld_space_vertex_table(self):
        for vertex in range(len(self.objSpaceVertexTable)):
            self.wldSpaceVertexTable[vertex] = translate_vertex(
                rotate_vertex(scale_vertex(self.objSpaceVertexTable[vertex], self.scl), self.rot),
                self.pos)  # I am so sorry

    def translate(self, pos_difference):
        self.pos = self.pos + pos_difference  # update position variable
        self.update_wld_space_vertex_table()

    def rotate(self, rot_difference):
        self.rot = self.rot + rot_difference
        self.update_wld_space_vertex_table()

    def scale(self, scl_difference):
        self.scl = self.scl * scl_difference
        self.update_wld_space_vertex_table()

    def set_pos(self, new_pos):
        self.pos = new_pos
        self.update_wld_space_vertex_table()

    def set_rot(self, new_rot):
        self.rot = new_rot
        self.update_wld_space_vertex_table()

    def set_scale(self, new_scl):
        self.scl = new_scl
        self.update_wld_space_vertex_table()

    def set_geometry(self, new_obj_vertex_table, new_edge_table, new_surface_table):
        self.objSpaceVertexTable = new_obj_vertex_table
        self.wldSpaceVertexTable = new_obj_vertex_table
        self.update_wld_space_vertex_table()
        self.edgeTable = new_edge_table
        self.surfaceTable = new_surface_table


class Empty:
    def __init__(self, position=array([0, 0, 0]), rotation=array([0, 0, 0]), scale=array([1, 1, 1])):
        self.pos = position
        self.rot = rotation
        self.scl = scale

    def translate(self, pos_difference):
        self.pos = self.pos + pos_difference  # update position variable

    def rotate(self, rot_difference):
        self.rot = self.rot + rot_difference

    def scale(self, scale_difference):
        self.scl = self.scl * scale_difference

    def set_pos(self, new_pos):
        self.pos = new_pos

    def set_rot(self, new_rot):
        self.rot = new_rot

    def set_scale(self, new_scale):
        self.scl = new_scale


class Camera:
    def __init__(self, position=array([0, 0, 0]), rotation=array([0, 0, 0]), scale=array([1, 1, 1]), focal_length=5,
                 shift_x=0, shift_y=0):
        self.pos = position
        self.rot = rotation
        self.scl = scale
        self.fL = focal_length
        self.sX = shift_x
        self.sY = shift_y

    def translate(self, pos_difference):
        self.pos = self.pos + pos_difference  # update position variable

    def rotate(self, rot_difference):
        self.rot = self.rot + rot_difference

    def scale(self, scale_difference):
        self.scl = self.scl * scale_difference

    def change_fl(self, fl_difference):
        self.fL = self.fL + fl_difference

    def shift_view_plane(self, diff_x, diff_y):
        self.sX = self.sX + diff_x
        self.sY = self.sY + diff_y

    def set_pos(self, new_pos):
        self.pos = new_pos

    def set_rot(self, new_rot):
        self.rot = new_rot

    def set_scl(self, new_scl):
        self.scl = new_scl

    def set_fl(self, new_fl):
        self.fL = new_fl


class Screen:
    def __init__(self, width, height):
        self.pixels = full((width, height, 3), 0, dtype=uint8)
        self.res = (width, height)
        self.height = height
        self.width = width

    def change_resolution(self, new_height, new_width):
        self.height = new_height
        self.width = new_width
        self.res = (new_height, new_width)

    def draw_pixel(self, point, color):
        px, py = point
        # print(str(px) + ' ' + str(py))
        self.pixels[px][py] = color

    def draw_line(self, point0, point1, color):  # bresenham magic
        x0, y0 = point0[0], point0[1]
        x1, y1 = point1[0], point1[1]
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < x1 else -1
        error = dx + dy
        while True:
            self.draw_pixel((x0, y0), color)
            if (x0 == x1) and (y0 == y1):
                break
            e2 = 2 * error
            if e2 >= dy:
                if x0 == x1:
                    break
                error = error + dy
                x0 = x0 + sx
            if e2 <= dx:
                if y0 == y1:
                    break
                error = error + dx
                y0 = y0 + sy


def translate_vertex(vertex, trn):
    return vertex + trn


def rotate_vertex(vertex, rot, origin=array([0, 0, 0])):
    x_rot_matrix = array([
        [1, 0, 0],  # x-axis rotation matrix
        [0, cos(rot[0]), sin(rot[0])],
        [0, -sin(rot[0]), cos(rot[0])],
    ])
    y_rot_matrix = array([
        [cos(rot[1]), 0, -sin(rot[1])],  # y-axis rotation matrix
        [0, 1, 0],
        [sin(rot[1]), 0, cos(rot[1])],
    ])
    z_rot_matrix = array([
        [cos(rot[2]), sin(rot[2]), 0],  # z-axis rotation matrix
        [-sin(rot[2]), cos(rot[2]), 0],
        [0, 0, 1],
    ])
    rot_matrix = matmul(matmul(x_rot_matrix, y_rot_matrix), z_rot_matrix)  # compound rotation matrix

    return matmul((vertex - origin).T, rot_matrix).T + origin  # magic


def scale_vertex(vertex, scl, origin=array([0, 0, 0])):
    return ((vertex - origin) * scl) + origin


def project(vertex, camera, screen):
    rotated_vertex = rotate_vertex(vertex, camera.rot, camera.pos)  # transform into camera space

    projected_x = ((camera.fL / rotated_vertex[2]) * rotated_vertex[0]) + camera.sX  # project onto view plane
    projected_y = ((camera.fL / rotated_vertex[2]) * rotated_vertex[1]) + camera.sY  # project onto view plane

    rotated_vertex[2] = 0.000001 if rotated_vertex[2] == 0 else rotated_vertex[2]  # prevents division by zero

    projected_x = (projected_x * 10) + (screen.width / 2)
    projected_y = (projected_y * 10) + (screen.height / 2)

    return array([projected_x, projected_y], int32)


def r(old_degrees):
    return deg2rad(old_degrees)


def d(old_radians):
    return rad2deg(old_radians)


Cube = Object(
    array([0, 0, 0]),  # position
    array([0, 0, 0]),  # rotation
    array([1, 1, 1]),  # scale
    array([  # vertex table
        [-1, -1, -1],  # 0
        [-1, -1, 1],  # 1
        [-1, 1, -1],  # 2
        [-1, 1, 1],  # 3
        [1, -1, -1],  # 4
        [1, -1, 1],  # 5
        [1, 1, -1],  # 6
        [1, 1, 1]]),  # 7
    array([  # edge table
        [0, 1],  # 0
        [0, 2],  # 1
        [0, 4],  # 2
        [1, 2],  # 3
        [1, 3],  # 4
        [1, 4],  # 5
        [1, 5],  # 6
        [1, 7],  # 7
        [2, 3],  # 8
        [2, 4],  # 9
        [2, 6],  # 10
        [2, 7],  # 11
        [3, 7],  # 12
        [4, 5],  # 13
        [4, 6],  # 14
        [4, 7],  # 15
        [5, 7],  # 16
        [6, 7]]),  # 17
    array([  # surface table
        [0, 1, 3],  # 0
        [0, 2, 5],  # 1
        [1, 2, 9],  # 2
        [3, 7, 8],  # 3
        [4, 7, 12],  # 4
        [6, 5, 13],  # 5
        [6, 7, 16],  # 6
        [8, 11, 12],  # 7
        [9, 10, 14],  # 8
        [10, 11, 17],  # 9
        [13, 15, 16],  # 10
        [14, 15, 17]])  # 11
)

Pyramid = Object(
    array([0, 0, 0]),  # position
    array([0, 0, 0]),  # rotation
    array([1, 1, 1]),  # scale
    array([  # vertex table
        [-1, -1, -1],  # 0
        [-1, 1, -1],  # 1
        [1, -1, -1],  # 2
        [1, 1, -1],  # 3
        [0, 0, 1]]),  # 4
    array([  # edge table
        [0, 1],  # 0
        [0, 2],  # 1
        [0, 3],  # 2
        [0, 4],  # 3
        [1, 3],  # 4
        [1, 4],  # 5
        [2, 3],  # 6
        [2, 4],  # 7
        [3, 4]]),  # 8
    array([  # surface table
        [0, 2, 4],  # 0
        [0, 3, 5],  # 1
        [1, 2, 6],  # 2
        [1, 3, 7],  # 3
        [4, 5, 8],  # 4
        [6, 7, 8]])  # 5
)
