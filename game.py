from hashlib import new
import re
import time
from tkinter import CENTER
from tkinter.tix import Tree
from turtle import Screen
from venv import create
import pygame, sys, random
diem = 0

def create_ong(): # hàm tạo ống
    random_ong_pos = random.choice(ong_height) # rand chiều dài y
    bot_ong = ong.get_rect(midtop =  (350,random_ong_pos))
    top_ong = ong.get_rect(midtop =  (350,random_ong_pos-405))
    return bot_ong, top_ong
def draw_floor(): # tạo sàn chuyển động
    Screen.blit(floor,(floor_x_vitri,466))
    Screen.blit(floor,(floor_x_vitri+324,466))
def move_ong(ongs,): #di chuyển ống
    for ong in ongs:
        #print(ong.centerx)
        ong.centerx -= 2
        
    return ongs
def draw_ong(ongs): # hàm vẽ ống
    global diem
    d = 1
    for on in ongs:
        if on.bottom > 500:
            Screen.blit(ong,on)
        else:
            flip_ong = pygame.transform.flip(ong,False,True)
            Screen.blit(flip_ong,on)
            if 99 <= on.centerx <=100:    
                diem+=1                 
                tiengan.play()
def check_vacham(ongs): # kiểm tra va chạm
    for on in ongs:
        if bird_rect.colliderect(on):
            tienghit.play()
            time.sleep(0.5)
            tiengdie.play()

            #print('va cham')
            return False
            #pass
    # nếu chim đụng đầu hoặc rơi sàn
    if bird_rect.top <= -25 or bird_rect.bottom >=466:
        return False
    return True
def chim_cd(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_move*8,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird,new_bird_rect
def hienthi(kq):
    if kq:

        hienthidiem= game_font.render(f'SCORE: {int(diem)}',True,(255,255,255))
        diem_rect = hienthidiem.get_rect(center = (162,50))
        Screen.blit(hienthidiem,diem_rect)
    else:
        hienthidiem= game_font.render(f'SCORE: {int(diem)}',True,(255,255,255))
        diem_rect = hienthidiem.get_rect(center = (162,50))
        Screen.blit(hienthidiem,diem_rect)

        if diem <=3:
            hienthidiem= hienthi_font.render(f'You need to try harder',True,(255,255,255))
            diem_rect = hienthidiem.get_rect(center = (162,85))
            Screen.blit(hienthidiem,diem_rect)
        else:
            hienthidiem= hienthi_font.render(f'You are good',True,(255,255,255))
            diem_rect = hienthidiem.get_rect(center = (162,85))
            Screen.blit(hienthidiem,diem_rect)

        hienthidiemcao= game_font.render(f'HIGH SCORE: {int(diemcao)}',True,(255,255,255))
        diemcao_rect = hienthidiemcao.get_rect(center = (162,448))
        Screen.blit(hienthidiemcao,diemcao_rect)
def capnhat(diem,diemcao):
    if diem > diemcao:
        diemcao = diem
    return diemcao
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2,buffer=512)
pygame.init()

# fps  
clock = pygame.time.Clock()
# cài tiêu đề và icon
pygame.display.set_caption('Flappy Bird by Nguyen Hao')
gameIcon = pygame.image.load('assets/icon.jpg')
pygame.display.set_icon(gameIcon)

# biến xử thua
ketqua = True
#trọng lực
trongluc = 0.05
bird_move = 0

diemcao = 0
d =1 
# cài background
Screen = pygame.display.set_mode((324,576))

#background = pygame.image.load('assets/background-night.png')
background = pygame.transform.scale(pygame.image.load('assets/background-night.png').convert(),(324,576))

# chèn sàn
floor =pygame.image.load('assets/floor.png').convert()
floor_x_vitri =0 #vị trí x của sàn

# tạo font chữ
game_font =pygame.font.Font('04B_19.TTF',30)
hienthi_font =pygame.font.Font('04B_19.TTF',20)
# tạo chim
bird_mid =pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down =pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_up =pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_list=[bird_down, bird_mid,bird_up]
bird_index=0;
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,288))

# tạo timer cho chim đập cánh
dapcanh = pygame.USEREVENT+1
pygame.time.set_timer(dapcanh,200)
# tạo cột
#ong = pygame.image.load('assets/pipe-green.png').convert()
ong = pygame.transform.scale(pygame.image.load('assets/pipe-green.png').convert(),(45,300))
ong_list = []
ong_height = [300, 350, 275, 250, 225, 375, 325] # chiều cao ống
# tạo màn hình kết thúc
game_over = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over.get_rect(center = (162,288))

# tạo game over
gameover = pygame.image.load('assets/gameover.png').convert_alpha()
gameover_rect = gameover.get_rect(center = (162,136))

# tạo tiếng
tiengchim =pygame.mixer.Sound('sound/sfx_wing.wav')
tienghit =pygame.mixer.Sound('sound/sfx_hit.wav')
tiengan =pygame.mixer.Sound('sound/sfx_point.wav')
tiengdie =pygame.mixer.Sound('sound/sfx_die.wav')
# tạo timer
xuathien = pygame.USEREVENT
pygame.time.set_timer(xuathien,1000) # sau 1 giây thì xuất hiện 1 ống
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_SPACE and ketqua==True:
                #print('bay')
                
                bird_move=0
                bird_move = -2.2
                tiengchim.play()
                
            if event.key== pygame.K_SPACE and ketqua==False:
                d=1 
                ketqua =True
                ong_list.clear()

                #reset chim
                bird_rect.center =(100,288)
                bird_move =0
                # reset diem
                diem =0 
        if event.type == dapcanh:
            if bird_index<2:
                bird_index +=1
            else:
                bird_index=0

        #hàm tạo hiệu ứng đập cánh
        bird, bird_rect = bird_animation()
        # ống xuất hiện
        if event.type== xuathien:
            #print('tao ong')
            ong_list.extend(create_ong())
    Screen.blit(background,(0,0))
    if ketqua:

        #chim bay
        bird_move +=trongluc # chim càng di chuyển => trọng lực càng tăng
        
        bird_rect.centery += bird_move
        chimcd = chim_cd(bird)
        Screen.blit(chimcd,bird_rect)
        ketqua = check_vacham(ong_list )

        # ống
        ong_list = move_ong(ong_list)
        draw_ong(ong_list)
        #diem +=0.01
        hienthi(True)
    else:
        
        if d==1:
            tiengdie.play()
            d=0
        if diemcao == 0:
            bd= game_font.render(f'Code by Nguyen Hao',True,(255,255,255))
            bd_rect = bd.get_rect(center = (162,135))
            Screen.blit(bd,bd_rect)
        else:
            Screen.blit(gameover,gameover_rect)

        Screen.blit(game_over,game_over_rect)
        diemcao = capnhat(diem,diemcao)
        hienthi(False)
        #diem = 0
        

    # sàn
    floor_x_vitri -=1 
    draw_floor()
    if floor_x_vitri<=-324:
        floor_x_vitri=0
    pygame.display.update()
    #pygame.display.flip()

    clock.tick(120)

pygame.quit()