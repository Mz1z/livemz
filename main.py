from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PIL import Image  # 需要安装PIL库来加载图片

import time

from ctypes import windll
import ctypes.wintypes


from steve import Steve, Limbs

FPS = 30   # 设置刷新率，如果要更改需要调整跟刷新率有关的参数


# 全局变量保存鼠标位置
last_x = 0
last_y = 0

is_dragging = False

ENABLE_LIGHT = False
LIGHT_POSITION = [-1.0, 1.0, 2.0, 0.0]


# 摄像机初始坐标
g_camera_z = 20
g_camera_x = 0
g_camera_y = 0


def init():
    glEnable(GL_DEPTH_TEST)  # 启用深度测试
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置背景颜色为黑色

    if ENABLE_LIGHT:
        # 添加光照
        # 启用光照
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        # 设置光源位置 LIGHT_POSITION全局变量
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)

        # 设置光源颜色
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

        # 设置全局材质
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 0.0)

    # 初始化steve小人
    global steve_mz
    steve_mz = Steve("model/mz.png", ENABLE_LIGHT)
    

def draw_light_ball():
    # 保存当前矩阵状态
    glPushMatrix()
    # 移动到光源位置
    glTranslatef(LIGHT_POSITION[0], LIGHT_POSITION[1], LIGHT_POSITION[2])
    # 绘制一个小球
    glutSolidSphere(0.1, 10, 10)  # 半径为 0.1，细分程度为 10x10    
    # 恢复矩阵状态
    glPopMatrix()

def display():
    global offset_x, offset_y   # 用于鼠标跟随
    global g_camera_z, g_camera_x, g_camera_y
    global g_left_arm, g_right_arm, g_left_leg, g_right_leg
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    gluLookAt(g_camera_x, g_camera_y, g_camera_z, 
        g_camera_x, g_camera_y, 0, 
        0, 1, 0)

    if ENABLE_LIGHT:
        # 刷新光照
        # glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
        pass
    
    steve_mz.draw()

    # draw_light_ball()  # 用于测试光源
    
    glutSwapBuffers()

def reshape(width, height):
    global window_width, window_height
    window_width = width
    window_height = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def mouse(button, state, x, y):
    global is_dragging, last_x, last_y
    global g_camera_z
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            is_dragging = True
            last_x = x
            last_y = y
        else:
            is_dragging = False
    # 3 == GLUT_WHEEL_UP  4 == GLUT_WHEEL_DOWN
    _change_rate = 0.3
    if state == GLUT_UP and button == 3:
        g_camera_z -= _change_rate
    if state == GLUT_UP and button == 4:
        g_camera_z += _change_rate

def motion(x, y):
    global last_x, last_y, is_dragging
    last_x, last_y = steve_mz.motion(x, y, last_x, last_y, is_dragging)
    # glutPostRedisplay()

def keyboard(key, x, y):
    global g_camera_x, g_camera_y
    _change_rate = 0.3

    if ord(key) == 27:  # ESC键
        glutLeaveMainLoop()
    elif key == b'W' or key == b'w':
        g_camera_y += _change_rate
    elif key == b'A' or key == b'a':
        g_camera_x -= _change_rate
    elif key == b'S' or key == b's':
        g_camera_y -= _change_rate
    elif key == b'D' or key == b'd':
        g_camera_x += _change_rate
    elif key == b' ':
        steve_mz.jump()



# 刷新线程
def flush_thread(id):
    global window_width, window_height
    
    window_x = glutGet(GLUT_WINDOW_X)   # 获取窗口坐标
    window_y = glutGet(GLUT_WINDOW_Y)

    # 获取当前鼠标位置（包括窗口外）
    # 注意：这仅在Windows上有效，其他平台需要其他方法
    pt = ctypes.wintypes.POINT()
    windll.user32.GetCursorPos(ctypes.byref(pt))

    # print(pt.x, pt.y)  # 鼠标在屏幕中的位置

    # 更新躯体动画
    steve_mz.update(pt, window_x, window_y, window_width, window_height)
        
    glutPostRedisplay()
    glutTimerFunc(1000//FPS, flush_thread, 1);   # 刷新计时器




# 初始化GLUT
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow(b"livemz")

init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutKeyboardFunc(keyboard)

glutTimerFunc(1000//FPS, flush_thread, 1); # glutTimerFunc(毫秒数, 回调函数指针, 区别值);

glutMainLoop()