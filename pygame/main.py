import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import os
from time import sleep
import random
import tensorflow as tf
from utils import visualization_utils as viz_utils


class RockPaperScissors():
	def __init__(self):
		pygame.init()
		
		# TENSORFLOW MODEL
		self.detect_fn = tf.saved_model.load('../tensorflow_object_detection_api/inference_graph/saved_model')

		self.category_index = {
		    1: {'id': 1, 'name': 'rock'},
		    2: {'id': 2, 'name': 'paper'},
		    3: {'id': 3, 'name': 'scissors'},
		    4: {'id': 4, 'name': 'rock'},
		    5: {'id': 5, 'name': 'quit'}
		}


		# PYGAME
		self.camera = cv2.VideoCapture(0)
		pygame.display.set_caption("Rock-Paper-Scissors")
		self.screen = pygame.display.set_mode([1000,480])


		# IMAGES
		self.computer_img = pygame.image.load("icons/computer.png")

		self.rock_img = pygame.image.load("icons/rock2.png")
		self.rock_img =  pygame.transform.scale(self.rock_img, (80, 80))

		self.paper_img = pygame.image.load("icons/paper3.png")
		self.paper_img =  pygame.transform.scale(self.paper_img, (80, 80))

		self.scissors_img = pygame.image.load("icons/scissors2.png")
		self.scissors_img =  pygame.transform.scale(self.scissors_img, (80, 80))

		self.results_img = pygame.image.load("icons/results.png")
		self.results_img =  pygame.transform.scale(self.results_img, (1000-640, 50))


		# FONTS
		self.font = pygame.font.Font('freesansbold.ttf', 32)
		self.countdown_font = pygame.font.Font('freesansbold.ttf', 50)


		# COLORS
		self.white = (255, 255, 255)
		self.gray = (220, 220, 220)
		self.red = (255, 0, 0)
		self.green = (0, 255, 0)


		# GAME VARIABLES
		self.SIGNS = ["rock", "paper", "scissors", "quit", "other"]

		self.GAME_ON = True
		self.START_GAME = False
		self.USER_POINTS, self.COMPUTER_POINTS = 0, 0

		self.w, self.h = 100, 100
		self.comp_center_coords = (170, self.h//2 - 80)
		self.computer_choice, self.user_choice = "other", "paper"

		self.countdown_started = False


		# START GAME
		self.main()
			

	### DESTRUCTOR ###
	def __del__(self):
		pygame.quit()
		self.camera.release()
		cv2.destroyAllWindows()
		sys.exit(0)

	
	### COUNTDOWN TO COMPUTER CHOICE AND SIGNS COMPARISON BETWEEN USER AND COMPUTER ###
	def start_countdown(self, start_ticks):
		seconds=(pygame.time.get_ticks()-start_ticks)/1000
		count = self.countdown_font.render(str(int(seconds)), False, self.white)
		self.screen.blit(count, (170, self.h//2 - 80))
		
		if seconds >= 3.99:
			return False, seconds
		else: return True, seconds


	### CHOOSE COMPUTER SIGN AND RETURN ITS ICON ### 
	def show_computer_choice(self):
		choice = random.choice(self.SIGNS[:-2])
		if choice == "paper":
			choice_img = self.paper_img
		elif choice == "rock":
			choice_img = self.rock_img
		elif choice == "scissors":
			choice_img = self.scissors_img
		return choice, choice_img


	### SHOW COMPUTER AND USER SCORE ON THE BOTTOM ###
	def show_points(self):
		self.screen.blit(self.results_img, (0, self.h-50))
		count = self.font.render(f"{self.COMPUTER_POINTS}                  {self.USER_POINTS}", False, self.white)
		self.screen.blit(count, (80, self.h-40))


	### COMPARE COMPUTER'S AND USER'S SIGNS AND JUDGE WHO WINS THE ROUND ###
	def compare_signs(self, user_sign, comp_sign, GAME_ON, user_points, comp_points):
	    if user_sign == "quit":
	        verdict = "YOU QUITED"
	        GAME_ON = False
	    elif user_sign == "other":
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

	    # choose verdict's colour
	    if "DRAW" in verdict or "QUIT" in verdict:
	    	color = self.gray
	    elif "YOU" in verdict:
	        color = self.green
	    else:
	   	    color = self.red

	    return GAME_ON, user_points, comp_points, self.font.render(verdict, False, color)



	### CONVERT FRAME TO NUMPY ARRAY AND RESHAPE IT ###
	def load_image_into_numpy_array(self, image):
	  (im_height, im_width) = image.shape[:2]
	  return np.array(image).reshape(
	      (im_height, im_width, 3)).astype(np.uint8)


	### DRAW RECTANGLE ON HAND AND RETURN CHOSEN SIGN ###
	def detect_hand(self, frame, game_start):
		# if game hasn't started yet, exit the function
		if not game_start:
			return frame, self.user_choice

		frame_np = self.load_image_into_numpy_array(frame)
		input_tensor = np.expand_dims(frame_np, 0)
		detections = self.detect_fn(input_tensor)
		viz_utils.visualize_boxes_and_labels_on_image_array(
	    	frame_np,
	    	detections['detection_boxes'][0].numpy(),
	    	detections['detection_classes'][0].numpy().astype(np.int32),
	    	detections['detection_scores'][0].numpy(),
	    	self.category_index,
	    	use_normalized_coordinates=True,
	    	max_boxes_to_draw=1,
	    	min_score_thresh=.4,
	    	skip_scores=True,
	    	skip_labels=True,
	    	agnostic_mode=False
	    	)

		# choose the second detection from the array
		user_choice = self.category_index[detections['detection_classes'][0].numpy().astype(np.int32)[1]]
		return frame_np, user_choice["name"]


	### MAIN FUNCTION ###
	def main(self):
		while self.GAME_ON:
			ret, frame = self.camera.read()

			# start detecting hand when user starts the game
			frame, self.user_choice = self.detect_hand(frame, self.START_GAME)

			# expand the game window on the left by filling it with colour
			# and displaying computer icon
			self.screen.fill([4, 47, 102])
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.h, self.w  = frame.shape[:2]
			frame = np.rot90(frame)
			frame = pygame.surfarray.make_surface(frame)
			self.screen.blit(frame, (1000 - self.w,0))
			self.screen.blit(self.computer_img, ( (750 - self.w) // 2,100))

			# if game is not started, wait for any key to be pressed
			if not self.START_GAME:
				start_game1 = self.font.render('Press any key', False, self.white)
				smile = self.countdown_font.render(":)", False, self.white)
				start_game2 = self.font.render('to START', False, self.white)
				self.screen.blit(start_game1, (70, 50))
				self.screen.blit(smile, (170, self.h//2 - 80))
				self.screen.blit(start_game2, (100, self.h-100))
			else:
				# if the game is on, show the user and computer score
				self.show_points()
				user_choice_text = self.font.render(self.user_choice, False, self.white)
				self.screen.blit(user_choice_text, (400, 30))

				# if the countdown hasn't started yet, begin it
				if not self.countdown_started:
					start_ticks=pygame.time.get_ticks()
				self.countdown_started, secs = self.start_countdown(start_ticks)

				# if nearly 4 seconds have passed, compare user's and computer's signs
				# show the verdict and update score
				if secs >= 3.99:
					start_ticks = pygame.time.get_ticks()
					self.computer_choice, computer_choice_img = self.show_computer_choice()
					self.GAME_ON, self.USER_POINTS, self.COMPUTER_POINTS, VERDICT = self.compare_signs(self.user_choice,
																										self.computer_choice,
																										self.GAME_ON,
																										self.USER_POINTS,
																										self.COMPUTER_POINTS)
					secs2 = 0
					while secs2 < 4:
						self.screen.blit(computer_choice_img, (145, 140))
						self.screen.blit(VERDICT, (60, 50))
						pygame.display.update()

						secs2 += .001


			pygame.display.update()

			# exit the game pressing "Q" key
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_q:
						self.GAME_ON = False
					else:
						self.START_GAME = True



if __name__ == "__main__":
	rps_game = RockPaperScissors()