import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
from time import sleep
import random
import tensorflow as tf

hand_top, hand_right, hand_bottom, hand_left = 150, 600, 400, 350
model = tf.keras.models.load_model("RPS.model")
IMG_SIZE = 50

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

results_img = pygame.image.load("icons/results.png")
results_img =  pygame.transform.scale(results_img, (1000-640, 50))


# FONTS
font = pygame.font.Font('freesansbold.ttf', 32)
countdown_font = pygame.font.Font('freesansbold.ttf', 50)

SIGNS = ["rock", "paper", "scissors", "quit", "none"]

GAME_ON = True
START_GAME = False
ROUND = 1
USER_POINTS, COMPUTER_POINTS = 0, 0

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
red = (255, 0, 0)
green = (0, 255, 0)

w, h = 100, 100
comp_center_coords = (170, h//2 - 80)
computer_choice, user_choice = "none", "paper"

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
		choice_img = paper_img
	elif choice == "rock":
		choice_img = rock_img
	elif choice == "scissors":
		choice_img = scissors_img
	return choice, choice_img


def show_points():
	screen.blit(results_img, (0, h-50))
	count = font.render(f"{COMPUTER_POINTS}                   {USER_POINTS}", False, white)
	screen.blit(count, (80, h-40))



def guess_user_choice(hand):
    hand = cv2.cvtColor(hand, cv2.COLOR_RGB2GRAY)
    r, hand_thresh = cv2.threshold(hand, 90, 255, cv2.THRESH_BINARY_INV)
    hand = cv2.resize(hand, (IMG_SIZE, IMG_SIZE))
    hand = hand.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    prediction = model.predict(hand)
    return SIGNS[np.argmax(prediction)]


def compare_signs(user_sign, comp_sign, GAME_ON, user_points, comp_points):
    if user_sign == "quit":
        verdict = "YOU QUITED"
        GAME_ON = False
    elif user_sign == "none":
        comp_points += 1
        verdict = "POINT FOR PC!"
    elif user_sign == comp_sign:
        verdict = " IT'S A DRAW!"
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

    if "YOU" in verdict:
        color = green
    elif "DRAW" in verdict:
    	color = gray
    else:
   	    color = red

    return GAME_ON, user_points, comp_points, font.render(verdict, False, color)


try:
	while GAME_ON:

		ret, frame = camera.read()

		screen.fill([4, 47, 102])
		cv2.rectangle(frame, (hand_left, hand_top), (hand_right, hand_bottom), (0, 255, 0), 2)
		hand_frame = frame[hand_top:hand_bottom, hand_left:hand_right]

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w  = frame.shape[:2]
		frame = np.rot90(frame)
		frame = pygame.surfarray.make_surface(frame)
		screen.blit(frame, (1000 - w,0))
		screen.blit(computer_img, ( (750 - w) // 2,100))

		if not START_GAME:
			start_game1 = font.render('Press any key', False, white)
			smile = countdown_font.render(":)", False, white)
			start_game2 = font.render('to START', False, white)
			screen.blit(start_game1, (70, 50))
			screen.blit(smile, (170, h//2 - 80))
			screen.blit(start_game2, (100, h-100))
		else:
			show_points()
			user_choice = guess_user_choice(hand_frame)
			user_choice_text = font.render(user_choice, False, white)
			screen.blit(user_choice_text, (300, 50))

			if not countdown_started:
				start_ticks=pygame.time.get_ticks()
			countdown_started, secs = start_countdown(start_ticks)

			if secs >= 3.99:
				start_ticks = pygame.time.get_ticks()
				computer_choice, computer_choice_img = show_computer_choice()
				GAME_ON, USER_POINTS, COMPUTER_POINTS, VERDICT = compare_signs(user_choice, computer_choice, GAME_ON, USER_POINTS, COMPUTER_POINTS)
				secs2 = 0
				while secs2 < 4:
					screen.blit(computer_choice_img, (145, 140))
					screen.blit(VERDICT, (60, 50))
					pygame.display.update()

					secs2 += .001


		pygame.display.update()

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit(0)
				else:
					START_GAME = True

pygame.quit()
cv2.destroyAllWindows()
camera.release()
sys.exit(0)