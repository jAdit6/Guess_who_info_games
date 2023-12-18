class Person:
    def __init__(self, name, gender, hair_color, eye_color, height, weight):
        self.name = name
        self.gender = gender
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.height = height
        self.weight = weight

class GuessWhoGame:
    def __init__(self, people):
        self.people = people

    def guess_person(self, attribute, value):
        self.people = [person for person in self.people if getattr(person, attribute) == value]

    def get_remaining_people(self):
        return [person.name for person in self.people]

# Creating people for the game
people_list = [
    Person("Alice", "Female", "Blonde", "Blue", "tall", "heavy"),
    Person("Bob", "Male", "Brown", "Brown","tall", "heavy"),
    Person("Charlie", "Male", "Black", "Green","tall", "heavy"),
    Person("Diana", "Female", "Red", "Blue","tall", "heavy"),
    Person("Eve", "Female", "Blonde", "Brown","tall", "heavy"),
    Person("Aditya", "Male", "Black", "Black","tall", "heavy"),
    Person("V", "Female", "Brown", "Brown","tall", "heavy")
]