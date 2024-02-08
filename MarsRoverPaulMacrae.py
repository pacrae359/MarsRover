# Class for rovers holding location in plateau and heading
class Rover:
	def __init__(self, x, y, heading, commands):
		self.x = int(x)
		self.y = int(y)
		self.heading = heading
		self.commands = commands

	def __str__(self):
		return f"({self.x}, {self.y}) {self.heading} {self.commands}"

# Class for the plateau holding the maximum x and y values allowed.
class Plateau():
	def __init__(self, maxX, maxY):
		# max X and max Y needed to check if rover input is possible, don't need to store entire plateau to save space, could have used a list of tuples to 
		# compare to if storing the plateau as a data type.
		self.maxX = int(maxX)
		self.maxY = int(maxY)

def check_CollideY(next_move, current_rover, rover_coordsX, rover_coordsY):
	for i in range(len(rover_coordsX)):
		if rover_coordsY[i] == (current_rover.y + next_move) and rover_coordsX[i] == current_rover.x:
			return True
	return False

def check_CollideX(next_move, current_rover, rover_coordsX, rover_coordsY):
	for i in range(len(rover_coordsY)):
		if rover_coordsX[i] == (current_rover.x + next_move) and rover_coordsY[i] == current_rover.y:
			return True
	return False

def check_duplicate(new_X, new_Y, rover_coordsX, rover_coordsY):
	for i in range(len(rover_coordsY)):
		if rover_coordsX[i] == new_X and rover_coordsY[i] == new_Y:
			return True
	return False

def move_Rover(current_rover, rovers, counter, rover_coordsX, rover_coordsY):
	# CHECK IF NEXT COORDINATE IS WITHIN PLATEAU AND DOESNT COLLIDE WITH ANOTHER ROVER, IF EITHER IS TRUE ABORT AND GIVE REASONING
	# OTHERWISE UPDATE NEW ROVER POSITION MOVING FORWARD IN DIRECTION OF HEADING
	lefts = ["N","W","S","E"]
	rights = ["N","E","S","W"]
	#next_Moves = {"N" : "y + 1", "E" : "x + 1", "S" : "y - 1", "W" : "x - 1"}
	for command in current_rover.commands:
		# Change the coordinates of the rover based on the heading it currently has, wanted to do this with a dictionary ^^^, 
		# but couldnt get it to work sadly :(
		backup_X = current_rover.x
		backup_Y = current_rover.y
		if command == "M":
			# Based on heading, move in a direction. Horrible nested ifs here, was rushed, I apologise for poor readibility.
			if current_rover.heading == "N":
				if not check_CollideY(1, current_rover, rover_coordsX, rover_coordsY):
					current_rover.y += 1
				else:
					return print(f"For rover {counter}, to avoid a collision with another rover, not all moves could be completed.")
			if current_rover.heading == "S":
				if not check_CollideY(-1, current_rover, rover_coordsX, rover_coordsY):
					current_rover.y -= 1
				else:
					return print(f"For rover {counter}, to avoid a collision with another rover, not all moves could be completed.")
			if current_rover.heading == "W":
				if not check_CollideX(-1, current_rover, rover_coordsX, rover_coordsY):
					current_rover.x -= 1
				else:
					return print(f"For rover {counter}, to avoid a collision with another rover, not all moves could be completed.")
			if current_rover.heading == "E":
				if not check_CollideX(1, current_rover, rover_coordsX, rover_coordsY):
					current_rover.x += 1
				else:
					return print(f"For rover {counter}, to avoid a collision with another rover, not all moves could be completed.")
			# If the next move will take the rover out of the plateau, stop, but keep its current new position.
			if current_rover.x > plateau.maxX or current_rover.y > plateau.maxY or current_rover.x < 0 or current_rover.y < 0:
				# Doesn't make the move if it will go outside of plateau, and aborts further moves.
				current_rover.x = backup_X
				current_rover.y = backup_Y
				return print(f"For rover {counter}, one of the proposed moves goes outside of the plateau. This rover will stop before this move.")
			rover_coordsX[counter-1] = current_rover.x
			rover_coordsY[counter-1] = current_rover.y
		if command == "L":
			newheading = lefts.index(current_rover.heading)
			if newheading == 3:
				newheading = -1
			current_rover.heading = lefts[newheading+1]
		if command == "R":
			newheading = rights.index(current_rover.heading)
			if newheading == 3:
				newheading = -1
			current_rover.heading = rights[newheading+1]


# Main code body
# get the top right coordinate of the plateau from user input
continue_program = False
# this does not catch adding punctuation or special characters, it only catches extra white space and extra values (Should have used regular expressions or my
# later set validation instead)
while not continue_program:

	plateau_top = (input("Enter Top Right coordinate of Plateau (Format: X Y): ").strip()).split(" ")
	try:
		if len(plateau_top) == 2:
			plateau = Plateau(plateau_top[0],plateau_top[1])
			continue_program = True
		else:
			print("Please try again using the correct format for input!")
	except ValueError:
		print("Please try again using the correct format for input!")

print(plateau_top)
add_new_rover = True
rovers = []
rover_coordsX = []
rover_coordsY = []
# used to ensure inputs are only L R or M for the commands part of user input.
allowed_directions = ["L","R","M"]
# used to ensure headings are only "N","W","E" or "S".
allowed_headings = ["N","W","E","S"]

while add_new_rover:
	# Does the user want to make a new rover, N will begin moving and updating rover coordinates, this will only work for Y or N inputs (regardless of case)
	new_rover_answer = (input("Add a new rover (Y/N)? ").strip()).upper()

	if new_rover_answer == "Y":
		add_new_rover = True
		continue_program = False
		# this catches a few errors on input such as extra spaces of lower case which will matter later when checking headings.

		while not continue_program:
			rover_position = (input("Enter Rover Position (Format: X Y H) : ").upper()).split(" ")
			# test to see if I can change the input into wanted data types, if I can then the input is desired and I can continue, else restart
			try:

				if (len(rover_position) == 3):
					rover_position[0] = int(rover_position[0])
					rover_position[1] = int(rover_position[1])
					rover_position[2] = str(rover_position[2])
					if (rover_position[2] in allowed_headings):
						if check_duplicate(rover_position[0], rover_position[1], rover_coordsX, rover_coordsY):
							print("These rover coordinates are already in use!")
						else:
							continue_program = True
					else:
						print("Please try again using the correct format for input!")
				else:
					print("Please try again using the correct format for input!")

			except ValueError:
				print("Please try again using the correct format for input!")

		continue_program = False

		while not continue_program:
			rover_commands = [*(input("Enter Rover Commands (Format LRM): ").upper()).replace(" ","")]
			check = [i in allowed_directions for i in rover_commands]
			if all(check):
				continue_program = True
		rovers.append(Rover(rover_position[0], rover_position[1], rover_position[2], rover_commands))
		# stores x and y coordinates so I dont have to check every coordinate every time, just one batch then the other at the same index if there is a
		# match to avoid collisions
		rover_coordsX.append(rovers[-1].x)
		rover_coordsY.append(rovers[-1].y)

	elif new_rover_answer == "N":

		# execute rover commands and output ending location and heading when all are finished moving
		done_moving = False
		counter = 0

		if len(rovers) != 0:

			while not done_moving:
				counter += 1
				if len(rovers) == 1:	
					done_moving = True
				current_rover = rovers.pop(0)
				move_Rover(current_rover, rovers, counter, rover_coordsX, rover_coordsY)	
				print(f"Rover {counter} New Coordinates and Heading: {current_rover.x} , {current_rover.y} , {current_rover.heading}")	

		add_new_rover = False

print("End of Program")