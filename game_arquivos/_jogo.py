from _jogo_classes import *
from sys import exit

with open(resource_path('r.txt'), 'r') as arquivo:
    record = arquivo.read()

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init() #iniciar funções do pygame

pygame.display.set_caption('21.IO  --  versão 1.0') #definir nome da aba

tela = pygame.display.set_mode((largura_tela, altura_tela)) #definir tamanho da tela
relogio = pygame.time.Clock() #definir relogio
font_p = pygame.font.Font(resource_path("font/04B_30__.TTF"),18)
font_m = pygame.font.Font(resource_path("font/04B_30__.TTF"),30)
font_g = pygame.font.Font(resource_path("font/04B_30__.TTF"),70)

while True:
    
    tela.fill((0, 80, 0)) #cor da tela
    if resultado == False: #partida
        jogador.update()
        robo.conta_cartas()

        if jogador.especial < 2:
            botao_compra.animacao()
            botao_parei.animacao()      
        else:
            escolha = font_m.render('ESCOLHA UMA:', True, (0,0,0))
            tela_escolha.image.blit(escolha, (145, 80), )
            pygame.sprite.Sprite.kill(caixa_texto)
            pygame.sprite.Sprite.kill(carta_topo)
            carta_topo.speed_x = carta_topo.speed_y = 0      

        for evento in pygame.event.get(): #definir eventos  

            if evento.type == QUIT: #evento de fechar a janela
                pygame.quit()
                exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogador.especial < 2:
                    jogador.comprar()
                    jogador.para()
                else:
                    jogador.escolha_especial()
            
        #logica
        #inicio de jogo
        if len(mao_jogador) < 2:
            tempo += 1
            if len(mao_jogador) == 0:
                if tempo == 15:
                    jogador.comprar()
                    tempo = 0
            elif tempo == 30:
                jogador.comprar()
                tempo = 0

        if jogador.turno == False:
            if robo.pontos >= 21:
                robo.para()
            
            else:
                if robo.porc_acerto >= 52:
                    robo.fala()
                    robo.comprar()

                else:
                    if 44 <= robo.porc_acerto < 52:
                        probab = randint(1, 108)
                        if probab >= 15:
                            robo.fala()
                            robo.comprar()
                        else:
                            robo.para()                        
                    
                    elif 37 <= robo.porc_acerto < 44:
                        probab = randint(1, 108)
                        if probab >= 44:
                            robo.fala()
                            robo.comprar()
                        else:
                            robo.para()                        

                    elif 29 <= robo.porc_acerto < 37:
                        probab = randint(1, 108)
                        if probab >= 75:
                            robo.fala()
                            robo.comprar()
                        else:
                            robo.para()

                    elif 22 <= robo.porc_acerto < 29:
                        probab = randint(1, 108)
                        if probab >= 90:
                            robo.fala()
                            robo.comprar()
                        else:
                            robo.para()                        

                    elif 14 <= robo.porc_acerto < 22:
                        probab = randint(1, 108)
                        if probab >= 100:
                            robo.fala()
                            robo.comprar()
                        else:
                            robo.para()                        

                    else:
                        robo.para()

        if robo.parou == True:
            robo.fala()

        # cor dos pontos
        score = font_g.render(f'{int(jogador.pontos)} ', True, (0,0,0))
        if jogador.pontos >= 22:
            score = font_g.render(f'{int(jogador.pontos)} ', True, (100,0,0))

        #mostras as sprites na tela
        mao_robo.draw(tela)
        todas_sprites.draw(tela)
        mao_jogador.draw(tela)
        todas_sprites.update()
        mao_robo.update()
        mao_jogador.update() #atualiza as sprites
        tela_placar.update()

        #alinhando pontos
        if jogador.pontos <10:
            tela.blit(score, (botao_parei.rect.center[0] -25 , botao_parei.rect.center[1] + 30))
        elif 10 <= jogador.pontos < 20:  
            tela.blit(score, (botao_parei.rect.center[0] -50 , botao_parei.rect.center[1] + 30))
        elif jogador.pontos == 21:
            tela.blit(score, (botao_parei.rect.center[0] -53 , botao_parei.rect.center[1] + 30))
        else:
            tela.blit(score, (botao_parei.rect.center[0] -60 , botao_parei.rect.center[1] + 30))
        
        if jogador.parou == True and robo.parou == True:
            tempo += 1
            if jogador.ultimo == True and jogador.pontos < 22:
                tempo = 30
                jogador.ultimo = False

            if tempo == 35:
                resultado = True
                tempo = 0

    elif resultado == True: #resultado da partida

        jogador.update()
        play.animacao()

        pygame.draw.line((tela), (90, 90, 90), (largura_tela/2, 50), (largura_tela/2, 650) )
        
        for evento in pygame.event.get(): #definir eventos  

            if evento.type == QUIT: #evento de fechar a janela
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN: #iniciar novo jogo
                play.botao_reiniciar()
                if play.reiniciar == True:
                    play.reiniciar = False
                    tempo = 0
                    cond_vitoria = True
                    resultado = False
        
        jogador.pos_carta = 0
        robo.pos_carta = 0
        y = 200
        for carta in mao_jogador:
            carta.image = carta.frente
            carta.rect.center = (150 + jogador.pos_carta, y)
            jogador.pos_carta += 50
            if jogador.pos_carta == 250:
                y += 120
                jogador.pos_carta = 0

        y = 200
        for carta in mao_robo:
            carta.image = carta.frente
            carta.rect.center = ((largura_tela - 150) - robo.pos_carta, y)
            robo.pos_carta += 50
            if robo.pos_carta == 250:
                y += 120
                robo.pos_carta = 0

        vitorias_consec = font_p.render(f' VITORIAS CONSECUTIVAS: {int(vitorias)} ', True, (0,0,0))
        tela.blit(vitorias_consec, (340, 30), )

        meu_score = font_m.render(f' JOGADOR: {int(jogador.pontos)} ', True, (0,0,0))
        tela.blit(meu_score, (100, 600), )

        score_robo = font_m.render(f' ROBO: {int(robo.pontos)} ', True, (0,0,0))
        tela.blit(score_robo, (680, 600), )

        if robo.pontos < jogador.pontos < 22 or robo.pontos > 21 and jogador.pontos < 22:
            if cond_vitoria == True:
                vitorias += 1
                cond_vitoria = False

        elif jogador.pontos < robo.pontos < 22 or jogador.pontos > 21 and robo.pontos < 22:
            vitorias = 0

        txt_record = font_m.render(f' RECORD: {record} ', True, (0,0,50))
        if vitorias > int(record):
            record = vitorias
            with open(resource_path('r.txt'), 'w') as arquivo:
                arquivo.write(str(record))
                
        tela.blit(txt_record, (largura_tela/2 - 138, altura_tela/2 - 250))

        mao_robo.draw(tela)
        mao_jogador.draw(tela)
        tela_placar.draw(tela)
        tela_placar.update()

    pygame.display.flip() #atualizar a tela
    relogio.tick(30) #relogio em frames por segundo





