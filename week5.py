from typing import List, Optional
from datetime import datetime

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