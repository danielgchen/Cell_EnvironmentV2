from typing import List
import source.constants as constants

# define the vent class
class Vent:
    def __init__(self):
        # position
        self.position = constants.INITIAL_POSITION
        # radius
        self.radius = constants.VENT_RADIUS
        # color
        self.color = constants.VENT_COLOR

    # get functions
    def get_position(self) -> List[float]:
        """
        get function for the position

        @returns the position of the vent
        """
        return self.position

    def get_radius(self) -> float:
        """
        get function for the radius

        @returns the radius of the vent
        """
        return self.radius

    def get_color(self) -> str:
        """
        get function for the color

        @returns the color of the vent
        """
        return self.color
