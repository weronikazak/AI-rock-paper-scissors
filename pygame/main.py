import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
from time import sleep
import random
# import tensorflow as tf

hand_top, hand_right, hand_bottom, hand_left = 150, 600, 400, 350

# SCREEN
camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Rock-Paper-Scissors")
screen = pygame.display.set_mode([1000,480])

# IMAGES
computer_img = pygame.image.load("icons/computer.png")

rock_img = pygame.image.load("icons/rock2.png")
rock_img =  pygame.transform.scale(rock_img, (80, 80))

paper_img = pygame.image.load("icons/paper3.png")
paper_img =  pygame.transform.scale(paper_img, (80, 80))

scissors_img = pygame.image.load("icons/scissors2.png")
scissors_img =  pygame.transform.scale(scissors_img, (80, 80))

# FONTS
font = pygame.font.Font('freesansbold.ttf', 32)
countdown_font = pygame.font.Font('freesansbold.ttf', 50)

SIGNS = ["rock", "paper", "scissors", "quit", "none"]

GAME_ON = True
START_GAME = False
ROUND = 1
USER_POINTS, COMPUTER_POINTS = 0, 0
VERDICT = "XD"
# model = tf.keras.models.load_model("RPS.model")

white = (255, 255, 255)
black = (0, 0, 0)

w, h = 100, 100
comp_center_coords = (170, h//2 - 80)
computer_choice, user_choice = "none", "none"

countdown_started = False

		
def start_countdown(start_ticks):
	seconds=(pygame.time.get_ticks()-start_ticks)/1000
	count = countdown_font.render(str(int(seconds)), False, white)
	screen.blit(count, (170, h//2 - 80))
	
	if seconds >= 3.99:
		return False, seconds
	else: return True, seconds


def show_computer_choice():
	choice = random.choice(SIGNS[:-2])
	if choice == "paper":
		choice = paper_img
	elif choice == "rock":
		choice = rock_img
	elif choice == "scissors":
		choice = scissors_img
	return choice


def show_points():
	count = font.render("COMPUTER    YOU\n  {}   {}".format(COMPUTER_POINTS, USER_POINTS), False, white)
	screen.blit(choice, (comp_center_coords[0], comp_center_coords[1] - 150))


def compare_signs(user_sign, comp_sign, GAME_ON, user_points, comp_points, verdict):
    if user_sign == "quit":
        verdict = "YOU QUITED"
        GAME_ON = False
    elif user_sign == "none":
        comp_points += 1
        verdict = "POINT FOR PC!"
    elif user_sign == comp_sign:
        verdict = "REMIS!"
    else:
        if user_sign == "scissors":
            if comp_sign == "rock":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
        elif user_sign == "rock":
            if comp_sign == "paper":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
        elif user_sign == "paper":
            if comp_sign == "scissors":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
    return GAME_ON, user_points, comp_points, verdict


try:
	while GAME_ON:

		ret, frame = camera.read()

		screen.fill([4, 47, 102])
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w  = frame.shape[:2]
		frame = np.rot90(frame)
		frame = pygame.surfarray.make_surface(frame)
		screen.blit(frame, (1000 - w,0))

		screen.blit(computer_img, ( (750 - w) // 2,100))

		if not START_GAME:
			start_game1 = font.render('Press any key', False, white)
			start_game2 = font.render('to START', False, white)
			screen.blit(start_game1, (70, 50))
			screen.blit(start_game2, (100, h-100))
		else:
			if not countdown_started:
				start_ticks=pygame.time.get_ticks()
			countdown_started, secs = start_countdown(start_ticks)

			if secs >= 3.99:
				start_ticks = pygame.time.get_ticks()
				computer_choice = show_computer_choice()
				secs2 = 0
				while secs2 < 4:
					pygame.display.update()
					screen.blit(computer_choice, (145, 140))
					secs2 += .001
				# GAME_ON, USER_POINTS, COMPUTER_POINTS, VERDICT = compare_signs(sign, comp_sign, GAME_ON, user_points, comp_points, verdict)


		pygame.display.update()

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit(0)
				else:
					START_GAME = True
except KeyboardInterrupt:
	pygame.quit()
	cv2.destroyAllWindows()