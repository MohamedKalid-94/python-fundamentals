# MULTILEVEL: a chain of inheritance  Vehicle -> Car -> ElectricCar

class Vehicle:
    def __init__(self, brand):
        self.brand = brand
        print("Vehicle init")

    def info(self):
        return f"Vehicle: {self.brand}"

    def honk(self):
        return "beep"


class Car(Vehicle):
    def __init__(self, brand, doors):
        super().__init__(brand)
        self.doors = doors
        print("Car init")

    def info(self):
        return super().info() + f", doors={self.doors}"


class ElectricCar(Car):
    def __init__(self, brand, doors, battery):
        super().__init__(brand, doors)
        self.battery = battery
        print("ElectricCar init")

    def info(self):
        return super().info() + f", battery={self.battery}kWh"


e = ElectricCar("Tesla", 4, 75)
# Vehicle init
# Car init
# ElectricCar init          the parents are initialised FIRST, going up the chain

print(e.info())                         # Vehicle: Tesla, doors=4, battery=75kWh
print(e.honk())                         # beep        inherited from the grandparent
print([c.__name__ for c in ElectricCar.__mro__])
# ['ElectricCar', 'Car', 'Vehicle', 'object']

print(isinstance(e, ElectricCar), isinstance(e, Car), isinstance(e, Vehicle))
# True True True

# Call a method of a specific ancestor
print(Vehicle.info(e))                  # Vehicle: Tesla

# HIERARCHICAL: one parent, several children
class Truck(Vehicle):
    pass

class Bike(Vehicle):
    pass

print(Truck("MAN").honk(), Bike("BMX").honk())
# Vehicle init
# Vehicle init
# beep beep

# HYBRID: any mix of the above (for example a diamond on top of a chain).
# Keep chains short: more than 3 levels is usually hard to follow.