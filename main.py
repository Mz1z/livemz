from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PIL import Image  # 需要安装PIL库来加载图片

import time

from ctypes import windll
import ctypes.wintypes

# 全局变量保存鼠标位置
last_x = 0
last_y = 0

g_head_rotate_x = 0.0
g_head_rotate_y = 0.0

g_body_rotate_y = 0.0


is_dragging = False

offset_x = 0
offset_y = 0


ENABLE_LIGHT = True
ENABLE_LIGHT = False
LIGHT_POSITION = [-1.0, 1.0, 2.0, 0.0]


# 摄像机初始坐标
g_camera_z = 20
g_camera_x = 0
g_camera_y = 0



# 用于方便的进行加载贴图
# pos : (left, top, right, down)
# img Image.open后的原始png图像
# return id
g_texture_num = 0
def _load_mc_texture(pos, img):
    global g_texture_num
    g_texture_num += 1

    _img = img.crop(pos).transpose(Image.Transpose.FLIP_LEFT_RIGHT)  # 裁剪,png需要反转
    img_data = _img.convert("RGBA").tobytes()

    width, height = _img.size

    ret_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ret_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  # 按像素显示
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return ret_id


def load_texture(filename):
    global head_up_texture_id, head_front_texture_id, head_left_texture_id, \
        head_right_texture_id, head_back_texture_id, head_down_texture_id, \
        hair_up_texture_id, hair_front_texture_id, hair_left_texture_id, \
        hair_right_texture_id, hair_back_texture_id, \
        body_up_texture_id, body_front_texture_id, body_left_texture_id, \
        body_right_texture_id, body_back_texture_id, body_down_texture_id, \
        arm_up_texture_id, arm_front_texture_id, arm_left_texture_id, \
        arm_right_texture_id, arm_back_texture_id, arm_down_texture_id, \
        leg_up_texture_id, leg_front_texture_id, leg_left_texture_id, \
        leg_right_texture_id, leg_back_texture_id, leg_down_texture_id

    img = Image.open(filename)
    head_front_texture_id = _load_mc_texture((8, 8, 16, 16), img)
    head_up_texture_id = _load_mc_texture((8, 0, 16, 8), img)
    head_left_texture_id = _load_mc_texture((0, 8, 8, 16), img)
    head_right_texture_id = _load_mc_texture((16, 8, 24, 16), img)
    head_down_texture_id = _load_mc_texture((16, 0, 24, 8), img)
    head_back_texture_id = _load_mc_texture((24, 8, 32, 16), img)

    hair_up_texture_id = _load_mc_texture((40, 0, 48, 8), img)
    hair_front_texture_id = _load_mc_texture((40, 8, 48, 16), img)
    hair_left_texture_id = _load_mc_texture((32, 8, 40, 16), img)
    hair_right_texture_id =  _load_mc_texture((48, 8, 56, 16), img)
    hair_back_texture_id = _load_mc_texture((56, 8, 64, 16), img)

    body_front_texture_id = _load_mc_texture((20, 20, 28, 32), img)
    body_up_texture_id = _load_mc_texture((20, 16, 28, 20), img)
    body_left_texture_id = _load_mc_texture((28, 20, 32, 32), img)
    body_right_texture_id = _load_mc_texture((28, 20, 32, 32), img)   # 暂时和左边一样
    body_down_texture_id = _load_mc_texture((28, 16, 36, 20), img)
    body_back_texture_id = _load_mc_texture((32, 20, 40, 32), img)

    arm_front_texture_id = _load_mc_texture((44, 20, 48, 32), img)
    arm_up_texture_id = _load_mc_texture((44, 16, 48, 20), img)
    arm_left_texture_id = _load_mc_texture((40, 20, 44, 32), img)
    arm_right_texture_id = _load_mc_texture((40, 20, 44, 32), img)   # 暂时和左边一样
    arm_down_texture_id = _load_mc_texture((48, 16, 52, 20), img)
    arm_back_texture_id = _load_mc_texture((40, 20, 44, 32), img)   # 暂时和左边一样

    leg_front_texture_id = _load_mc_texture((2, 20, 8, 32), img)
    leg_up_texture_id = _load_mc_texture((4, 16, 8, 20), img)
    leg_left_texture_id = _load_mc_texture((0, 20, 4, 32), img)
    leg_right_texture_id = _load_mc_texture((8, 20, 12, 32), img)
    leg_down_texture_id = _load_mc_texture((8, 16, 12, 20), img)
    leg_back_texture_id = _load_mc_texture((12, 20, 16, 32), img) 




