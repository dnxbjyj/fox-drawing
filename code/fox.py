# coding:utf-8
# 画小狐狸
from turtle import *
from math import *
import time

def init():  # 初始化
    mode('logo')  # 设置mode为logo
    shape('turtle')  # 设置画笔形状
    pensize(5)  # 设置画笔粗细
    speed(0)
    skip_to_home()

def ang2rad(angle):
    '''
    角度转弧度

    :param angle: 角度
    :type angle: float

    :return: 弧度值
    :rtype: float
    '''
    return float(angle)/180 * pi

def ellipse(x, y, a,b,angle,steps,rotate_angle, clockwise = False):
    '''
    以(x, y)点为b轴上端点下标绘制两轴长分别为a、b的椭圆，绘制angle度，步数为steps，椭圆相对于水平位置旋转rotate_angle度

    :param x: 起点横坐标
    :type x: float

    :param y: 起点纵坐标
    :type y: float

    :param a: 椭圆轴长
    :type a: float

    :param b: 椭圆轴长
    :type b: float

    :param angle: 绘制角度
    :type angle: float

    :param steps: 绘制步数
    :type steps: int

    :param rotate_angle: 相对于水平位置旋转角度
    :type rotate_angle: float

    :return: 绘制完椭圆后画笔所在坐标和朝向
    :rtype: ((float, float), float)
    '''
    min_rad = ang2rad(angle) / steps
    rotate_rad = ang2rad(rotate_angle)
    penup()
    if clockwise:
        x_diff = x + b*sin(rotate_rad)
        y_diff = y - b*cos(rotate_rad)
    else:
        x_diff = x - b*sin(rotate_rad)
        y_diff = y + b*cos(rotate_rad)
    setpos(x, y)
    pendown()
    for i in range(steps):
        if clockwise:
            next_point = [a*sin((i+1)*min_rad), b*cos((i+1)*min_rad)]
        else:
            next_point = [a*sin((i+1)*min_rad), -b*cos((i+1)*min_rad)]
        next_point = [x_diff + next_point[0]*cos(rotate_rad)-next_point[1]*sin(rotate_rad),
                     y_diff + next_point[0]*sin(rotate_rad)+next_point[1]*cos(rotate_rad)]
        setpos(next_point)
    return (pos(), heading())

def skip_forward(step):
    '''
    抬笔，前进step像素，返回最终位置的坐标

    :param step: 前进的像素值，如果为负数，则后退step像素
    :type step: int

    :return: (x, y)，最终位置的下标
    :rtype: (float, float)
    '''
    penup()
    forward(step)
    pendown()
    return pos()
    
def skip_to_home():
    '''
    抬笔，回到原点

    :return: None
    :rtype: None
    '''
    penup()
    home()
    pendown()
    
def skip_to(x, y):
    '''
    抬笔，前进到(x,y)坐标位置

    :param x: 横坐标
    :type x: float

    :param y: 纵坐标
    :type y: float

    :return: None
    :rtype: None
    '''
    penup()
    goto(x, y)
    pendown()

def draw_arc(radius, angle):
    '''
    以当前坐标为圆心，当前朝向为弧的起点位置，radius为半径，画角度为angle的圆弧。
    当angle为正数时，逆时针画；当angle为负数时，顺时针画。
    返回圆弧的起始位置和终止位置坐标、朝向

    :param radius: 圆弧半径
    :type radius: int

    :param angle: 圆弧角度
    :type angle: int

    :return: (((start_x, start_y), start_heading), (end_x, end_y), end_heading) 圆弧起始位置、终止位置坐标、朝向
    :rtype: (((float, float), float), (float, float), float)
    '''
    # 记录原始朝向和位置
    raw_heading = heading()
    raw_pos = pos()

    # 画圆弧
    start_pos = skip_forward(radius)
    left(90)
    start_heading = heading()
    circle(radius, angle)
    end_pos = pos()
    end_heading = heading()

    # 回到起始位置，恢复朝向
    skip_to(raw_pos[0], raw_pos[1])
    setheading(raw_heading)
    return ((start_pos, start_heading), (end_pos, end_heading))
    
