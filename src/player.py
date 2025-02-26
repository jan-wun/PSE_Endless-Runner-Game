import pygame
from src.assets import Assets
from src.entity import Entity
from src.enums import PlayerState, WeaponType, GameState
from src.weapon import Weapon
import random
import json
import asyncio

class Player(Entity):
    """
    Enhanced Player class with chaos-driven mechanics and multiplayer-ready features.
    """

    def __init__(self, images_idle, images_walk, images_jump, images_slide, game):
        """
        Initializes the player with animations, chaos stats, and networked state.

        Args:
            images_idle (list): Idle animation images.
            images_walk (list): Walk animation images.
            images_jump (list): Jump animation images.
            images_slide (list): Slide animation images.
            game (Game): Game instance for chaos context.
        """
        self.assets = Assets()
        self.game = game
        self.position = [100, 520]  # Initial chaos spawn

        super().__init__(self.position, images_idle, PlayerState.IDLE, game)

        # Chaos Stats
        self.max_health = self.assets.config.get("max_player_health", 100)
        self.health = self.assets.config.get("initial_player_health", 50)
        self.chaos_meter = 0  # New chaos energy
        self.max_chaos = 100  # Chaos cap
        self.invincible = False
        self.invincible_time = self.game.fps * self.assets.config.get("invincible_time", 2)

        # Weapons with Chaos Upgrades
        self.weapons = {
            WeaponType.DEFAULT: Weapon([self.position[0] + self.rect.width, self.position[1] + 30], 
                                      WeaponType.DEFAULT, game, self),
            WeaponType.CHAOS_BLADE: Weapon([self.position[0] + self.rect.width, self.position[1] + 20], 
                                          WeaponType.CHAOS_BLADE, game, self, damage=20)
        }
        self.current_weapon = WeaponType.DEFAULT

        # Animation Chaos
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.images_jump = images_jump
        self.images_slide = images_slide
        self.animations = {
            PlayerState.IDLE: self.images_idle,
            PlayerState.WALKING_LEFT: self.images_walk,
            PlayerState.WALKING_RIGHT: self.images_walk,
            PlayerState.JUMPING: self.images_jump,
            PlayerState.SLIDING: self.images_slide,
            PlayerState.DASHING: images_walk  # New dash chaos
        }
        self.animation_speed = self.assets.config.get("player_animation_speed", 0.1)
        self.current_frame = 0

        # Movement Chaos
        self.speed = self.assets.config.get("player_speed", 5)
        self.jump_height = self.assets.config.get("player_jump_height", 15)
        self.jump_speed = self.jump_height
        self.is_jumping = False
        self.is_sliding = False
        self.is_dashing = False  # New dash state
        self.dash_speed = self.speed * 2  # Chaos dash boost
        self.dash_duration = self.game.fps * 0.5  # Half-second dash
        self.dash_cooldown = 0
        self.dash_cooldown_max = self.game.fps * 2  # 2-second cooldown
        self.slide_height = self.assets.config.get("player_slide_height", 450)
        self.slide_speed_reduction = self.assets.config.get("player_slide_speed_reduction", 0.2)
        self.slide_end_position = self.assets.config.get("player_slide_end_position", 20)
        self.slide_speed = self.speed
        self.slide_cooldown = 0
        self.slide_cooldown_max = self.assets.config.get("player_slide_cooldown_max", 60)
        self.shoot_pressed = False

        # Chaos State
        self.current_state = PlayerState.IDLE
        self.previous_walking_state = None
        self.facing_right = True  # Direction for chaos visuals

        # Multiplayer Chaos
        self.player_id = random.randint(1000, 9999)  # Unique chaos ID
        self.network_state = {}  # Socket-ready chaos sync

    def handle_input(self):
        """
        Handles chaotic player input with new dash and weapon swap mechanics.
        """
        keys = pygame.key.get_pressed()
        if self.game.current_state != GameState.PLAYING:
            return

        # Horizontal Chaos Movement
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not self.is_sliding and not self.is_dashing:
            self.move_right()
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not self.is_sliding and not self.is_dashing:
            self.move_left()
        else:
            self.current_state = PlayerState.IDLE

        # Jump, Slide, Dash Chaos
        if keys[pygame.K_UP] and not self.is_jumping and not self.is_sliding and not self.is_dashing:
            self.assets.sounds["jump"].play()
            self.is_jumping = True
        elif keys[pygame.K_DOWN] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not self.is_jumping and not self.is_sliding and self.slide_cooldown == 0:
            self.is_sliding = True
            self.slide_cooldown = self.slide_cooldown_max
        elif keys[pygame.K_LSHIFT] and self.dash_cooldown == 0 and self.chaos_meter >= 20:
            self.is_dashing = True
            self.dash_cooldown = self.dash_cooldown_max
            self.chaos_meter -= 20  # Chaos cost

        # Shooting Chaos
        if keys[pygame.K_SPACE] and not self.shoot_pressed:
            self.shoot()
            self.shoot_pressed = True
        elif not keys[pygame.K_SPACE]:
            self.shoot_pressed = False

        # Weapon Swap Chaos
        if keys[pygame.K_1]:
            self.switch_weapon(WeaponType.DEFAULT)
        elif keys[pygame.K_2] and self.chaos_meter >= 50:
            self.switch_weapon(WeaponType.CHAOS_BLADE)

    def move_left(self):
        """Move player left with chaos boundary checks."""
        self.current_state = PlayerState.WALKING_LEFT
        self.facing_right = False
        new_x = self.position[0] - (self.speed + self.game.scrolling_bg_speed)
        self.position[0] = max(new_x, 0)

    def move_right(self):
        """Move player right with chaos boundary checks."""
        self.current_state = PlayerState.WALKING_RIGHT
        self.facing_right = True
        new_x = self.position[0] + self.speed
        self.position[0] = min(new_x, self.game.width - self.rect.width)

    def jump(self):
        """Execute chaotic jump with refined physics."""
        if self.is_jumping:
            self.current_state = PlayerState.JUMPING
            if self.jump_speed >= -self.jump_height:
                direction = 1 if self.jump_speed >= 0 else -1
                self.position[1] -= self.jump_speed * direction * 0.5  # Smoother chaos jump
                self.jump_speed -= 0.5  # Gradual descent
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.previous_walking_state = PlayerState.WALKING_LEFT
                elif keys[pygame.K_RIGHT]:
                    self.previous_walking_state = PlayerState.WALKING_RIGHT
            else:
                self.is_jumping = False
                self.jump_speed = self.jump_height

    def slide(self):
        """Execute chaotic slide with momentum decay."""
        if self.is_sliding:
            self.current_state = PlayerState.SLIDING
            self.position[1] = self.slide_height
            self.slide_speed -= self.slide_speed_reduction

            if self.slide_speed > 0:
                new_x = self.position[0] + (self.slide_speed if self.facing_right else -self.slide_speed - self.game.scrolling_bg_speed)
                self.position[0] = max(0, min(new_x, self.game.width - self.rect.width))
            else:
                self.is_sliding = False
                self.position[1] -= self.slide_end_position
                if self.facing_right:
                    self.position[0] += self.image.get_width() - self.images_idle[0].get_width()
                self.slide_speed = self.speed

    def dash(self):
        """New chaos dash mechanic with speed burst."""
        if self.is_dashing:
            self.current_state = PlayerState.DASHING
            self.invincible = true
            self.dash_duration -= 1
            new_x = self.position[0] + (self.dash_speed if self.facing_right else -self.dash_speed - self.game.scrolling_bg_speed)
            self.position[0] = max(0, min(new_x, self.game.width - self.rect.width))
            if self.dash_duration <= 0:
                self.is_dashing = False
                self.invincible = False
                self.dash_duration = self.game.fps * 0.5

    def switch_weapon(self, weapon_type):
        """Switch to a chaotic weapon with requirements."""
        if weapon_type in self.weapons:
            self.current_weapon = weapon_type
            self.weapon = self.weapons[weapon_type]

    def shoot(self):
        """Fire chaotic weapon with chaos boost."""
        weapon = self.weapons[self.current_weapon]
        if weapon.shots >= 1:
            weapon.fire()
            self.assets.sounds['shoot'].play()
            self.chaos_meter += 5  # Chaos gain per shot—#FuryGlowX fury

    def update_animation(self):
        """Update chaotic animations with directional chaos."""
        self.image_list = self.animations.get(self.current_state, self.images_idle)
        if not self.facing_right and self.current_state in [PlayerState.WALKING_LEFT, PlayerState.JUMPING, PlayerState.DASHING]:
            self.image_list = [pygame.transform.flip(image, True, False) for image in self.image_list]
        self.update_animation_frame()

    def update_animation_frame(self):
        """Smooth chaos animation frame updates."""
        self.current_frame = (self.current_frame + self.animation_speed) % len(self.image_list)
        self.image = self.image_list[int(self.current_frame)]

    async def update_network_state(self):
        """New async chaos sync for multiplayer—#BlazeRush velocity."""
        self.network_state = {
            "player_id": self.player_id,
            "position": self.position.copy(),
            "state": self.current_state.value,
            "health": self.health,
            "chaos": self.chaos_meter,
            "weapon": self.current_weapon.value
        }
        await self.game.network.send_packet(self.network_state)  # Assuming a network manager

    def
