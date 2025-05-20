from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image  # 需要安装PIL库来加载图片


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

# 四肢管理
class Limbs(object):
    def __init__(self, is_arm, is_left):
        self.x_rotate = 0
        self.z_rotate = 0    # 控制arm微张
        self.is_arm = is_arm  # 是否是手臂
        self.is_left = is_left  # 是否是左边的手，从摄像机视角看，（其实就是人物右手）

        self._z_rotate_rate = -0.3 
        self.MAX_Z_ROTATE = 7

        self.run_direction = 1
        self.MAX_X_ROTATE = 40

    def update(self, if_run, run_speed=8):
        if self.is_arm:
            # 自然动作z轴晃动
            if self.is_left:    # 左arm
                self.z_rotate += self._z_rotate_rate
                if self.z_rotate < -self.MAX_Z_ROTATE or self.z_rotate >= 0:
                    self._z_rotate_rate = -self._z_rotate_rate
            else:     # 右arm
                self.z_rotate -= self._z_rotate_rate
                if self.z_rotate > self.MAX_Z_ROTATE or self.z_rotate <= 0:
                    self._z_rotate_rate = -self._z_rotate_rate
            # 跑步动作x轴转动
            if if_run:
                if self.is_left:
                    self.x_rotate += run_speed * self.run_direction
                else:
                    self.x_rotate -= run_speed * self.run_direction
                if abs(self.x_rotate) > self.MAX_X_ROTATE:
                    self.run_direction = -self.run_direction
            else:
                # 停止跑步但是肢体没有回位
                if self.x_rotate > 0:
                    self.x_rotate -= 1
                elif self.x_rotate < 0:
                    self.x_rotate += 1


        else:
            # 腿部动作
            if if_run:
                if self.is_left:
                    # 左腿
                    self.x_rotate -= run_speed * self.run_direction
                else:
                    self.x_rotate += run_speed * self.run_direction
                if abs(self.x_rotate) > self.MAX_X_ROTATE:
                    self.run_direction = -self.run_direction
            else:
                # 停止跑步但是肢体没有回位
                if self.x_rotate > 0:
                    self.x_rotate -= 1
                elif self.x_rotate < 0:
                    self.x_rotate += 1



    def draw(self):
        glColor4f(1.0, 1.0, 1.0, 1.0)  # 默认白色纹理
        if ENABLE_LIGHT:
            mat_diffuse = [1.0, 1.0, 1.0, 1.0]
            glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        if self.is_arm and self.is_left:
            glTranslatef(-1.0, -1.0, 0.0)
            glRotatef(self.z_rotate, 0, 0, 1)
            glTranslatef(1.0, 1.0, 0.0)
            glTranslatef(-1.0, -1.5, 0.0)
            glRotatef(self.x_rotate, 1, 0, 0)
            glTranslatef(1.0, 1.5, 0.0)
            # 左arm
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

        elif self.is_arm and not self.is_left:
            glTranslatef(1.0, -1.0, 0.0)
            glRotatef(self.z_rotate, 0, 0, 1)
            glTranslatef(-1.0, 1.0, 0.0)
            glTranslatef(1.0, -1.5, 0.0)
            glRotatef(self.x_rotate, 1, 0, 0)
            glTranslatef(-1.0, 1.5, 0.0)
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

        elif not self.is_arm and self.is_left:
            glTranslatef(-0.5, -4.0, 0.0)
            glRotatef(self.x_rotate, 1, 0, 0)
            glTranslatef(0.5, 4.0, 0.0)
            # 左leg
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
        elif not self.is_arm and not self.is_left:
            glTranslatef(0.5, -4.0, 0.0)
            glRotatef(self.x_rotate, 1, 0, 0)
            glTranslatef(-0.5, 4.0, 0.0)
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




