from typing import List
import source.constants as constants
import source.utils as utils
import numpy as np

# define the food class
class Food:
    def __init__(self, position: np.array = constants.INITIAL_POSITION):
        # position
        self.position = position
        # radius
        self.radius = utils.gen_distribution(
            distribution="normal",
            kwargs={
                "loc": constants.FOOD_RADIUS_MEAN,
                "scale": constants.FOOD_RADIUS_STD,
            },
        )
        # color
        self.color = constants.FOOD_COLOR

    # movement functions
    def move(self, currentx_map: np.array, currenty_map: np.array) -> None:
        """
        movement magnitude is determined by self.move_step_size energy cost
        is determined by step size multiplied by trait score for movement
        as we consider step size to require a linear higher cost
        """
        # calculate position inputs
        idx, idy = round(self.position[0]), round(self.position[1])
        # retrieve the relevant deltas
        deltas = np.array([currentx_map[idy, idx], currenty_map[idy, idx]])
        # calculate new positions
        position_hat = self.position + deltas
        # add canvas based adjustments
        position_hat[0] = utils.limit_input(
            number=position_hat[0], vmin=0, vmax=constants.WINDOW_WIDTH - 1
        )
        position_hat[1] = utils.limit_input(
            number=position_hat[1], vmin=0, vmax=constants.WINDOW_HEIGHT - 1
        )
        # reassign position to new positions
        self.position = position_hat

    # get functions
    def get_position(self) -> List[float]:
        """
        get function for the position

        @returns the position of the food
        """
        return self.position

    def get_radius(self) -> float:
        """
        get function for the radius

        @returns the radius of the food
        """
        return self.radius

    def get_color(self) -> str:
        """
        get function for the color

        @returns the color of the food
        """
        return self.color
