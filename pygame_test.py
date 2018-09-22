import pygame
import sys
import time
from view_model import *
from model.model import Passenger

size = width, height = 620, 440
black = 0, 0, 0
passenger_icon = pygame.image.load("PoliceOfficer.png")

passenger_floor1_1 = Passenger(1, 1)
passenger_floor1_2 = Passenger(1, 1)
passenger_floor2_1 = Passenger(1, 2)
passenger_floor3_1 = Passenger(1, 3)
passenger_floor4_1 = Passenger(1, 4)
passengers = [
    passenger_floor1_1,
    passenger_floor1_2,
    passenger_floor2_1,
    passenger_floor3_1,
    passenger_floor4_1
]

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
animation_handler = AnimationHandler()
view_dimensions = ViewDimensions(0, 0, width, height)
leave_speed = (5, 0)
view_passenger_manager = ViewPassengerManager(
    passenger_capacity=10,
    animation_handler=animation_handler,
    view_dimensions=view_dimensions,
    leave_speed=leave_speed,
    display_surface=screen)
view_passenger_manager.passengers_enter(passengers)

while True:
    if pygame.event.peek(pygame.QUIT):
        sys.exit()

    if animation_handler.is_animation():
        animation_handler.iterate_animation()
    else:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                view_passenger_manager.passengers_leave(1)
            if event.key == pygame.K_2:
                view_passenger_manager.passengers_leave(2)
            if event.key == pygame.K_3:
                view_passenger_manager.passengers_leave(3)

    current_view_passengers = view_passenger_manager.get_view_passengers()

    screen.fill(black)
    for view_passenger in current_view_passengers:
        view_dimensions = view_passenger.get_passenger_view_dimensions()
        screen.blit(passenger_icon, view_dimensions.get_left_corner())

    pygame.display.flip()

    clock.tick(30)


