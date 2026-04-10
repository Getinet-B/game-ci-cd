# app/game.py
import random
import copy


class DamageCalculationError(Exception):
    pass


class Character:
    def __init__(self, name, age, char_type):
        self.name = name
        self.age = age
        self.char_type = char_type

        self.ability_scores = {}
        self.roll_abilities()

        self.health = self.calculate_health()
        self.current_health = self.health

        self.inventory = {
            "consumables": ["Potion", "Coins", "Energy"],
            "gear": ["Dagger", "Bows", "Shield", "Armor"]
        }

        self.has_sneak_attack = True
        self.reflection = None
        self.clone = None
        self.dodging = False
        self.hidden = False
        self.rage_survival_used = False
        self.survive = lambda damage: self._survive_logic(damage)

    def roll_stat(self):
        return 10 + random.randint(1, 8)

    def roll_abilities(self):
        self.ability_scores["Str"] = self.roll_stat()
        self.ability_scores["Dex"] = self.roll_stat()
        self.ability_scores["Con"] = self.roll_stat()

    def calculate_health(self):
        return self.ability_scores["Con"] * 3

    def attack(self):
        base_damage = random.randint(1, 10) + (self.ability_scores["Str"] // 2)
        if self.char_type == "Rogue" and self.has_sneak_attack:
            base_damage += 10
            self.has_sneak_attack = False
        return base_damage

    def _survive_logic(self, damage):
        if self.char_type == "Paladin":
            blocked = self.ability_scores["Con"] // 2
            reduced = max(damage - blocked, 0)
            self.current_health += blocked // 2
            return reduced
        elif self.char_type == "Barbarian":
            if damage >= self.current_health and not self.rage_survival_used:
                self.rage_survival_used = True
                return self.current_health - 1
        return damage

    def take_damage(self, damage):
        if damage < 0:
            raise DamageCalculationError("Damage cannot be negative.")
        if self.dodging:
            damage = damage // 2
            self.dodging = False
        damage = self.survive(damage)
        self.current_health = max(self.current_health - damage, 0)

    def is_alive(self):
        return self.current_health > 0


def simulate_battle():
    player = Character("Hero", 25, "Rogue")
    enemy = Character("Enemy", 30, "Mage")

    damage_to_enemy = player.attack()
    enemy.take_damage(damage_to_enemy)

    if enemy.is_alive():
        damage_to_player = enemy.attack()
        player.take_damage(damage_to_player)

    return {
        "player_hp": player.current_health,
        "enemy_hp": enemy.current_health,
        "player_alive": player.is_alive(),
        "enemy_alive": enemy.is_alive(),
    }
