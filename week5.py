from typing import List, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

class Power:
    def __init__(self, name: str, description: str, power_level: int):
        self.name = name
        self.description = description
        self.power_level = power_level
    
    def __str__(self) -> str:
        return f"{self.name} (Level {self.power_level})"

class Superhero:
    def __init__(self, name: str, secret_identity: str, powers: List[Power]):
        self._name = name  
        self.__secret_identity = secret_identity  
        self.powers = powers
        self.health = 100
        self.energy = 100
        self._mission_count = 0
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def total_power_level(self) -> int:
        return sum(power.power_level for power in self.powers)
    
    def use_power(self, power_name: str) -> str:
        """Use a specific power if the hero has enough energy."""
        for power in self.powers:
            if power.name.lower() == power_name.lower():
                if self.energy >= 10:
                    self.energy -= 10
                    return f"{self.name} uses {power.name}!"
                return f"{self.name} is too tired to use {power.name}..."
        return f"{self.name} doesn't have the power: {power_name}"
    
    def rest(self) -> str:
        """Recover energy and health."""
        self.energy = min(100, self.energy + 30)
        self.health = min(100, self.health + 20)
        return f"{self.name} has recovered! Energy: {self.energy}, Health: {self.health}"
    
    def _complete_mission(self) -> None:
        """Protected method to track missions."""
        self._mission_count += 1
        self.energy = max(0, self.energy - 20)
        self.health = max(0, self.health - 10)

class FlyingHero(Superhero):
    def __init__(self, name: str, secret_identity: str, powers: List[Power], max_altitude: float):
        super().__init__(name, secret_identity, powers)
        self.max_altitude = max_altitude
        self.is_flying = False
    
    def fly(self, altitude: float) -> str:
        """Attempt to fly at the specified altitude."""
        if altitude > self.max_altitude:
            return f"{self.name} cannot fly that high! Maximum altitude: {self.max_altitude}m"
        
        if self.energy >= 15:
            self.energy -= 15
            self.is_flying = True
            return f"{self.name} is now flying at {altitude}m!"
        return f"{self.name} is too tired to fly..."
    
    def land(self) -> str:
        """Land the flying hero."""
        if self.is_flying:
            self.is_flying = False
            return f"{self.name} has landed safely."
        return f"{self.name} is already on the ground."

class TeamLeader(Superhero):
    def __init__(self, name: str, secret_identity: str, powers: List[Power]):
        super().__init__(name, secret_identity, powers)
        self.team_members: List[Superhero] = []
        self.missions_completed = 0
    
    def add_team_member(self, hero: Superhero) -> str:
        """Add a hero to the team."""
        if hero not in self.team_members:
            self.team_members.append(hero)
            return f"{hero.name} has joined {self.name}'s team!"
        return f"{hero.name} is already on the team!"
    
    def lead_mission(self, mission_name: str) -> str:
        """Lead the team on a mission."""
        if not self.team_members:
            return "Cannot start mission: No team members!"
        
        if self.energy < 30:
            return f"{self.name} is too tired to lead a mission..."
        
        # Complete mission for all team members
        self._complete_mission()
        for member in self.team_members:
            member._complete_mission()
        
        self.missions_completed += 1
        return f"Mission '{mission_name}' completed successfully! Team is tired but victorious."


if __name__ == "__main__":
    # Creating some powers
    flight = Power("Flight", "Ability to fly", 8)
    super_strength = Power("Super Strength", "Enhanced physical strength", 9)
    telepathy = Power("Telepathy", "Read and control minds", 7)
    
    # Creating heroes
    superman = FlyingHero("Superman", "Clark Kent", [flight, super_strength], 10000.0)
    professor_x = TeamLeader("Professor X", "Charles Xavier", [telepathy])
    
    # Demonstrating usage
    print(superman.fly(5000)) 
    print(superman.use_power("super strength")) 
    print(superman.land())  
    
    print(professor_x.add_team_member(superman))  
    print(professor_x.lead_mission("Save the City"))  
    
    print(superman.rest())  
    
    
    
    #Activity 2
  

