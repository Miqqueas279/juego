import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 1500, 1000
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("El Juego de la Bola que Escala")

ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)
GRIS = (100, 100, 100)
AZUL = (0, 0, 255)

TIEMPO_LIMITE = 60
tiempo_restante = TIEMPO_LIMITE
reloj = pygame.time.Clock()
puntuacion = 0
juego_activo = False
pausado = False
menu_activo = True
mostrar_mensaje_perdiste = False
tiempo_mensaje = 0
tiempo_mostrar_mensaje = 3000  

ultimo_tiempo = pygame.time.get_ticks()

radio_pelota = 20
vel_x, vel_y = 0, 0
gravedad = 0.5
salto = -18
coyote_time = 0.2
coyote_timer = 0

plataformas = []
altura_inicial = ALTO - 50

fondo = pygame.image.load("C:/Users/PC/Desktop/facultad/juego facu/cielo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

salto_sonido = pygame.mixer.Sound("C:/Users/PC/Desktop/facultad/juego facu/cartoon-jump-6462.mp3")

sonido_perder = pygame.mixer.Sound("C:/Users/PC/Desktop/facultad/juego facu/perder.mp3")  

sonido_moneda = pygame.mixer.Sound("C:/Users/PC/Desktop/facultad/juego facu/monedas recoger.mp3")  

def generar_plataformas():
    plataformas.clear()
    for i in range(10000):
        x = random.randint(100, ANCHO - 200)
        y = altura_inicial - i * 100
        plataformas.append(pygame.Rect(x, y, random.randint(150, 250), 10))

generar_plataformas()

primera_plataforma = plataformas[0]
x_pelota = primera_plataforma.x + primera_plataforma.width // 2
y_pelota = primera_plataforma.y - radio_pelota

def generar_monedas():
    monedas = []
    for i, plataforma in enumerate(plataformas):
        if i % 3 == 0:
            x_moneda = random.randint(plataforma.x + 10, plataforma.x + plataforma.width - 10)
            y_moneda = plataforma.y - 30
            monedas.append(pygame.Rect(x_moneda, y_moneda, 20, 20))
    return monedas

monedas = generar_monedas()

camara_y = 0

fuente = pygame.font.SysFont("Arial", 24)
fuente_titulo = pygame.font.SysFont("Arial", 60)

def mostrar_texto(texto, x, y, fuente, color=BLANCO):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

def dibujar_boton(texto, x, y, ancho, alto, color_base, color_hover, accion=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto))
        if click[0] == 1 and accion is not None:
            accion()
    else:
        pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto))

    texto_boton = fuente.render(texto, True, BLANCO)
    pantalla.blit(texto_boton, (x + 10, y + 10))

def salir_juego():
    pygame.quit()
    sys.exit()

def iniciar_juego():
    global juego_activo, puntuacion, tiempo_restante, plataformas, monedas, camara_y, menu_activo, ultimo_tiempo, x_pelota, y_pelota
    juego_activo = True
    menu_activo = False
    puntuacion = 0
    tiempo_restante = TIEMPO_LIMITE
    generar_plataformas()
    monedas = generar_monedas()
    camara_y = 0
    ultimo_tiempo = pygame.time.get_ticks()
    
    primera_plataforma = plataformas[0]
    x_pelota = primera_plataforma.x + primera_plataforma.width // 2
    y_pelota = primera_plataforma.y - radio_pelota