def _draw_hair():
    glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
    if ENABLE_LIGHT:
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # 头发up
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, hair_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.1, 1.1, 1.1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.1, 1.1, 1.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.1, 1.1, -1.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.1, 1.1, -1.1)

    glEnd()
    glDisable(GL_TEXTURE_2D)


    # 头发front
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, hair_front_texture_id)
   
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.5)
    
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.1, 1.1, 1.1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.1, 1.1, 1.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.1, -1.1, 1.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.1, -1.1, 1.1)

    glEnd()
    glDisable(GL_ALPHA_TEST)
    glDisable(GL_TEXTURE_2D)

    # 头发left
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, hair_left_texture_id)
   
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.5)
    
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.1, 1.1, 1.1)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.1, 1.1, -1.1)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.1, -1.1, -1.1)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.1, -1.1, 1.1)

    glEnd()
    glDisable(GL_ALPHA_TEST)
    glDisable(GL_TEXTURE_2D)

    # 头发right
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, hair_right_texture_id)
   
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.5)
    
    glBegin(GL_QUADS)
    glNormal3f(1.1, 0.0, 0.0)  # 法线

    glTexCoord2f(1-0.0, 0.0)
    glVertex3f(1.1, 1.1, 1.1)
    glTexCoord2f(1-1.0, 0.0)
    glVertex3f(1.1, 1.1, -1.1)
    glTexCoord2f(1-1.0, 1.0)
    glVertex3f(1.1, -1.1, -1.1)
    glTexCoord2f(1-0.0, 1.0)
    glVertex3f(1.1, -1.1, 1.1)

    glEnd()
    glDisable(GL_ALPHA_TEST)
    glDisable(GL_TEXTURE_2D)

    # 头发back
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, hair_back_texture_id)
   
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.5)
    
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(1-0.0, 0.0)
    glVertex3f(1.1, 1.1, -1.1)
    glTexCoord2f(1-1.0, 0.0)
    glVertex3f(-1.1, 1.1, -1.1)
    glTexCoord2f(1-1.0, 1.0)
    glVertex3f(-1.1, -1.1, -1.1)
    glTexCoord2f(1-0.0, 1.0)
    glVertex3f(1.1, -1.1, -1.1)

    glEnd()
    glDisable(GL_ALPHA_TEST)
    glDisable(GL_TEXTURE_2D)


def _draw_head():
    glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
    if ENABLE_LIGHT:
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面 - 绿色
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -1.0, -1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -1.0, 1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, 1.0, -1.0)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -1.0, 1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, 1.0, 1.0)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, 1.0, -1.0)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, 1.0, -1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, head_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, 1.0)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -1.0, -1.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)



