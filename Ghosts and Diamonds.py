#chama a biblioteca pygame
import pygame
#inicializa os componentes da biblioteca pygame
pygame.init()

#tamanho da tela
win = pygame.display.set_mode((600,600))

#nome da tela
pygame.display.set_caption("Ghosts and Diamonds")

#vetores de sprites
walkRight = [pygame.image.load('img/R1.png'), pygame.image.load('img/R2.png'), pygame.image.load('img/R3.png'), pygame.image.load('img/R4.png')]
walkLeft = [pygame.image.load('img/L1.png'), pygame.image.load('img/L2.png'), pygame.image.load('img/L3.png'), pygame.image.load('img/L4.png')]
walkBottom = [pygame.image.load('img/F1.png'), pygame.image.load('img/F2.png'), pygame.image.load('img/F3.png'), pygame.image.load('img/F4.png')]
walkTop = [pygame.image.load('img/B1.png'), pygame.image.load('img/B2.png'), pygame.image.load('img/B3.png'), pygame.image.load('img/B4.png')]

#variaveis com as imagens guardadas
end = pygame.image.load('img/end.png')
begin = pygame.image.load('img/begin.png')
winner = pygame.image.load('img/win.png')
level1 = pygame.image.load('img/level1.png')
level2 = pygame.image.load('img/level2.png')
level3 = pygame.image.load('img/level3.png')
level4 = pygame.image.load('img/level4.png')
level5 = pygame.image.load('img/level5.png')
diamante = pygame.image.load('img/diamante.png')

#variavel para definir qual imagem será desenhada
stage = 0

#iniciar a musica do jogo
music = pygame.mixer.music.load('music/music.wav')
#a musica sempre repetirá com "-1"
pygame.mixer.music.play(-1)

#inicia o clock
clock = pygame.time.Clock()

#classe com as funções do diamante(item para passar de "level")
class item(object):
    #função para pegar a posição, tamanho e altura do diamante no loop principal
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    #função para desenhar o diamante + o hitbox(quado o personagem encostar nele)
    def draw(self, win):
        win.blit(diamante, (self.x,self.y))
        self.hitbox = (self.x + 14, self.y + 15, 38, 35)
   
