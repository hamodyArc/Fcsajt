import random

class Varelse:
    def __init__(self, namn, hp, dmg):
        self.namn = namn
        self.hp = hp
        self.dmg = dmg

    def attack(self, target):
        target.hp -= self.dmg
        print(f"{self.namn} attackerar {target.namn} för {self.dmg} skada")

    def heal(self, target, healInt):
        target.hp += healInt
        print(f"{self.namn} healar {target.namn} för {healInt} hp")
    
    def is_alive(self):
        return self.hp > 0
    

class Fajter(Varelse):
    def __init__(self, namn, hp, dmg, weapon):
        super().__init__(namn, hp, dmg)
        self.weapon = weapon

    def attack(self, target):
        target.hp -= self.dmg + self.weapon
        print(f"{self.namn} attackerar {target.namn} för {self.dmg + self.weapon} skada")

class Monster(Varelse):
    def __init__(self, namn, hp, dmg, fear):
        super().__init__(namn, hp, dmg)
        self.fear = fear

    def fearsummon(self):
        print(f"{self.namn} skapar en aura av rädsla")

class Djur(Varelse):
    def __init__(self, namn, hp, dmg, healInt):
        super().__init__(namn, hp, dmg)
        self.healInt = healInt

    def healer(self, target):
        self.heal(target, self.healInt)
class Weapon:
    def __init__(self, namn, dmg):
        self.namn = namn
        self.dmg = dmg

class Arena:
    def __init__(self, *varelser):
        self.varelser = list(varelser)

    def fight(self):
        while len([v for v in self.varelser if v.is_alive()]) > 1:
            attacker = random.choice(self.varelser)
            target = random.choice(self.varelser)

            if attacker != target or not attacker.is_alive() or not target.is_alive():
                if isinstance(attacker, Djur):
                    attacker.healer(target)
                else:
                    attacker.attack(target)
            


        winner = next((v for v in self.varelser if v.is_alive()), None)
        if winner:
            print(f"Vinnaren är {winner.namn}")
        else:
            print("Ingen vinner, alla är döda!")

Weapon1 = Weapon("Svärd", 2)
Weapon2 = Weapon("Yxa", 4)
Monster1 = Monster("Goblin", 10, 2, 1)
Monster2 = Monster("Ork", 20, 4, 2)
Fajter1 = Fajter("Krigare", 15, 3, 2)
djurH = Djur("Häst", 10, 0, 2)

rumble = Arena(Monster1, Monster2, Fajter1, djurH)
rumble.fight()