def _draw_body():
    glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
    if ENABLE_LIGHT:
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4, 0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4, 0.5)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -1.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -1.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, body_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -4, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -4, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def _draw_arms():
    # 左arm
    glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
    if ENABLE_LIGHT:
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-2.0, -4, 0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -4, 0.5)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-2.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-2.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-2.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-2.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-2.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-2.0, -1.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -1.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -4, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-2.0, -4, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-2.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 右arm
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -4, 0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(2.0, -4, 0.5)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(2.0, -1.0, -0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(2.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(2.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(2.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(2.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -1.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(2.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -1.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(2.0, -1.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, arm_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(2.0, -4, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -4, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -4, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(2.0, -4, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def _draw_legs():
    # 左leg
    glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
    if ENABLE_LIGHT:
        mat_diffuse = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -7.0, 0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -7.0, 0.5)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -4.0, -0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(-1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(-1.0, -7.0, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -7.0, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -4.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -4.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -7.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(-1.0, -7.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(-1.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 右leg
    # 前面 - 使用纹理
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_front_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -7.0, 0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -7.0, 0.5)

    glEnd()
    glDisable(GL_TEXTURE_2D)

    # 后面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_back_texture_id)
    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, -1.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -4.0, -0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -7.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
  
    # 左面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_left_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(1.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(1.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -7.0, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 右面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_right_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -4.0, -0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(0.0, -7.0, 0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 上面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_up_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -4.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -4.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -4.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -4.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # 下面
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, leg_down_texture_id)
    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)  # 法线
    glTexCoord2f(0.0, 0.0);glVertex3f(1.0, -7.0, 0.5)
    glTexCoord2f(1.0, 0.0);glVertex3f(0.0, -7.0, 0.5)
    glTexCoord2f(1.0, 1.0);glVertex3f(0.0, -7.0, -0.5)
    glTexCoord2f(0.0, 1.0);glVertex3f(1.0, -7.0, -0.5)
    glEnd()
    glDisable(GL_TEXTURE_2D)



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

    
    # 加载纹理
    # load_texture("1.jpg")
    load_texture("model/mz.png")

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glLoadIdentity()
    gluLookAt(g_camera_x, g_camera_y, g_camera_z, 
        g_camera_x, g_camera_y, 0, 
        0, 1, 0)

    if ENABLE_LIGHT:
        # 刷新光照
        # glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
        pass
    
    # 绘制头部
        # 应用旋转 + offset鼠标跟随
    glPushMatrix()
    glRotatef(g_head_rotate_x+offset_y/18, 1, 0, 0)
    glRotatef(g_head_rotate_y+offset_x/18, 0, 1, 0)
    glTranslatef(0.0, 0.0, 0.0)    # 移动物体到原点
    _draw_head()    # 绘制头部
    _draw_hair()    # 绘制头发
    glPopMatrix()

    # 绘制身体
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(g_body_rotate_y, 0, 1, 0)
    _draw_body()    
    _draw_arms()
    _draw_legs()
    glPopMatrix()

    # 绘制四肢，四肢要跟着身体一起操作


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
    global g_head_rotate_x, g_head_rotate_y, last_x, last_y, is_dragging
    if is_dragging:
        dx = x - last_x
        dy = y - last_y
        
        g_head_rotate_y += dx * 0.5
        g_head_rotate_x += dy * 0.5
        
        last_x = x
        last_y = y
        glutPostRedisplay()

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




# 刷新线程
def flush_thread(id):
    global g_head_rotate_x, g_head_rotate_y, last_x, last_y, is_dragging, window_width, window_height
    global g_body_rotate_y
    global offset_x, offset_y   # 用于鼠标跟随

    window_x = glutGet(GLUT_WINDOW_X)   # 获取窗口坐标
    window_y = glutGet(GLUT_WINDOW_Y)

    # 获取当前鼠标位置（包括窗口外）
    # 注意：这仅在Windows上有效，其他平台需要其他方法
    pt = ctypes.wintypes.POINT()
    windll.user32.GetCursorPos(ctypes.byref(pt))

    # print(pt.x, pt.y)  # 鼠标在屏幕中的位置
        
    # 计算窗口中心在屏幕中的坐标
    center_x = window_x + window_width // 2
    center_y = window_y + window_height // 2
        
    offset_x = pt.x - center_x
    offset_y = pt.y - center_y

    # print(offset_x, offset_y)

    # 计算身体偏转, 头部旋转带动身体
    _head_rotate_y = g_head_rotate_y+offset_x/18
    if _head_rotate_y - g_body_rotate_y > 30:
        g_body_rotate_y = _head_rotate_y - 30
    elif g_body_rotate_y - _head_rotate_y > 30:
        g_body_rotate_y = _head_rotate_y + 30

        
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



FPS = 30
glutTimerFunc(1000//FPS, flush_thread, 1); # glutTimerFunc(毫秒数, 回调函数指针, 区别值);

glutMainLoop()