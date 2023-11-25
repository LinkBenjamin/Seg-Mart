import sys, pygame
import config.globalvars
import segment.analytics as analytics

from app.utils.imports import import_folder
from config.files import get_full_path

class Player(pygame.sprite.Sprite):
    def __init__(self, position, hitboxinflate, groups, obstacle_sprites, items):
        super().__init__(groups)
        self.image = pygame.image.load(get_full_path("static", "Jeff", "down_idle", "Jeff-Front-Idle.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(hitboxinflate,hitboxinflate)
        
        self.space_pressed = False

        # Animation Setup
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites
        self.items = items

        self.touching_item = ' '

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status + '_idle'

    def import_player_assets(self):
        character_path = get_full_path('static', 'Jeff')
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle':[], 'down_idle': [], 'left_idle': [], 'right_idle': []
                          }
        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        keys = pygame.key.get_pressed()

        # Character Movement Input Controls
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # Object Interaction Controls
        if keys[pygame.K_SPACE] and not self.space_pressed:
            self.space_pressed = True
            if config.globalvars.object_interaction != ' ':
                if config.globalvars.object_interaction == 't':
                    #do checkout-y things
                    config.globalvars.shopping_bag.clear()
                else:
                    #put item in shopping bag
                    config.globalvars.shopping_bag.append(config.globalvars.object_interaction)
        if not keys[pygame.K_SPACE]:
            self.space_pressed = False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        self.touch()
        config.globalvars.object_interaction = self.touching_item

    def touch(self):
        for sprite in self.items:
            if sprite.hitbox.colliderect(self.hitbox):
                self.touching_item = sprite.sprite_type
                break
            if sprite.sprite_type not in self.touching_item:
                self.touching_item = ' '

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    else:
                        self.hitbox.left = sprite.hitbox.right
                    

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.hitbox = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)