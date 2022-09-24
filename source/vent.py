import tkinter
from typing import List, Tuple
import source.constants as constants
import source.utils as utils
import source.food as food

# define the vent class
class Vent:
    def __init__(self, prod_rate: int):
        """
        @param prod_rate = production rate for food
        """
        # position
        self.position = utils.gen_position()
        # radius
        self.radius = constants.VENT_RADIUS
        # color
        self.color = constants.VENT_COLOR
        # food
        self.prod_rate = prod_rate

    # create functions
    def create_foods(self, canvas: tkinter.Canvas) -> Tuple[List[food.Food]]:
        """
        creates a list of food based on the production rate

        @param canvas = canvas to draw on
        @returns food_objects = memory tracked positions of the food
        @returns food_drawings = memory tracked canvas drawings of the food
        """
        # instantiate drawing objects
        food_objects = {}
        food_drawings = {}
        # loop through the n to produce
        for _ in range(self.prod_rate):
            # create the object
            food_object = food.Food(position=self.position)
            # get the id
            food_id = id(food_object)
            # draw the food
            food_drawing = utils.draw_circular_object(
                canvas=canvas,
                position=food_object.position,
                radius=food_object.radius,
                fill_color=food_object.color,
                outline_color=constants.FOOD_OUTLINE_COLOR,
            )
            # append to trackers
            food_objects[food_id] = food_object
            food_drawings[food_id] = food_drawing
        return (food_objects, food_drawings)

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