# 用来统一管理四肢状态，同步更新
class Steve():
    def __init__(self, model_path, _ENABLE_LIGHT):
        global ENABLE_LIGHT
        ENABLE_LIGHT = _ENABLE_LIGHT
        # 加载纹理
        load_texture(model_path)
        # 初始化四肢
        self.left_arm = Limbs(is_arm=True, is_left=True)
        self.right_arm = Limbs(is_arm=True, is_left=False)
        self.left_leg = Limbs(is_arm=False, is_left=True)
        self.right_leg = Limbs(is_arm=False, is_left=False)
        # 用于鼠标跟随
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        # 身体转向
        self.body_rotate_y = 0.0
        # 头部转向
        self.head_rotate_x = 0.0
        self.head_rotate_y = 0.0
        # 跳跃控制
        self.if_jump = False
        self.jump_height = 0.0
        self.jump_timer = 0
        self.jump_timer_MAX = 18
        self.jump_speed = 0.2
        # 跑步速度控制
        self.if_run = False
        self.run_speed = 0

    def jump(self):
        if self.if_jump:
            return
        # 启动跳跃
        self.if_jump = True
        self.jump_timer = self.jump_timer_MAX

    def add_run_speed(self, num):
        self.run_speed += num
        if self.run_speed <= 0:
            self.run_speed = 0
            self.if_run = False
        else:
            self.if_run = True

    def set_run_speed(self, num):
        self.run_speed = num
        if self.run_speed <= 0:
            self.run_speed = 0
            self.if_run = False
        else:
            self.if_run = True

    def motion(self, x, y, last_x, last_y, is_dragging):
        # 处理用户鼠标移动事件
        if is_dragging:
            dx = x - last_x
            dy = y - last_y
            
            self.head_rotate_y += dx * 0.5
            self.head_rotate_x += dy * 0.5
            
            last_x = x
            last_y = y
        return last_x, last_y


    # pt: ctypes.wintypes.POINT() 鼠标在屏幕中的位置
    def update(self, pt, window_x, window_y, window_width, window_height):
        # 计算窗口中心在屏幕中的坐标
        center_x = window_x + window_width // 2
        center_y = window_y + window_height // 2
            
        self.mouse_offset_x = pt.x - center_x
        self.mouse_offset_y = pt.y - center_y

        # print(self.mouse_offset_x, self.mouse_offset_y)

        # 计算身体偏转, 头部旋转带动身体
        _head_rotate_y = self.head_rotate_y+self.mouse_offset_x/18
        if _head_rotate_y - self.body_rotate_y > 30:
            self.body_rotate_y = _head_rotate_y - 30
        elif self.body_rotate_y - _head_rotate_y > 30:
            self.body_rotate_y = _head_rotate_y + 30
        self.left_arm.update(self.if_run, self.run_speed)
        self.right_arm.update(self.if_run, self.run_speed)
        self.left_leg.update(self.if_run, self.run_speed)
        self.right_leg.update(self.if_run, self.run_speed)

        if self.if_jump:
            if self.jump_timer <= self.jump_timer_MAX / 2:
                self.jump_height -= self.jump_speed
            else:
                self.jump_height += self.jump_speed
            self.jump_timer -= 1
            if self.jump_timer == 0:
                self.jump_height = 0
                self.if_jump = False


    def draw(self):
        # 跳跃高度
        glPushMatrix()
        if True:
            glTranslatef(0.0, self.jump_height, 0.0)

            # 绘制头部
            # 应用旋转 + offset鼠标跟随
            glPushMatrix()
            glRotatef(self.head_rotate_x+self.mouse_offset_y/18, 1, 0, 0)
            glRotatef(self.head_rotate_y+self.mouse_offset_x/18, 0, 1, 0)
            _draw_head()    # 绘制头部
            _draw_hair()    # 绘制头发
            glPopMatrix()

            # 绘制身体，四肢
            if True:
                glPushMatrix()    
                glRotatef(self.body_rotate_y, 0, 1, 0)
                _draw_body()  

                if True:  # 画手臂
                    glPushMatrix()
                    self.left_arm.draw()
                    glPopMatrix()
                    glPushMatrix()
                    self.right_arm.draw()
                    glPopMatrix()

                if True:  # 画腿
                    glPushMatrix()
                    self.left_leg.draw()
                    glPopMatrix()
                    glPushMatrix()
                    self.right_leg.draw()
                    glPopMatrix()

                glPopMatrix()
        glPopMatrix()




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