def mostrar_menu_inicio():
    pantalla.fill(NEGRO)
    
    mostrar_texto("El Juego de la Bola que Escala", ANCHO // 4, ALTO // 4, fuente_titulo, ROJO)
    
    mostrar_texto("Instrucciones:", ANCHO // 3, ALTO // 2 - 50, fuente, ROJO)
    mostrar_texto("1. Usa las teclas de las flechas izquierda y derecha para moverte.", ANCHO // 3, ALTO // 2, fuente, ROJO)
    mostrar_texto("2. Presiona espacio para saltar.", ANCHO // 3, ALTO // 2 + 30, fuente, ROJO)
    mostrar_texto("3. Colecciona monedas para ganar puntos.", ANCHO // 3, ALTO // 2 + 60, fuente, ROJO)
    mostrar_texto("4. Evita caer al vacío y que se acabe el tiempo", ANCHO // 3, ALTO // 2 + 90, fuente, ROJO)
    
    dibujar_boton("Jugar", ANCHO // 3, ALTO // 2 + 140, 200, 50, GRIS, ROJO, iniciar_juego)
    dibujar_boton("Salir", ANCHO // 3, ALTO // 2 + 200, 200, 50, GRIS, ROJO, salir_juego)

    pygame.display.flip()

def mostrar_mensaje_perdida():
    global puntuacion  

    sonido_perder.play()

    pantalla.fill(NEGRO)
    
    mostrar_texto("¡PERDISTE!", ANCHO // 3, ALTO // 3, fuente_titulo, ROJO)
    
    mostrar_texto("Has perdido, vuelve a intentarlo.", ANCHO // 3, ALTO // 3 + 70, fuente, ROJO)
    mostrar_texto(f"Puntaje final: {puntuacion}", ANCHO // 3, ALTO // 3 + 110, fuente, ROJO)

    dibujar_boton("Volver al Menú", ANCHO // 3, ALTO // 2 + 200, 200, 50, GRIS, ROJO, reiniciar_juego)

    pygame.display.flip()

def reiniciar_juego():
    global menu_activo, juego_activo, puntuacion, tiempo_restante
    menu_activo = True
    juego_activo = False
    puntuacion = 0
    tiempo_restante = TIEMPO_LIMITE

def pausar_juego():
    global pausado
    pausado = not pausado

def mostrar_botones_juego():
    dibujar_boton("Pausar", ANCHO - 150, 10, 130, 50, GRIS, AZUL, pausar_juego)
    dibujar_boton("Salir", ANCHO - 150, 70, 130, 50, GRIS, AZUL, salir_juego)

while True:
    if menu_activo:
        mostrar_menu_inicio()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    iniciar_juego()
                elif evento.key == pygame.K_s:
                    salir_juego()
    elif juego_activo:
        pantalla.blit(fondo, (0, 0))  
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and coyote_timer > 0:
                    vel_y = salto
                    salto_sonido.play()  
                    coyote_timer = 0
                elif evento.key == pygame.K_p:
                    pausar_juego()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            vel_x = -5
        elif teclas[pygame.K_RIGHT]:
            vel_x = 5
        else:
            vel_x = 0

        if tiempo_restante <= 0:
            tiempo_restante = 0
            mostrar_mensaje_perdida()
            pygame.time.wait(tiempo_mostrar_mensaje)  
            menu_activo = True
            juego_activo = False
        else:
            if tiempo_restante > 0:
                tiempo_restante -= reloj.get_time() / 1000  

        vel_y += gravedad
        x_pelota += vel_x
        y_pelota += vel_y
        camara_y = min(camara_y, y_pelota - ALTO // 2)

        if x_pelota - radio_pelota < 0: x_pelota = radio_pelota
        if x_pelota + radio_pelota > ANCHO: x_pelota = ANCHO - radio_pelota

        puede_saltar = False
        for plataforma in plataformas:
            if plataforma.colliderect(pygame.Rect(x_pelota - radio_pelota, y_pelota, radio_pelota * 2, radio_pelota)):
                if vel_y > 0:
                    y_pelota = plataforma.top - radio_pelota
                    vel_y = 0
                    puede_saltar = True

        if puede_saltar:
            coyote_timer = coyote_time
        else:
            coyote_timer -= reloj.get_time() / 1000

        if y_pelota > camara_y + ALTO:
            mostrar_mensaje_perdida()
            pygame.time.wait(tiempo_mostrar_mensaje)
            menu_activo = True
            juego_activo = False

        for moneda in monedas[:]:
            if moneda.colliderect(pygame.Rect(x_pelota - radio_pelota, y_pelota - radio_pelota, radio_pelota * 2, radio_pelota * 2)):
                monedas.remove(moneda)
                puntuacion += 1
                tiempo_restante = min(tiempo_restante + 5, TIEMPO_LIMITE)
                sonido_moneda.play()

        pygame.draw.circle(pantalla, ROJO, (int(x_pelota), int(y_pelota) - camara_y), radio_pelota)
        for plataforma in plataformas:
            pygame.draw.rect(pantalla, GRIS, (plataforma.x, plataforma.y - camara_y, plataforma.width, plataforma.height))
        for moneda in monedas:
            pygame.draw.circle(pantalla, DORADO, (moneda.centerx, moneda.centery - camara_y), moneda.width // 2)

        mostrar_texto(f"Puntos: {puntuacion}", 10, 10, fuente, ROJO)
        mostrar_texto(f"Tiempo: {int(tiempo_restante)}s", 10, 40, fuente, ROJO)
        if pausado:
            mostrar_texto("PAUSADO", ANCHO // 2 - 60, ALTO // 2 - 50, fuente, ROJO)

        mostrar_botones_juego()

        pygame.display.flip()
        reloj.tick(60)
