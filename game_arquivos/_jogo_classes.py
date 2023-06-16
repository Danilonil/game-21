import pygame
from pygame.locals import *
from random import shuffle, randint
import sys
import os

# função para usar onefile do pyinstaller com img-audio-font 
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



largura_tela = 1080
altura_tela = 720
tempo = 0
vitorias = 0
record = 0
cond_vitoria = True
resultado = False
baralho = []

todas_sprites = pygame.sprite.Group()
mao_jogador = pygame.sprite.Group()
mao_robo = pygame.sprite.Group()
tela_placar = pygame.sprite.Group()

#-----------------------------------------------------------------------------

sprite_sheet_tela_escolha = pygame.image.load(resource_path('img/escolha333x250.png'))

class TelaEscolha(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_tela_escolha
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela/2, altura_tela/2)
        
tela_escolha = TelaEscolha()

#-----------------------------------------------------------------------------

sprite_sheet_caixa_texto = pygame.image.load(resource_path('img/caixatexto200x200.png'))

class CaixaTexto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_caixa_texto.subsurface((0*200, 0*200), (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (900, 170)
        
caixa_texto = CaixaTexto()

#-----------------------------------------------------------------------------

sprite_sheet_especial = pygame.image.load(resource_path('img/especial88x124.png'))

class Especial(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frente = sprite_sheet_especial.subsurface((x*88, y*124), (88, 124))
        self.verso = sprite_sheet_especial.subsurface((0*88, 0*124), (88, 124))
        self.valor = 0
        self.image = self.frente
        self.rect = self.image.get_rect()
        self.rect.center = (900, 300)


x = y = 0
for i in range(8):
    if x == 4:
        x = 0
        y += 1
    especial = Especial(x,y)
    #baralho.append(especial)
    x += 1
    
    #def dealer(self):
        
#-----------------------------------------------------------------------------

sprite_sheet_cartas = pygame.image.load(resource_path('img/cartas88x124.png'))

class Cartas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frente = sprite_sheet_cartas.subsurface((x*88, y*124), (88, 124))
        self.verso = sprite_sheet_cartas.subsurface((1*88, 13*124), (88, 124))
        self.valor = y+1
        if 9 < y < 13:
            self.valor = 10
        if y == 13:
            self.valor = 0

        self.image = self.frente
        self.rect = self.image.get_rect()
        self.rect.center = (900, 300)
        self.speed_x = self.speed_y = 0

carta_topo = Cartas(0, 13)

x = y = 0
for i in range(52):
    if x == 4:
        x = 0
        y += 1
    carta = Cartas(x,y)
    baralho.append(carta)
    x += 1


shuffle(baralho)

#-----------------------------------------------------------------------------

sprite_sheet_botao_compra = pygame.image.load(resource_path('img/baralho88x140.png'))

class BotaoCompra(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_botao_compra.subsurface((1*88, 0), (88, 140))
        self.rect = self.image.get_rect()
        self.rect.center = (900, 300)

    def animacao(self):
        # se o mouse colidir com sprite  do baralho    
        if botao_compra.rect.collidepoint(jogador.pos_mouse) and jogador.turno == True:
            # mouse transforma em mão
            cursor_mão = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor_mão)
            
            # aparece caixa de texto
            caixa_texto.image = sprite_sheet_caixa_texto.subsurface((0*200, 0*200), (200, 200))
            caixa_texto.rect.center = (900, 170)
            todas_sprites.add(caixa_texto)

            # carta do topo se movimenta
            carta_topo.image = carta_topo.verso
            carta_topo.rect.center = (self.rect.center[0] - carta_topo.speed_x, self.rect.center[1] + carta_topo.speed_y)
            todas_sprites.add(carta_topo)
            carta_topo.speed_x += 2
            carta_topo.speed_y += 5
            
            if carta_topo.speed_x > 10:
                carta_topo.speed_x = 10
            if carta_topo.speed_y > 20:
                carta_topo.speed_y = 20

        elif botao_compra.rect.collidepoint(jogador.pos_mouse) and jogador.turno == False:
            cursor_mão = pygame.SYSTEM_CURSOR_NO
            pygame.mouse.set_cursor(cursor_mão)

        else:
            pygame.mouse.set_cursor()
            pygame.sprite.Sprite.kill(caixa_texto)
            pygame.sprite.Sprite.kill(carta_topo)
            carta_topo.speed_x = carta_topo.speed_y = 0

botao_compra = BotaoCompra()
todas_sprites.add(botao_compra)

#-----------------------------------------------------------------------------

sprite_sheet_botao_parei = pygame.image.load(resource_path('img/Explosion384x384.png'))

class BotaoParei(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = sprite_sheet_botao_parei.subsurface((1*384, 0), (384, 384))
        self.rect = self.image.get_rect()
        self.rect.center = (125, 500)
        self.x = 6
        self.y = 0

    def update(self):        
        if jogador.apaga_pavil == True:
            self.image = sprite_sheet_botao_parei.subsurface((0*384, 0), (384, 384))
        else:   
            if 12 <= jogador.pontos < 14:
                self.image = sprite_sheet_botao_parei.subsurface((2*384, 0), (384, 384))
            
            if 14 <= jogador.pontos < 16:
                self.image = sprite_sheet_botao_parei.subsurface((3*384, 0), (384, 384))

            if 16 <= jogador.pontos < 18:
                self.image = sprite_sheet_botao_parei.subsurface((4*384, 0), (384, 384))

            if 18 <= jogador.pontos < 20:
                self.image = sprite_sheet_botao_parei.subsurface((5*384, 0), (384, 384))

            if 20 <= jogador.pontos <= 21:
                self.image = sprite_sheet_botao_parei.subsurface((6*384, 0), (384, 384))
            
            if jogador.pontos > 21:
                self.x += 0.5
                if self.x == 9:
                    self.x = 0
                    self.y = 1 
                self.image = sprite_sheet_botao_parei.subsurface((int(self.x) *384, self.y * 384), (384, 384))
                if self.x == 8 and self.y ==1:
                    self.image = sprite_sheet_botao_parei.subsurface((9*384, 1 * 384), (384, 384))
                    pygame.sprite.Sprite.kill(botao_parei)

    def animacao(self):
        # se o mouse colidir com sprite  do baralho    
        if botao_parei.rect.collidepoint(jogador.pos_mouse) and jogador.turno == True:
            # mouse transforma em mão
            cursor_mão = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor_mão)

            caixa_texto.image = sprite_sheet_caixa_texto.subsurface((1*200, 0*200), (200, 200))
            caixa_texto.rect.center = (self.rect.center[0], self.rect.center[1] + 150)
            todas_sprites.add(caixa_texto)

        elif botao_parei.rect.collidepoint(jogador.pos_mouse) and jogador.turno == False:
            cursor_mão = pygame.SYSTEM_CURSOR_NO
            pygame.mouse.set_cursor(cursor_mão)

botao_parei = BotaoParei()
todas_sprites.add(botao_parei)

#-----------------------------------------------------------------------------

class Jogador():
    def __init__(self) -> None:
        self.pontos = 0
        self.pos_carta = 0
        self.turno = True
        self.parou = False
        self.apaga_pavil = False
        self.ultimo = False
        self.especial = 0

    def update(self):
        self.pos_mouse = pygame.mouse.get_pos() 

    def para(self):
        if botao_parei.rect.collidepoint(jogador.pos_mouse) and self.turno == True or self.pontos >= 22:
            if self.pontos <= 21:
                self.apaga_pavil = True
            self.parou = True
            self.turno = False

    def comprar(self):
        if botao_compra.rect.collidepoint(self.pos_mouse) and self.turno == True or len(mao_jogador) < 2 and self.turno == True:
            carta = baralho[-1]        
            carta.image = carta.frente
            carta.image = pygame.transform.scale(carta.image, (88 * 1.8, 124 * 1.8))
            self.pontos += carta.valor
            mao_jogador.add(carta)
            baralho.remove(carta)
            if type(carta) == type(especial):
                self.especial += 1
                if self.especial <= 1:
                    carta.rect.center = (868, 500)
                
                else:
                    todas_sprites.add(tela_escolha)
                    x = 0
                    for carta in mao_jogador:
                        if type(carta) == type(especial): 
                            carta.rect.center = (largura_tela/2 - 135 + x , 350)
                            x += 200
            else:
                carta.rect.center = (300 + self.pos_carta, 500)
                self.pos_carta += 50

            self.turno = False
    
    def escolha_especial(self):
        pass

jogador = Jogador()

#-----------------------------------------------------------------------------

cartas_boas = []

class Robo():
    def __init__(self):
        self.pontos = 0
        self.pos_carta = 0
        self.parou = False
        self.tempo = 0
        self.duracao_fala = 1

    def conta_cartas(self):
        if self.parou == False:
            for carta in baralho:
                if carta.valor <= (21 - self.pontos):
                    cartas_boas.append(carta.valor)

            self.porc_acerto = int((len(cartas_boas)/ len(baralho)) *100)
        cartas_boas.clear()

    def fala(self):
        self.tempo += 1
        if self.tempo == 14:
            if self.parou == False: 
                if len(mao_robo) > 1:
                    n = randint(1, 3)
                    fala = pygame.mixer.Sound(resource_path(f'audio/fala_{str(n)}.mp3'))
                    fala.play()
                    self.duracao_fala = int((pygame.mixer.Sound.get_length(fala))) + 0.2

            elif self.parou == True:
                fala = pygame.mixer.Sound(resource_path('audio/parei.mp3'))
                fala.play()

    def comprar(self): 
        if len(mao_robo) < 1:
            self.duracao_fala = 0.5

        if self.tempo == self.duracao_fala * 30:
            if self.parou == False: 
                carta = baralho[-1]        
                carta.image = carta.verso
                carta.rect.center = (700 - self.pos_carta, 100)
                self.pos_carta += 90
                self.pontos += carta.valor
                mao_robo.add(carta)
                baralho.remove(carta)

            if jogador.parou == False:
                jogador.turno = True

            self.tempo = 0

    def para(self):
        self.parou = True
        if jogador.parou == False:
            jogador.ultimo = True
            jogador.turno = True

robo = Robo()

#-----------------------------------------------------------------------------

sprite_sheet_acento = pygame.image.load(resource_path('img/acento.png'))

class Acento(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_acento 
        self.image = pygame.transform.scale(self.image, (23 * 0.5, 23 * 0.5))
        self.rect = self.image.get_rect()
        self.rect.center = (415, 20)

acento = Acento()
tela_placar.add(acento)

#-----------------------------------------------------------------------------

sprite_sheet_placar = pygame.image.load(resource_path('img/win_lose213x222.png'))

class PlacarFinal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0
        self.image = sprite_sheet_placar.subsurface((self.x *213, self.y *222), (213, 222))
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela/2, altura_tela/2 -100)        

    def update(self):
        if robo.pontos < jogador.pontos < 22 or robo.pontos > 21 and jogador.pontos < 22:
            self.x += 0.1
            self.y = 0
            self.image = sprite_sheet_placar.subsurface((int(self.x) *213, self.y *222), (213, 222))
            if self.x > 1.9:
                self.x = 0

        elif jogador.pontos < robo.pontos < 22 or jogador.pontos > 21 and robo.pontos < 22:
            self.x += 0.1
            self.y = 1
            self.image = sprite_sheet_placar.subsurface((int(self.x) *213, self.y *222), (213, 222))
            if self.x > 1.9:
                self.x = 0   

        else:
            self.x += 0.1
            self.y = 2
            self.image = sprite_sheet_placar.subsurface((int(self.x) *213, self.y *222), (213, 222))
            if self.x > 1.9:
                self.x = 0

placar = PlacarFinal()
tela_placar.add(placar)

#-----------------------------------------------------------------------------

sprite_sheet_play = pygame.image.load(resource_path('img/play195x80.png'))

class Play(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_play
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela/2, altura_tela - placar.rect.bottom + 60)
        self.reiniciar = False

    def animacao(self):  
        if self.rect.collidepoint(jogador.pos_mouse):
            self.image = pygame.transform.scale(self.image, (195 * 1.05, 80 * 1.05))
            cursor_mão = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor_mão)
        
        else:
            self.image = sprite_sheet_play
            pygame.mouse.set_cursor()
    
    def botao_reiniciar(self):
        if self.rect.collidepoint(jogador.pos_mouse):
            for carta in mao_jogador:
                baralho.append(carta)
            for carta in mao_robo:
                baralho.append(carta)
            pygame.sprite.Group.empty(mao_jogador)
            pygame.sprite.Group.empty(mao_robo)
            shuffle(baralho)
            jogador.parou = robo.parou = False
            jogador.pontos = robo.pontos = 0
            jogador.pos_carta = robo.pos_carta = 0
            jogador.turno = True
            jogador.apaga_pavil = False
            jogador.ultimo = False
            robo.tempo = 0
            botao_parei.image = sprite_sheet_botao_parei.subsurface((1*384, 0), (384, 384))
            todas_sprites.add(botao_parei)
            
            self.reiniciar = True

play = Play()
tela_placar.add(play)

