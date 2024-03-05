import pygame
import const

width = const.WIDTH
height = const.HEIGHT
pygame.init()
res = (width,height)
screen = pygame.display.set_mode(res)
starttext = pygame.font.SysFont('bradleyhanditc', 30)
text1 = starttext.render("Start", True, (255,255,255))
history_text = pygame.font.SysFont('bradleyhanditc', 30)
text2 = history_text.render("Game Play History", True, (255,255,255))
password = pygame.font.SysFont('bradleyhanditc', 30)
text3 = password.render("Renew password", True, (255,255,255))

while True:
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if 350 <= mouse[0] <= 450 and 200 <= mouse[1] <= 240:
                import main
            elif 275 <= mouse[0] <= 675 and 525 <= mouse[1] <= 590:
                import history #gameplay history
            elif 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 450:
                import update #renew password
    screen.fill((60,25,60))            
    mouse = pygame.mouse.get_pos()
    
    if 350 <= mouse[0]  <= 450 and 200 <= mouse[1] <= 240:
        pygame.draw.rect(screen,(170,170,170),[350,200,100,40])
    else:
        pygame.draw.rect(screen, (100,100,100), [350,200,100,40])
        
    if 275 <= mouse[0] <= 675 and 550 <= mouse[1] <= 590:
        pygame.draw.rect(screen,(170,170,170),[275,525,250,40])
    else:
        pygame.draw.rect(screen, (100,100,100), [275,525,250,40])
        
    if 300 <= mouse[0] <= 500 and 350 <= mouse[1] <= 450:
        pygame.draw.rect(screen,(170,170,170),[300,350,200,40])
    else:
       pygame.draw.rect(screen,(100,100,100),[300,350,200,40])
                
    screen.blit(text1, (370,210))
    screen.blit(text2,(275, 525))
    screen.blit(text3,(300, 350))
    pygame.display.update()
