import gear

class Armor:
    def __init__(self, head=None, body=None, legs=None, feet=None):
        self.head = head
        self.body = body
        self.legs = legs
        self.feet = feet
    
    def set_piece(self, piece, value):
        if piece in ("head", "body", "legs", "feet"):
            self.verify_piece(value, piece)
            setattr(self, piece, value)
        else:
            raise ValueError("Invalid piece")
        
    # create a set_multiple method that takes a dictionary of pieces and values
    def set_multiple(self, pieces):
        for piece, value in pieces.items():
            self.set_piece(piece, value)
            
    def verify_piece(self, piece, type):
        # if piece is in armor_pieces, return the piece
        # check under the armor type of armor_pieces
        # if it's not there, return False
        if piece in gear.armor_pieces[type]:
            return piece
        else:
            return False

    def set_equipped_piece(self, piece, type):
        verified_piece = self.verify_piece(piece, type)
        piece_type = type.lower()
        setattr(self, piece_type, verified_piece)

class Weapon:
    def __init__(self, weapon_type=None, name=None, damage=None, speed=None):
        self.weapon_type = weapon_type
        self.name = name
        self.damage = damage
        self.speed = speed
        
    def set_weapon(self, weapon_type, weapon_name):
        if weapon_type in gear.weapons:
           setattr(self, weapon_name, weapon_type)
            
    def set_equipped(self, weapon_type, weapon_name, damage, speed):
        if weapon_type in gear.weapons:
            self.weapon_type = weapon_type
            self.name = weapon_name
            self.damage = damage
            self.speed = speed
        else:
            raise ValueError("Invalid weapon type")
    

class Player:
    def __init__(self, name, hp, level, armor=None, weapon=None):
        self.name = name
        self.hp = hp
        self.level = level
        self.armor = armor or Armor()
        self.weapon = weapon or Weapon()
        self.inventory = []
        
    def set_attributes(self, attributes):
        self.name = attributes.get("name", self.name)
        self.hp = attributes.get("hp", self.hp)
        self.level = attributes.get("level", self.level)
        self.weapon = attributes.get("weapon", self.weapon)
        self.armor = attributes.get("armor", self.armor)
        
    def add_to_inventory(self, item):
        if item in gear.armor_pieces:
            verified_piece = self.armor.verify_piece(item)
            self.armor.set_piece(verified_piece, item)
        
    @property
    def equipped_armor(self):
        return {
            piece_name: getattr(self.armor, piece_name) 
            for piece_name in ["head", "body", "legs", "feet"] 
            if getattr(self.armor, piece_name)
        }
    @property
    def equipped_weapon(self):
        return {
            weapon_name: getattr(self.weapon, weapon_name)
            for weapon_name in ["weapon_type", "name", "damage", "speed"]
            if getattr(self.weapon, weapon_name)
        }
    @property
    def defense(self):
        defense = 0
        for armor_type, piece in self.equipped_armor.items():
            # replace the space with an underscore
            piece = piece.replace(" ", "_")
            # grab the defense value from gear.armor_pieces by using the piece name
            defense += gear.armor_pieces[armor_type][piece]["Defense"]
        return defense
    
    def get_alive_status(self):
        return self.hp > 0
        