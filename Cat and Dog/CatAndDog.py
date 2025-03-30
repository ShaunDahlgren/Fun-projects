class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def greet(self):
        print(f"Hi!  I'm {self.name}, and I'm a {self.species}.")

    def make_sound(self):
        if self.species == "cat":
            print("Meow!")
        elif self.species == "dog":
            print("Woof!")
        else:
            return 0

my_pet = Pet("Bubbles", "dog")
my_pet.greet()
my_pet.make_sound()