class Vehicle(ABC):
    def __init__(self, name: str, max_speed: float):
        self.name = name
        self.max_speed = max_speed
        self.current_speed = 0
        self.is_moving = False
    
    @abstractmethod
    def move(self) -> str:
        """Define how the vehicle moves."""
        pass
    
    @abstractmethod
    def stop(self) -> str:
        """Define how the vehicle stops."""
        pass
    
    def accelerate(self, speed_increase: float) -> str:
        """Increase the vehicle's speed."""
        if self.current_speed + speed_increase <= self.max_speed:
            self.current_speed += speed_increase
            return f"{self.name} accelerated to {self.current_speed} km/h"
        return f"{self.name} cannot go faster than {self.max_speed} km/h"

class Car(Vehicle):
    def __init__(self, name: str, max_speed: float, fuel_type: str):
        super().__init__(name, max_speed)
        self.fuel_type = fuel_type
        self.engine_started = False
    
    def start_engine(self) -> str:
        """Start the car's engine."""
        self.engine_started = True
        return f"{self.name}'s engine roars to life! "
    
    def move(self) -> str:
        if not self.engine_started:
            return f"Cannot drive {self.name}: Engine is not started!"
        self.is_moving = True
        return f"{self.name} is cruising down the road "
    
    def stop(self) -> str:
        self.is_moving = False
        self.current_speed = 0
        return f"{self.name} comes to a smooth stop "

class Plane(Vehicle):
    def __init__(self, name: str, max_speed: float, max_altitude: float):
        super().__init__(name, max_speed)
        self.max_altitude = max_altitude
        self.current_altitude = 0
        self.is_airborne = False
    
    def move(self) -> str:
        if not self.is_airborne:
            return self.take_off()
        return f"{self.name} is soaring through the clouds "
    
    def take_off(self) -> str:
        """Initiate takeoff sequence."""
        self.is_moving = True
        self.is_airborne = True
        return f"{self.name} takes off into the sky! "
    
    def land(self) -> str:
        """Land the plane."""
        self.is_airborne = False
        return f"{self.name} touches down on the runway "
    
    def stop(self) -> str:
        if self.is_airborne:
            return "Cannot stop while airborne!"
        self.is_moving = False
        self.current_speed = 0
        return f"{self.name} has come to a complete stop on the runway"

class Boat(Vehicle):
    def __init__(self, name: str, max_speed: float, boat_type: str):
        super().__init__(name, max_speed)
        self.boat_type = boat_type
        self.anchor_dropped = True
    
    def raise_anchor(self) -> str:
        """Raise the boat's anchor."""
        self.anchor_dropped = False
        return f"{self.name}'s anchor is up! "
    
    def drop_anchor(self) -> str:
        """Drop the boat's anchor."""
        self.anchor_dropped = True
        return f"{self.name}'s anchor has been dropped "
    
    def move(self) -> str:
        if self.anchor_dropped:
            return f"Cannot sail {self.name}: Anchor is still dropped!"
        self.is_moving = True
        return f"{self.name} is sailing across the waves "
    
    def stop(self) -> str:
        self.is_moving = False
        self.current_speed = 0
        return f"{self.name} glides to a stop on the water"

# Example usage
if __name__ == "__main__":
    # Creating vehicles
    tesla = Car("Tesla Model S", 250, "Electric")
    boeing = Plane("Boeing 747", 900, 13000)
    yacht = Boat("Luxury Yacht", 70, "Motor Yacht")
    
    # Demonstrating different movement behaviors
    print("\nCar Demo:")
    print(tesla.start_engine())
    print(tesla.move())
    print(tesla.accelerate(50))
    print(tesla.stop())
    
    print("\nPlane Demo:")
    print(boeing.move()) 
    print(boeing.accelerate(300))
    print(boeing.land())
    print(boeing.stop())
    
    print("\nBoat Demo:")
    print(yacht.move()) 
    print(yacht.raise_anchor())
    print(yacht.move())
    print(yacht.drop_anchor())