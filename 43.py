import pygame
import math

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
#аппаратное ускорение, двойной буфер, изменение размера
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)

pygame.init()
pygame.mixer.init() # музыка
car_image = pygame.image.load('cactus.png').convert_alpha()

road_image = pygame.image.load('desert.png')
background = pygame.transform.smoothscale(road_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Движение машины")

class CarSprite(pygame.sprite.Sprite):
    def __init__(self, car_image, x, y, rotations=360):
        pygame.sprite.Sprite.__init__(self)
        self.rot_img = [] #список повернутых изо
        self.min_angle = (360 / rotations) # минимальный угол поворота
        for i in range(rotations): # создаем повернутые изображения

            rotated_image = pygame.transform.rotozoom(car_image, 360 - 90 - (i * self.min_angle), 0.2)

            self.rot_img.append(rotated_image)

        # преобразуем минимальный угол в радианы
        self.min_angle = math.radians(self.min_angle)
        self.image = self.rot_img[0] # установили начальное изображение
        self.rect = self.image.get_rect() # получаем квадрат вокруг пикчи
        self.rect.center = (x, y) # устанавливаем начальное положение авто
        self.reversing = False
        self.heading = 0 # текущий угол направления машина
        self.speed = 0
        self.velocity = pygame.math.Vector2(0, 0) # вектор скорости
        self.position = pygame.math.Vector2(x, y) # вектор автомобиля

    def turn(self, angle_degrees):
        self.heading += math.radians(angle_degrees) # изменяем угол напралвения
        image_index = int(self.heading / self.min_angle) % len(self.rot_img) #
        #получаем индекс изображения для данного угла
        if self.image != self.rot_img[image_index]:# если оно изменилось
            x, y = self.rect.center # запоминаем текущее положение
            self.image = self.rot_img[image_index] # устанавливаем новое изображение
            self.rect = self.image.get_rect() # новый квадрат
            self.rect.center = (x, y) # старый квадрат

    def accelerate(self, amount):
        if not self.reversing: # если зад ход фолс
            self.speed += amount
        else:
            self.speed -= amount

    def brake(self): # метод торможения
        self.speed /= 2
        if abs(self.speed) < 0.1:
            self.speed = 0

    def reverse(self):
        self.speed = 0
        self.reversing = not self.reversing




    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        #преобразование полярны координат в вектор
        self.position += self.velocity # изменяем положение авто
        self.rect.center = (round(self.position[0]), round(self.position[1])) #прямоугольник изо обнуляем

car_image = pygame.image.load('cactus.png').convert_alpha()
black_car = CarSprite(car_image, WINDOW_WIDTH //2, WINDOW_HEIGHT // 2)
car_sprites = pygame.sprite.Group()
car_sprites.add(black_car)


clock = pygame.time.Clock()
done = False
while not done:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           done = True

       elif event.type == pygame.VIDEORESIZE:
           WINDOW_WIDTH = event.w
           WINDOW_HEIGHT = event.h
           window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
           background = pygame.transform.smoothscale(road_image,
                                             (WINDOW_WIDTH, WINDOW_HEIGHT))  # Масштабируем фон по новым размерам

       elif event.type == pygame.KEYUP:
           if event.key == pygame.K_h:
               print('beep - beep')

           elif event.key == pygame.K_r:
               print('nazad')
               black_car.reverse()

           elif event.key == pygame.K_DOWN:
               print('brake')
               black_car.brake()

           elif event.key == pygame.K_UP:
               print('accelerate')
               black_car.accelerate(0.5)

   keys = pygame.key.get_pressed()
   if keys[pygame.K_LEFT]:
       black_car.turn(-1.8)

   if keys[pygame.K_RIGHT]:
       black_car.turn(1.8)

   car_sprites.update()
   window.blit(background, (0, 0))
   car_sprites.draw(window)
   pygame.display.flip()
   clock.tick_busy_loop(60)

pygame.quit()