#classe com as funções do jogador(o boneco que será movimentado)
class player(object):
    #função para pegar a posição, tamanho e altura do jogador no loop principal
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.left = False
        self.right = False
        self.bottom = True
        self.top = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    #função para desenhar o personagem e mudar sua imagem com o vetores de sprites
    def draw(self, win):
        #define a velocidade da troca de imagens, utilizando um contador "walk"(conforme caminha com o personagem)
        if self.walkCount + 1 >= 20:
            self.walkCount = 0

        """caso o personagem não esteja parado, ele entrará nessa condição para mudar sua imagem de acordo com o
        movimento(se for pra cima, utiliza os sprites "top", ou pra baixo "bottom", etc.)"""
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//5], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//5], (self.x,self.y))
                self.walkCount +=1
            elif self.bottom:
                win.blit(walkBottom[self.walkCount//5], (self.x,self.y))
                self.walkCount +=1
            else:
                win.blit(walkTop[self.walkCount//5], (self.x,self.y))
                self.walkCount +=1
        #se estiver parado, ira mostrar a primeira imagem do vetor sprite, dependendo do ultimo botão pressionado
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            elif self.bottom:
                win.blit(walkBottom[0], (self.x, self.y))
            else:
                win.blit(walkTop[0], (self.x, self.y))
        #hitbox do personagem
        self.hitbox = (self.x + 17, self.y + 8, 29, 49)
        
    
        
    #função para quando o personagem encosta em um inimigo ou no diamante(no último "level")       
    def hit(self):
        #sempre que o personagem encosta em um inimigo, o contador "stage" fica igual a "1", entrando nessa condição
        if stage == 1:
            #desenha a imagem "perdeu!!!"
            win.blit(end, (0,0))
            #começa a roda uma musica diferente
            music = pygame.mixer.music.load('music/lose.wav')
            #essa música toca apenas uma vez
            pygame.mixer.music.play(1)
            #atualiza a tela
            pygame.display.update()

            """esse while serve para parar o jogo por alguns segundos na tela "perdeu!!!", mas caso o usuario queira fechar o jogo
            é possível fazer isso normalmente"""
            i = 0
            while i < 200:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 201
                        pygame.quit()

        #caso o personagem tenha encostado no diamante, e for a última tela, entrará nessa condição    
        elif stage == 7:
            #desenha a tela "ganhou!!!"
            win.blit(winner, (0,0))
            #toca uma música diferente da principal
            music = pygame.mixer.music.load('music/winned.wav')
            #essa música toca apenas uma vez
            pygame.mixer.music.play(1)
            pygame.display.update()
            i = 0
            while i < 200:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 201
                        pygame.quit()

        #resetar o contador "walk"(que serve para mudar a imagem do personagem)
        self.walkCount = 0
        #reseta a posição do jogador para a posição original
        self.x = 280
        self.y = 435    
        pygame.display.update()      
        

        
        
class enemy(object):
    #vetor de sprites do inimigo
    walkRight = [pygame.image.load('img/ER1.png'), pygame.image.load('img/ER2.png'), pygame.image.load('img/ER3.png'), pygame.image.load('img/ER4.png')]
    walkLeft = [pygame.image.load('img/EL1.png'), pygame.image.load('img/EL2.png'), pygame.image.load('img/EL3.png'), pygame.image.load('img/EL4.png')]
    walkBottom = [pygame.image.load('img/EF1.png'), pygame.image.load('img/EF2.png'), pygame.image.load('img/EF3.png'), pygame.image.load('img/EF4.png')]
    walkTop = [pygame.image.load('img/EB1.png'), pygame.image.load('img/EB2.png'), pygame.image.load('img/EB3.png'), pygame.image.load('img/EB4.png')]

    """função para pegar a posição, tamanho e altura, velocidade, limite x1, x2, y1 e y2(de onde até aonde o inimigo caminhará)
    e os ultimos quatro são qual direção ele caminhará primeiro(se top for igual a true, ele vai caminhar pra cima primeiro, por exemplo)"""
    def __init__(self, x, y, width, height, vel, limx1, limx2, limy1, limy2, right, left, top, bottom):
        self.x = x
        self.limx1 = limx1
        self.limx2 = limx2
        self.y = y
        self.limy1 = limy1
        self.limy2 = limy2
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = vel
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
        self.hitbox = (self.x + 17, self.y + 7, 31, 47)

    #igual a função draw do jogador, onde desenha o inimigo e troca suas imagens com o vetor sprite
    def draw(self,win):
        #chama primeiro a função "move"(logo abaixo) para executar o caminho dos inimigos
        self.move()
        if self.walkCount + 1 >= 20:
            self.walkCount = 0

        if self.right == True:
            win.blit(self.walkRight[self.walkCount //5], (self.x, self.y))
            self.walkCount += 1
        elif self.left == True:
            win.blit(self.walkLeft[self.walkCount //5], (self.x, self.y))
            self.walkCount += 1

        elif self.top == True:
            win.blit(self.walkTop[self.walkCount //5], (self.x, self.y))
            self.walkCount += 1

        else:
            win.blit(self.walkBottom[self.walkCount //5], (self.x, self.y))
            self.walkCount += 1
        #hitbox dos inimigos
        self.hitbox = (self.x + 20, self.y + 10, 28, 43)
        

        
    #função para movimentar o personagem de acordo com a posição e os limites x, y escolhidos
    def move(self):
        """antes de iniciar os movimentos, existem condições para definir qual o tipo de movimento, que seria somente para o lado,
        somente para cima, ou em circulos, respectivamente"""
        if(self.limx1 != 0 and self.limy1 == 0):
            if self.right == True:
                self.x += self.vel

                if self.x >= self.limx1:
                    self.right = False
                    self.left = True
       
            elif self.left == True:
                self.x -= self.vel
                if self.x <= self.limx2:
                    self.left = False
                    self.right = True
        elif(self.limy1 != 0 and self.limx1 == 0):
            
            if self.bottom == True:
                self.y += self.vel
                if self.y >= self.limy1:
                    self.bottom = False
                    self.top = True
       
            elif self.top == True:
                self.y -= self.vel
                if self.y <= self.limy2:
                    self.top = False
                    self.bottom = True
                    
        elif(self.limx1 > 0 and self.limy1 > 0):
            if self.right == True:
                self.x += self.vel

                if self.x >= self.limx1:
                    self.right = False
                    self.top = True
   
            elif self.top == True:
                self.y -= self.vel
                if self.y <= self.limy2:
                    self.top = False
                    self.left = True

            elif self.left == True:
                self.x -= self.vel
                if self.x <= self.limx2:
                    self.left = False
                    self.bottom = True

            elif self.bottom == True:
                self.y += self.vel
                if self.y >= self.limy1:
                    self.bottom = False
                    self.right = True

            

#função para desenhar os niveis, jogador, diamante e fantasmas, dependendo do contador "stage"            
def redrawGameWindow():
    #tela inicial
    if stage == 0:   
        win.blit(begin, (0,0))
    #level 1   
    elif stage == 2:
        win.blit(level1, (0,0))
        aux2 = 0
        man.draw(win)
        E1.draw(win)
        E2.draw(win)
        E3.draw(win)
        E4.draw(win)
        E5.draw(win)
        E6.draw(win)
        E7.draw(win)
        IT.draw(win)
    #level 2
    elif stage == 3:
        win.blit(level2, (0,0))
        man.draw(win)
        E1.draw(win)
        E2.draw(win)
        E3.draw(win)
        E4.draw(win)
        E5.draw(win)
        E6.draw(win)
        IT.draw(win)
    #level 3
    elif stage == 4:
        win.blit(level3, (0,0))
        man.draw(win)
        E1.draw(win)
        E2.draw(win)
        E3.draw(win)
        E4.draw(win)
        E5.draw(win)
        E6.draw(win)
        E7.draw(win)
        IT.draw(win)
    #level 4
    elif stage == 5:
        win.blit(level4, (0,0))
        man.draw(win)
        E1.draw(win)
        E2.draw(win)
        E3.draw(win)
        E4.draw(win)
        E5.draw(win)
        E6.draw(win)
        IT.draw(win)
    #level 5
    elif stage == 6:
        win.blit(level5, (0,0))
        E1.draw(win)
        E2.draw(win)
        E3.draw(win)
        E4.draw(win)
        E5.draw(win)
        E6.draw(win)
        E7.draw(win)
        E8.draw(win)
        E9.draw(win)
        E10.draw(win)
        E11.draw(win)
        E12.draw(win)
        E13.draw(win)
        E14.draw(win)
        E15.draw(win)
        E16.draw(win)
        E17.draw(win)
        E18.draw(win)
        E19.draw(win)
        E20.draw(win)
        IT.draw(win)
        man.draw(win)

    pygame.display.update()

#inicia as variaveis, que serão modificadas no loop principal
man = player(280, 435, 64,64) 
E1 = enemy(0, 0, 64, 64, 3, 10, 10, 0, 0, False, False, False, False)
E2 = enemy(0, 0, 64, 64, 3, 10, 10, 0, 0, False, False, False, False)
E5 = enemy(0, 0, 64, 64, 3, 10, 10, 0, 0, False, False, False, False)
E3 = enemy(0, 0, 64, 64, 3, 10, 10, 0, 0, False, False, False, False)
E4 = enemy(0, 0, 64, 64, 3, 10, 10, 0, 0, False, False, False, False)
E6 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E7 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E8 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E9 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E10 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E11 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E12 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E13 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E14 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E15 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E16 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E17 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E18 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E19 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
E20 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
IT = item(280, 100, 64, 64)
aux = 0
#loop principal(onde roda o jogo)
run = True
while run:
    #serve para controlar os frame rates do jogo(frequência com que as imagens são executadas)
    clock.tick(30)

    """2 condições, a primeira serve para entrar em outras condições e mandar os dados para a função poder desenhar os personagens
    já a segunda condição reseta as posições do jogador e do diamante"""
    if stage >= 2 and stage <= 6:
        #a variavel auxiliar serve para entrar nas condições apenas uma vez, já que em qualquer condição ela passa a ter o valor 1
        if stage == 2 and aux == 0:
            man = player(280, 435, 64, 64) 
            E1 = enemy(300, 160, 64, 64, 6, 400, 150, 0, 0, True, False, False, False)
            E2 = enemy(300, 210, 64, 64, 6, 400, 150, 0, 0, False, True, False, False)
            E5 = enemy(150, 260, 64, 64, 7, 400, 150, 0, 0, True, False, False, False)
            E3 = enemy(300, 320, 64, 64, 6, 400, 150, 0, 0, False, True, False, False)
            E4 = enemy(300, 370, 64, 64, 6, 400, 150, 0, 0, False, True, False, False)
            E6 = enemy(95, 370, 64, 64, 6, 0, 0, 430, 105, False, False, True, False)
            E7 = enemy(445, 210, 64, 64, 6, 0, 0, 430, 105, False, False, False, True)
            E8 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E9 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E10 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E11 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E12 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E13 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E14 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E15 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E16 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E17 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E18 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E19 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E20 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            IT = item(275, 100, 64, 64)
            aux = 1
            
        elif stage == 3 and aux == 0:
            man = player(100, 100, 64, 64) 
            E1 = enemy(240, 155, 64, 64, 7, 240, 95, 210, 155, True, False, False, False)
            E2 = enemy(280, 210, 64, 64, 5, 0, 0, 430, 105, False, False, True, False)
            E3 = enemy(240, 310, 64, 64, 7, 240, 95, 435, 310, False, True, False, False)
            E4 = enemy(445, 105, 64, 64, 7, 445, 325, 210, 105, False, True, False, False)
            E5 = enemy(150, 260, 64, 64, 5, 445, 95, 0, 0, True, False, False, False)
            E6 = enemy(445, 310, 64, 64, 7, 445, 325, 390, 310, False, False, True, False)
            E7 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E8 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E9 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E10 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E11 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E12 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E13 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E14 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E15 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E16 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E17 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E18 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E19 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E20 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            IT = item(440, 440, 64, 64)
            aux = 1

        elif stage == 4 and aux == 0:
            man = player(100, 435, 64, 64) 
            E1 = enemy(400, 100, 64, 64, 5, 400, 95, 0, 0, False, True, False, False)
            E2 = enemy(445, 155, 64, 64, 7, 445, 95, 0, 0, False, True, False, False)
            E3 = enemy(445, 210, 64, 64, 5, 445, 95, 0, 0, False, True, False, False)
            E4 = enemy(445, 265, 64, 64, 7, 445, 95, 0, 0, False, True, False, False)
            E5 = enemy(445, 320, 64, 64, 5, 445, 95, 0, 0, False, True, False, False)
            E6 = enemy(445, 375, 64, 64, 7, 445, 95, 0, 0, False, True, False, False)
            E7 = enemy(445, 430, 64, 64, 5, 445, 95, 0, 0, False, True, False, False)
            E8 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E9 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E10 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E11 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E12 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E13 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E14 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E15 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E16 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E17 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E18 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E19 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E20 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            IT = item(440, 100, 64, 64)
            aux = 1

        elif stage == 5 and aux == 0:
            man = player(280, 100, 64, 64) 
            E1 = enemy(330, 220, 64, 64, 5, 330, 230, 320, 220, False, True, False, False)
            E2 = enemy(230, 320, 64, 64, 5, 330, 230, 320, 220, False, True, False, False)
            E3 = enemy(380, 170, 64, 64, 7, 380, 180, 370, 170, False, True, False, False)
            E4 = enemy(380, 370, 64, 64, 7, 380, 180, 370, 170, False, False, True, False)
            E5 = enemy(180, 370, 64, 64, 7, 380, 180, 370, 170, False, False, False, True)
            E6 = enemy(180, 170, 64, 64, 7, 380, 180, 370, 170, False, False, True, False)
            E7 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E8 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E9 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E10 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E11 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E12 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E13 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E14 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E15 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E16 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E17 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E18 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E19 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            E20 = enemy(0, 0, 64, 64, 4, 0, 0, 10, 10, False, False, False, False)
            IT = item(275, 270, 64, 64)
            aux = 1

        elif stage == 6 and aux == 0:
            man = player(280, 435, 64, 64) 
            E1 = enemy(400, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E2 = enemy(140, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E3 = enemy(400, 380, 64, 64, 2.5, 400, 140, 380, 170, False, False, True, False)
            E4 = enemy(140, 380, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E5 = enemy(350, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E6 = enemy(300, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E7 = enemy(250, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E8 = enemy(200, 170, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E9 = enemy(140, 230, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E10 = enemy(140, 280, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E11 = enemy(140, 330, 64, 64, 2.5, 400, 140, 380, 170, False, True, False, False)
            E12 = enemy(350, 380, 64, 64, 2.5, 400, 140, 380, 170, True, False, False, False)
            E13 = enemy(300, 380, 64, 64, 2.5, 400, 140, 380, 170, True, False, False, False)
            E14 = enemy(250, 380, 64, 64, 2.5, 400, 140, 380, 170, True, False, False, False)
            E15 = enemy(200, 380, 64, 64, 2.5, 400, 140, 380, 170, True, False, False, False)
            E16 = enemy(400, 320, 64, 64, 2.5, 400, 140, 380, 170, False, False, True, False)
            E17 = enemy(95, 370, 64, 64, 5, 0, 0, 430, 105, False, False, True, False)
            E18 = enemy(445, 210, 64, 64, 5, 0, 0, 430, 105, False, False, False, True)
            E19 = enemy(300, 325, 64, 64, 6, 350, 180, 0, 0, True, False, False, False)
            E20 = enemy(300, 220, 64, 64, 6, 350, 180, 0, 0, False, True, False, False)
            IT = item(275, 270, 64, 64)
            aux = 1
    else:
        man = player(600, 0, 64, 64) 
        IT = item(0, 600, 64, 64)

    """as 21 condições a seguir servem para ver se o hitbox do personagem encosta no hitbox do inimigo, o hitbox é como se fosse
    uma caixa invisível que, ao se chocarem através dessas condições, resetará o jogo para a primeira fase, com excessão da última
    que volta para a tela inicial"""
    if man.hitbox[1] < E1.hitbox[1] + E1.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E1.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E1.hitbox[0] and man.hitbox[0] < E1.hitbox[0] + E1.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E2.hitbox[1] + E2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E2.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E2.hitbox[0] and man.hitbox[0] < E2.hitbox[0] + E2.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E3.hitbox[1] + E3.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E3.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E3.hitbox[0] and man.hitbox[0] < E3.hitbox[0] + E3.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E4.hitbox[1] + E4.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E4.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E4.hitbox[0] and man.hitbox[0] < E4.hitbox[0] + E4.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E5.hitbox[1] + E5.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E5.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E5.hitbox[0] and man.hitbox[0] < E5.hitbox[0] + E5.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E6.hitbox[1] + E6.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E6.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E6.hitbox[0] and man.hitbox[0] < E6.hitbox[0] + E6.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E7.hitbox[1] + E7.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E7.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E7.hitbox[0] and man.hitbox[0] < E7.hitbox[0] + E7.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    if man.hitbox[1] < E8.hitbox[1] + E8.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E8.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E8.hitbox[0] and man.hitbox[0] < E8.hitbox[0] + E8.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E9.hitbox[1] + E9.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E9.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E9.hitbox[0] and man.hitbox[0] < E9.hitbox[0] + E9.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E10.hitbox[1] + E10.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E10.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E10.hitbox[0] and man.hitbox[0] < E10.hitbox[0] + E10.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E11.hitbox[1] + E11.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E11.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E11.hitbox[0] and man.hitbox[0] < E11.hitbox[0] + E11.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E12.hitbox[1] + E12.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E12.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E12.hitbox[0] and man.hitbox[0] < E12.hitbox[0] + E12.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E13.hitbox[1] + E13.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E13.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E13.hitbox[0] and man.hitbox[0] < E13.hitbox[0] + E13.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E14.hitbox[1] + E14.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E14.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E14.hitbox[0] and man.hitbox[0] < E7.hitbox[0] + E14.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E15.hitbox[1] + E15.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E15.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E15.hitbox[0] and man.hitbox[0] < E15.hitbox[0] + E15.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E16.hitbox[1] + E16.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E16.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E16.hitbox[0] and man.hitbox[0] < E16.hitbox[0] + E16.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E17.hitbox[1] + E17.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E17.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E17.hitbox[0] and man.hitbox[0] < E17.hitbox[0] + E17.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E18.hitbox[1] + E18.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E18.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E18.hitbox[0] and man.hitbox[0] < E18.hitbox[0] + E18.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E19.hitbox[1] + E19.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E19.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E19.hitbox[0] and man.hitbox[0] < E19.hitbox[0] + E19.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()

    if man.hitbox[1] < E20.hitbox[1] + E20.hitbox[3] and man.hitbox[1] + man.hitbox[3] > E20.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > E20.hitbox[0] and man.hitbox[0] < E7.hitbox[0] + E20.hitbox[2]:
            stage = 1
            aux = 0
            man.hit()
            
    #cada vez que entra na condição hitbox do diamante, o contador stage aumente de 1 em 1, para trocar de fase
    if man.hitbox[1] < IT.hitbox[1] + IT.hitbox[3] and man.hitbox[1] + man.hitbox[3] > IT.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > IT.hitbox[0] and man.hitbox[0] < IT.hitbox[0] + IT.hitbox[2]:
            stage = stage + 1
            aux = 0
            man.hit()

    #caso a pessoa queira sair do jogo, é só clicar no x vermelho da janela, sem essa condição não será sair normalmente do jogo 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    #pega a função key pressed do pygame(para verificar o botão pressionado)
    keys = pygame.key.get_pressed()

    #se o contador "stage" estiver dentro das condições(as fases jogáveis), será possível movimentar o personagem
    if stage >= 2 and stage <= 6:
        """nas condições abaixo, é estipulado um limite para o personagem, que seria a parte "jogável", assim o personagem não
        será capaz de ultrapassar esse limite, ou a própria tela do jogo. É aqui que é definido qual a posição que o personagem
        está andando, por exemplo, se apertar o botão esquerdo do teclado "<-" a variavel man.left passará a ser igual a "True"
        enquanto que as outras serão "False" para que utilize somente a parte esquerda dos vetores de sprite"""
        if keys[pygame.K_LEFT] and man.x - 90 > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.bottom = False
            man.top = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 510 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.bottom = False
            man.left = False
            man.top = False
            man.standing = False
        elif keys[pygame.K_DOWN] and man.y < 500 - man.height - man.vel:
            man.y += man.vel
            man.right = False
            man.bottom = True
            man.left = False
            man.top = False
            man.standing = False
        elif keys[pygame.K_UP] and man.y - 100 > man.vel:
            man.y -= man.vel
            man.right = False
            man.bottom = False
            man.top = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0

    #tanto na tela inicial(stage==0), "perdeu!!!"(stage==1) e "ganhou!!!"(stage==7), é preciso apertar o espaço para iniciar
    #o jogo ou trocar a tela"""
    #No caso da tela inicial e "perdeu!!!", o contador "stage" passa a ter o valor 2, redirecionando para a tela "level1"
    #E no caso da tela "perdeu!!!" e "ganhou!!!" a música principal volta a tocar normalmente depois de apertar espaço
    elif stage == 0:
        if keys[pygame.K_SPACE]:
            stage = 2
    elif stage == 1:
        if keys[pygame.K_SPACE]:
            stage = 2
            music = pygame.mixer.music.load('music/music.wav')
            pygame.mixer.music.play(-1)
    elif stage == 7:
        if keys[pygame.K_SPACE]:
            stage = 0
            music = pygame.mixer.music.load('music/music.wav')
            pygame.mixer.music.play(-1)
    #inicia a função principal do jogo, que desenha tudo o que é necessário          
    redrawGameWindow()
    
#fecha os componentes da biblioteca pygame
pygame.quit()


