import pygame;
import sys;

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
        if self.rect.bottom >= ALTO or self.rect.top <= 0:
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

#Inicializando la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO));
nombrePantalla = pygame.display.set_caption(NOMBRE_DEL_JUEGO);
pygame.key.set_repeat(30);

bolita = Bolita();
jugador = Jugador();
muro = Muro(50);

while True:
    #Establecer fps
    reloj.tick(60);

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit();
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento);

    #Actualizar posición de bolita
    bolita.update();


    pantalla.fill(color_pantalla);
    #Dibujar objetos en Pantalla
    pantalla.blit(bolita.image, bolita.rect);
    pantalla.blit(jugador.image, jugador.rect);
    #Dibujar Muro
    muro.draw(pantalla);
    #Actualiza objetos en Pantalla
    pygame.display.flip()