def nose(radius = 20):
    '''
    画鼻子
    规格：鼻子为一个圆圈

    :param nose_radius: 鼻子圆圈半径（像素）
    :type nose_radius: int

    :return: None
    :rtype: None
    '''
    skip_to(radius, 0)
    fillcolor('white')
    begin_fill()
    circle(radius)
    end_fill()
    skip_to_home()

def head_top():
    '''
    画头顶

    :return: None
    :rtype: None
    '''
    # 头顶的起始、终止位置坐标（逆时针计算）
    global head_top_start_location, head_top_end_location
    
    right(20)  # 向右转20度

    # 画头顶的圆弧
    head_top_start_location,head_top_end_location = draw_arc(210, 40)
    
    # 回到原点
    skip_to_home()

def face():
    '''
    画脸

    :return: None
    :rtype: None
    '''
    # 脸和耳朵连接的圆弧
    right(70)
    # 右侧
    draw_arc(210, 25)
    # 左侧
    skip_to_home()
    left(45)
    draw_arc(210, 25)

    # 两侧脸的圆弧
    skip_to_home()
    # 左右脸圆弧角度
    face_angle = 180 - (90 - 20) * 2
    # 左侧
    # 计算左侧脸圆弧的圆心下标
    left_circle_center_x = -210 * cos(ang2rad((180-40-20*2-30*2) / 2.0))
    left_circle_center_y = left_circle_center_x / (tan(ang2rad(face_angle)))
    # 左右脸圆弧半径
    face_radius = -left_circle_center_y + 210 * sin(ang2rad((180-40-20*2-30*2) / 2.0))
    # 画左侧脸
    skip_to(left_circle_center_x, left_circle_center_y)
    draw_arc(face_radius, -face_angle)
    
    # 右侧
    skip_to_home()
    right_circle_center_x = -left_circle_center_x
    right_circle_center_y = left_circle_center_y
    skip_to(right_circle_center_x, right_circle_center_y)
    draw_arc(face_radius, face_angle)

    # 回到原点
    skip_to_home()

def ears():
    '''
    画左右耳朵

    :return: None
    :rtype: None
    '''
    # 左耳
    left_start_pos,_ = head_top_end_location
    ellipse(left_start_pos[0], left_start_pos[1], 120, 43.5, 174.5, 300, 130, False)

    # 回到原点
    skip_to_home()

    # 右耳
    right_start_pos,_ = head_top_start_location
    ellipse(right_start_pos[0], right_start_pos[1], 120, 43.5, 174.5, 300, 50, True)

    # 回到原点
    skip_to_home()

def pinnas():
    # 左耳廓
    # left_start_pos,_ = head_top_end_location
    left_pinna_start_pos = (-98.17,205.20)
    ellipse(left_pinna_start_pos[0], left_pinna_start_pos[1], 85, 35, 75, 300, 130, False)
    skip_to(left_pinna_start_pos[0], left_pinna_start_pos[1])
    setheading(130)
    circle(-20,170)

    # 回到原点
    skip_to_home()

    # 右耳廓
    # right_start_pos,_ = head_top_start_location
    right_pinna_start_pos = (86.37,192.62)
    ellipse(right_pinna_start_pos[0], right_pinna_start_pos[1], 100, 35, 75, 300, 50, True)
    skip_to(right_pinna_start_pos[0], right_pinna_start_pos[1])
    setheading(125)
    forward(45)

    # 回到原点
    skip_to_home()

def eyes():
    '''
    画眼睛

    :return: None
    :rtype: None
    '''
    # 左眼
    skip_to(-70, 90)
    right(30)
    draw_arc(40, 90)

    skip_to_home()
    
    # 右眼
    skip_to(70, 90)
    left(30)
    draw_arc(40, -90)
    
    skip_to_home()

def main():
    init()
    # time.sleep(3)
    head_top()
    ears()
    pinnas()
    face()
    nose()
    eyes()
    hideturtle()
    mainloop()

if __name__ == '__main__':
    main()
