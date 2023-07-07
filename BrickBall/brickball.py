import pygame;
import time; #Para usar sleep
import sys;  #Para usar funciones del sistema

#tamano de pantalla
ANCHO = 640;
ALTO = 480;
NOMBRE_DEL_JUEGO = "BrickBall";
VEL_X = 3;
VEL_Y = 3;

#Reloj de fps
reloj = pygame.time.Clock();

#Desaparecer bolitas anteriores cambiando fondo de pantalla
color_pantalla = (0,0,64); #Color Azul
color_blanco = (255,255,255); #Color blanco para textos

#Para poder usar fuentes dentro del videojuego
pygame.init();

#Bolita del Juego
class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self);
        #Cargar Imagen
        self.image = pygame.image.load("sprites/bolita.png");
        self.rect = self.image.get_rect();
        #Posicion Inicial
        self.rect.centerx = ANCHO/2;
        self.rect.centery = ALTO/2;
        #Establecer velocidad inicial
        self.speed = [VEL_X,VEL_Y];
    pass;

    def update(self):
        #Evitar que se salga en Y
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1];
        #Evitar que se salga en X
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0];
        #Mover en base a posicion X,Y
        self.rect.move_ip(self.speed);

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__;
        #Cargar imagen
        self.image = pygame.image.load("sprites/paleta.png");
        self.rect = self.image.get_rect();
        #Posición Inicial
        self.rect.midbottom = [ANCHO/2,ALTO-20];
        #Establecer velocidad
        self.speed = [0,0];
    pass;

    def update(self,evento):
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed[0] = -5;
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed[0] = 5;
        else:
            self.speed[0] = 0;
        pass;
        self.rect.move_ip(self.speed);

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,posicion):
        pygame.sprite.Sprite.__init__(self);
        #Cargar imagen
        self.image = pygame.image.load("sprites/ladrillo.png");
        self.rect = self.image.get_rect();
        #Posicion Inicial
        self.rect.topleft = posicion;
        #Establecer velocidad 
        self.speed = [0,0];
    pass;

class Muro(pygame.sprite.Group):
    def __init__(self,cantidadLadrillos):
        pygame.sprite.Group.__init__(self);
        posX = 0;
        posY = 20;
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((posX, posY));
            self.add(ladrillo);
            posX = posX + ladrillo.rect.width;
            if posX >= ANCHO:
                posX = 0;
                posY += ladrillo.rect.height;
            pass;
        pass;

    pass;

#Funcion para Game Over
def juego_terminado():
    fuente = pygame.font.SysFont('Arial',72);
    texto = fuente.render("GAME OVER", True, color_blanco);
    texto_rect = texto.get_rect();
    texto_rect.center = [ANCHO/2, ALTO/2];
    pantalla.blit(texto,texto_rect);
    pygame.display.flip();
    #Pausar
    time.sleep(3);
    #Salir
    sys.exit();
    
#Funcion para Mostrar Puntuacion
def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas',20);
    cadena = "Score: " + str(puntuacion).zfill(5);
    texto = fuente.render(cadena, True, color_blanco);
    texto_rect = texto.get_rect();
    texto_rect.topleft = [0,0];
    pantalla.blit(texto,texto_rect);
    pass;

#Funcion para Mostrar Vidas
def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas',20);
    cadena = "Vidas: " + str(vidas).zfill(2);
    texto = fuente.render(cadena, True, color_blanco);
    texto_rect = texto.get_rect();
    texto_rect.topright = [ANCHO,0];
    pantalla.blit(texto,texto_rect);
    pass;

#Inicializando la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO));
nombrePantalla = pygame.display.set_caption(NOMBRE_DEL_JUEGO);
pygame.key.set_repeat(30);

bolita = Bolita();
jugador = Jugador();
muro = Muro(50);
puntuacion = 0;
vidas = 3;
esperando_saque = True;
brick_crash_sound = pygame.mixer.Sound("sounds/pop1.ogg");

#Agregando musica de fondo
pygame.mixer.music.load("music/8bit Dungeon Boss.mp3")
pygame.mixer.music.play(-1)

while True:
    #Establecer fps
    reloj.tick(60);

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit();
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento);
            if evento.key == pygame.K_SPACE and esperando_saque == True:
                esperando_saque = False;
                if bolita.rect.centerx < ANCHO/2:
                    bolita.speed = [VEL_X,-VEL_Y];
                else:
                    bolita.speed = [-VEL_X, -VEL_Y];
                
                pass;

    #Actualizar posición de bolita
    if esperando_saque:
        bolita.rect.midbottom = jugador.rect.midtop;
    else:
        bolita.update();

    #Colision de bolita con el Jujador
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]; 
        pass;
    
    #Colision de la bolita con los muros
    if pygame.sprite.spritecollide(bolita,muro,True):
        pygame.mixer.Sound.play(brick_crash_sound);
        bolita.speed[1] = -bolita.speed[1];
        puntuacion += 10;
        pass;
    
    #Checar Game Over
    if bolita.rect.top >= ALTO:
        vidas -= 1;
        if vidas <= 0:
            pantalla.fill(color_pantalla);
            mostrar_puntuacion();
            mostrar_vidas();
            juego_terminado();
            pass;
        esperando_saque = True;
        pass;

    pantalla.fill(color_pantalla);
    #Mostrar Score
    mostrar_puntuacion();
    # Mostrar Vidas
    mostrar_vidas();
    #Dibujar objetos en Pantalla
    pantalla.blit(bolita.image, bolita.rect);
    pantalla.blit(jugador.image, jugador.rect);
    #Dibujar Muro
    muro.draw(pantalla);
    #Actualiza objetos en Pantalla
    pygame.display.flip()

