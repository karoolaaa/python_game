#importowanie odpowiednich bibliotek
import pygame
from pygame.locals import *

pygame.init()

#wymiary okna
screen_width = 500
screen_height = 500

#ustawienie czcionki
font = pygame.font.SysFont('Constantia', 20)

# obiekt kontrolujący czas
clock = pygame.time.Clock()

#stworzenie okna
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Moja gra')




tile_size = 50

#podanie ścieżek do plików
path_bg = 'pustynia.jpg'
path_player = 'dinozaur1.png'
path_wyniki = "results.txt"
path_FO = "ptaszek1.png"
path_sound = "sound.mp3"

sound_hit = pygame.mixer.Sound(path_sound)
#załadowanie tła  
bg_img = pygame.image.load(path_bg)

#definicja  kolorów
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

#definicja globalnych zmiennych
clicked = False
counter = 0


class button():    #klasa button odpowiedzialna za przyciski
    
    width = 150       #definicja szerekości i wysokości buttona
    height = 50

    def __init__(self, x, y, text):    #inicjator klasy button
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):   #rysuje button (w odpowiednich kolorach) i przycisk, zwraca True jeśli button został naciśnięty

        global clicked
        action = False

        #pozycja myszki
        pos = pygame.mouse.get_pos()

        #utworzenie obiektu Rect
        button_rect = Rect(self.x, self.y, self.width, self.height)

        #sprawdzanie czy myszka jest nad buttonem
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                clicked = True
                pygame.draw.rect(screen, white, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0:
                clicked = False
                action = False
                pygame.draw.rect(screen, red, button_rect)
        else:
            pygame.draw.rect(screen, white, button_rect)

        #dodwanie napisu do przycisku
        text_img = font.render(self.text, True, black)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 10))
        return action


class FlyingObject():        #tworzę klasę FlyingObject odpowiedzialną za przeszkody
    
    
    def __init__(self):                     #inicjator klasy FlyingObject
        img = pygame.image.load(path_FO)
        self.image = pygame.transform.scale(img, (30, 60))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width      #definiuje jego pozycje po prawej stronie okna
        self.rect.y = screen_height - 70
        self.wynik = 0
        

    def update(self):    
        self.rect.x -= 5    #za każdym wywołaniem przesuwa o 5 w lewo
        if self.rect.x <= 0:  
            self.rect.x = screen_width #cofnięcie do prawej strony
            self.wynik += 1  #dodanie punktu do wyniku
        screen.blit(self.image, self.rect)
    
    
    
class Player():    
    def __init__(self, x, y):
        img = pygame.image.load(path_player)
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.hp = 3     #ilość żyć
    def hit(self):
        self.hp -= 1
        sound_hit.play()
    def update(self):
        dx = 0
        dy = 0

        #zdefiniowanie działania w przypadku kliknięcia strzałek i spacji
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -30
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5


        #dodanie grawitacji
        self.vel_y += 2
        if self.vel_y > 20:
            self.vel_y = 20
        dy += self.vel_y


        
        self.rect.x += dx
        self.rect.y += dy
       
        if self.rect.bottom > screen_height:    #uniemożliwia wypadnięcie obiektu poza ekran na dole
            self.rect.bottom = screen_height
            dy = 0

        #namalowanie player'a na ekranie
        screen.blit(self.image, self.rect)





start_gry = button(screen_width/2-100, 30, 'Start gry')
wyjscie = button(screen_width/2-100, 130, 'Wyjście')
autor = button(screen_width/2-100, 230 , 'O autorze')
wyniki = button(screen_width/2-100, 330, 'Najlepsze wyniki')
zasady = button(screen_width/2-100, 430, 'Zasady gry')

player = Player(100, screen_height - 100)
FO = FlyingObject()



fopen = open(path_wyniki,"r")
bestr = int(fopen.read())
fopen.close()



delay = 0
gramy = False
run = True
while run:
    
    delay = 0
    if not gramy:
        screen.fill(bg)  #wypełnienie okna kolorem beżowym
    
        if start_gry.draw_button(): 
            gramy = True
            FO.wynik = 0
            counter = 0
        if wyjscie.draw_button():
             run = False
        if autor.draw_button():
            delay = 1
            autor_img = font.render("Karolina, Wrocław", True, red)
            screen.blit(autor_img, (screen_width/2+50, 50))
            counter += 1
        if zasady.draw_button():
            delay = 1
            zasady_img = font.render("Zasady w README", True, red)
            screen.blit(zasady_img, (screen_width/2+50, 50))
            counter += 1
        if wyniki.draw_button():
            delay = 1
            zasady_img = font.render("Najlepsze wyniki = " + str(bestr), True, red)
            screen.blit(zasady_img, (screen_width/2 + 50, 50))
            counter += 1

    if gramy:
        
                
        img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        screen.blit(img, (0, 0))
        player.update()
        FO.update()
        
        zycie_img = font.render("Ilość żyć = " + str(player.hp), True, red)
        screen.blit(zycie_img, (screen_width/2 - 50, 2))
        
        #analiza czy dwa obiekty nachodzą na siebie
        # jeżeli współrzędne x się nie pokrywają to obiekty na siebie nie zachodzą
        #jeżeli x się pokrywają to sprawdzamy czy współrzędne y się pokrywają
        if (not ((FO.rect.x > player.rect.x + player.rect.width) or (FO.rect.x + FO.rect.width< player.rect.x)) ) and ( player.rect.y + player.rect.height > FO.rect.y  ):
            player.hit()
            FO.rect.x = screen_width     #ustawia obiekt FO spowrotem po prawej stronie
        
        if player.hp == 0:   
            gramy = False  
            gameo_img = font.render("Game Over", True, red)
            screen.blit(gameo_img, (screen_width/2 - 50, 30))
            delay = 2
                                    
            player.hp = 3
            if FO.wynik > bestr:  #zapisanie najlepszego wyniku
                bestr = FO.wynik
                fopen = open(path_wyniki,"w")
                fopen.write(str(FO.wynik))
                fopen.close()
       
        wynik_img = font.render("wynik = " + str(FO.wynik), True, red)
        screen.blit(wynik_img, (screen_width/2 + 80, 2))       
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(60)        #opóźnienie działania pętli while
    
    pygame.display.update()
    pygame.time.delay(delay*1000)
pygame.quit()