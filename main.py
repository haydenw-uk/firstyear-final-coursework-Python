# Copyright 2024 - Hayden Williams
# End of Year Final Coursework - the Oxford Brookes University

import random
import time
import os


def show_board(board):
  # Get width, height integers
  width = len(board[0])
  height = len(board)

  # Format board to be shown to user
  print("/*** GAMEBOARD ***/")
  for i in range(len(board)):
    row = ''
    for j in range(len(board[i])):
      if board[i][j] == '':
        row += '. '
      else:
        row += str(board[i][j]) + ' '
    print(row)


def set_board(width, height):
  board = []
  for h in range(height):
    sub_list = [''] * width
    board.append(sub_list)
  return board


def set_start_time():
  # Time is used for score, this sets up to the correct rounded value
  current_time_seconds = time.time()

  current_time_seconds = round(current_time_seconds, 2)

  return current_time_seconds


def set_end_time(start_time, timeout_to_subtract):
  # This works out the time at the end through simple subtraction and rounding
  end_time = time.time()

  calculated_final_time = ((end_time - start_time) - timeout_to_subtract)

  calculated_final_time = round(calculated_final_time, 2)

  return calculated_final_time


def spawn_random_walls(board):
  # Initialise ranges
  lower_width = 0
  lower_height = 0

  upper_width = len(board[0])
  upper_height = len(board)

  # Spawn wall generation upper and lower bounds
  lower_random_spawns_count = 3
  upper_random_spawns_count = upper_height / 2

  # Select a random number of walls to add (loops)
  walls_to_spawn = random.randint(lower_random_spawns_count,
                                  int(upper_random_spawns_count))

  for spawns in range(walls_to_spawn):
    new_spawn_wall_width = random.randint(lower_width, upper_width - 1)
    new_spawn_wall_height = random.randint(lower_height, upper_height - 1)

    if board[new_spawn_wall_height][new_spawn_wall_width] == '':
      board[new_spawn_wall_height][new_spawn_wall_width] = 'W'

    # If space already occupied, try again!
    elif board[new_spawn_wall_height][new_spawn_wall_width] != '':
      pass

  return board


def spawn_random_landmine_traps(board):
  # Initialise ranges
  lower_width = 0
  lower_height = 0

  upper_height = len(board[0])
  upper_width = len(board)

  # Spawn land mine generation upper and lower bounds
  lower_random_spawns_count = 2
  upper_random_spawns_count = upper_height / 2

  # Select a random number of landmines to add (loops)
  landmine_traps_to_spawn = random.randint(lower_random_spawns_count,
                                           int(upper_random_spawns_count))

  for spawns in range(landmine_traps_to_spawn):
    new_spawn_landmine_trap_width = random.randint(lower_width,
                                                   upper_width - 1)
    new_spawn_landmine_trap_height = random.randint(lower_height,
                                                    upper_height - 1)

    if board[new_spawn_landmine_trap_height][
        new_spawn_landmine_trap_width] == '':
      board[new_spawn_landmine_trap_height][
          new_spawn_landmine_trap_width] = '.'

    elif board[new_spawn_landmine_trap_height][
        new_spawn_landmine_trap_width] != '':
      pass

  return board


def spawn_random_health_powerups(board):
  # Initialise ranges
  lower_width = 0
  lower_height = 0

  upper_height = len(board[0])
  upper_width = len(board)

  # Spawn generation upper and lower bounds
  lower_random_spawns_count = 1
  upper_random_spawns_count = upper_height / 2

  # Select a random number of health powerups to add (loops)
  health_powerups_to_spawn = random.randint(lower_random_spawns_count,
                                            int(upper_random_spawns_count))

  for spawns in range(health_powerups_to_spawn):
    new_spawn_health_powerups_width = random.randint(lower_width,
                                                     upper_width - 1)
    new_spawn_health_powerups_height = random.randint(lower_height,
                                                      upper_height - 1)

    if board[new_spawn_health_powerups_height][
        new_spawn_health_powerups_width] == '':
      board[new_spawn_health_powerups_height][
          new_spawn_health_powerups_width] = 'H'

    elif board[new_spawn_health_powerups_height][
        new_spawn_health_powerups_width] != '':
      pass

  return board


def player_reached_end_and_won(board, player_current_position,
                               endpoint_position):
  player_current_y, player_current_x = player_current_position
  endpoint_position_y, endpoint_position_x = endpoint_position

  # Check whether player current position = end_point_position (i.e. at end point)
  if board[player_current_y][player_current_x] == board[endpoint_position_y][
      endpoint_position_x]:
    return True
  else:
    return False


def calculate_endpoint_point(board):
  # Find upper and lower bounds of Board

  upper_width = len(board[0])
  upper_height = len(board)

  # Ensure that there is a minimum distance between points to make it fairer to players (although still random)
  lower_width = 0.75 * upper_width
  lower_height = 0.75 * upper_height

  # Calculate new points
  new_point_width = random.randint(int(lower_width), upper_width - 1)
  new_point_height = random.randint(int(lower_height), upper_height - 1)

  return new_point_width, new_point_height


def add_player_to_start_point(board, start_point):
  # Player @ character replaces start point marked on board to prepare for player to start the new game
  board[start_point[0]][start_point[1]] = "@"
  return board


def set_start_end_points(board):
  # Add points generated to board as characters
  point_width, point_height = 0, 0
  start_point = point_width, point_height

  point_width, point_height = calculate_endpoint_point(board)
  end_point = point_width, point_height

  # Set points on Board
  board[start_point[0]][start_point[1]] = "S"
  board[end_point[0]][end_point[1]] = "E"

  return board, start_point, end_point


def get_current_player_position_on_board(board):
  # Enumerate (find out the number of) and loop through entire board checking for @ character of player location
  for i, row in enumerate(board):
    for j, char in enumerate(row):
      if char == '@':
        return (i, j)


def move_player(direction, player, board, spaces_to_move):
  player_pos = player['current_pos']

  y, x = player_pos
  # Please note, the x and y are reversed from standard co-ordinates so this switch is made for ease of reading of below changes to player position.

  if direction == "NORTH":
    new_player_position = (x, y - spaces_to_move)
  elif direction == "SOUTH":
    new_player_position = (x, y + spaces_to_move)
  elif direction == "EAST":
    new_player_position = (x + spaces_to_move, y)
  elif direction == "WEST":
    new_player_position = (x - spaces_to_move, y)

  if check_move_legal(board, new_player_position):
    board = update_player_position_on_board(board, new_player_position)
    player['current_pos'] = get_current_player_position_on_board(board)
    print(f"Moved Player : {direction} by {spaces_to_move}")
  else:
    print("Move not allowed!")

  return board


def check_move_legal(board, new_proposed_player_pos):
  # Check move will not go off board
  # Check move won't land on wall
  if check_move_within_bounds_of_board(board, new_proposed_player_pos) == True:
    if check_walls_obstruction(board, new_proposed_player_pos) == False:
      return True
  else:
    return False


def update_player_position_on_board(board, new_player_pos):
  x, y = new_player_pos
  # Physically actuate move of player to new position on the board
  # 1. Find player @ on board currently and replace with 'blank' space
  # 2. Add player @ to new position parsed into function
  computed_board = []
  for sublist in board:
    new_sublist = []
    for char in sublist:
      new_sublist.append(char.replace('@', ''))
    computed_board.append(new_sublist)
  computed_board[y][x] = "@"

  return computed_board


def check_move_within_bounds_of_board(board, new_proposed_player_pos):
  # Find upper bounds of Board
  upper_width = len(board[0])
  upper_height = len(board)
  # Check whether move would go off board index or stay within it!
  if (0 <= new_proposed_player_pos[1] < upper_width
      and 0 <= new_proposed_player_pos[0] < upper_height):
    return True
  else:
    return False


def check_walls_obstruction(board, player_pos):
  # Check whether computed new player position is occupied by a wall obstruction
  x, y = player_pos
  if board[y][x] == 'W':
    return True
  else:
    return False


def is_player_on_landmine(board, player_pos):
  # Check whether player is on (hidden) land mine by
  # comparing location to hidden mine character '.'
  y, x = player_pos
  if board[x][y] == '.':
    return True
  else:
    return False


def is_player_on_health_powerup(board, player_pos):
  # Check whether player is on health powerup by
  # comparing location to 'H' health powerup character
  y, x = player_pos
  if board[x][y] == 'H':
    return True
  else:
    return False


def check_move_player_commands_legal(direction_command):
  # Compare requested player move direction with a set of possible moves available
  legal_move_directions = {'NORTH', 'SOUTH', 'WEST', 'EAST'}
  return direction_command in legal_move_directions


def show_main_menu():
  # Show main menu options for game
  return (
      "== MAIN MENU ==\nVLB - View Leaderboard\nNEW - New Game\n\n\nQUIT - Any other keys\n\n: "
  )


def show_action_panel():
  # Show actions in game which can be used
  return (
      "ACTION PANEL\nmove north/south/east/west\nhealth\ntimer\nsave (exits)\nQUIT (without saving)\n\n: "
  )


def clear_screen():
  # Clear prior output on terminal
  os.system('clear')


def display_health(player):
  # Fetch current player health from player dictionary and output
  health = player['health']
  print(f"Your Health : {health}")


def update_health(player, amount, less_or_more_health):
  # Computes new player health
  current_player_health = player['health']
  updated_health = current_player_health

  if less_or_more_health == "-":
    # If action remove health, take-away health from player from parsed amount
    updated_health = current_player_health - amount
  elif less_or_more_health == "+":
    # If action add health, add health from player from parsed amount
    updated_health = current_player_health + amount

  # Set player key 'health' to new, updated health value
  player['health'] = updated_health
  return player


def remove_mine_from_board_and_reset_player(board, current_player_positon):
  # Save current position for player (to be reset)
  current_y, current_x = current_player_positon

  # Move player back to start ! (Effect of the explosion kickback)
  reset_y, reset_x = 0, 0
  reset_position = reset_y, reset_x
  board = update_player_position_on_board(board, reset_position)
  # Remove mine and replace with blank character on board to 'deactivate it'
  board[current_y][current_x] = ''

  return board


def remove_health_powerup_from_board_and_reset_player(board,
                                                      current_player_positon):

  # Save current position for player (to be reset)
  current_y, current_x = current_player_positon

  # Move player back to start!
  reset_y, reset_x = 0, 0
  reset_position = reset_y, reset_x
  board = update_player_position_on_board(board, reset_position)

  # Remove health powerup and replace with blank character on board to 'deactivate it'
  board[current_y][current_x] = ''

  return board


def load_and_display_leaderboard_from_file(filename):
  # Open leaderboard file from parsed in filename
  leaderboard_file = open(filename)
  print("~~ LEADERBOARD ~~\n")
  # Set formatted index value of leaderboard position to prepare for line 1
  leaderboard_index = 1
  for line in leaderboard_file:
    # Loop through line by line of leaderboard file (3 top scores)
    line = line.strip('\n')
    line_split = line.split(',')
    # Split into 'names' and 'scores'
    name = line_split[0]
    score = line_split[1]
    # Print formatted values to user
    print(f"{leaderboard_index}. {name} | {score}\n")
    # Increase formatted index of leaderboard position for next line
    leaderboard_index += 1
  # Safely close file
  leaderboard_file.close()
  # Print end formatting for leaderboard print-out
  print("~~~~~~~~~~~~~~~~~\nCarpe diem\n\n")


def has_current_player_made_leaderboard(filename, score):
  # Open leaderboard in read-only mode
  with open(filename, 'r') as leaderboard_file:
    # Initialise a list for leaderboard scores
    leaderboard_scores = []
    # Loop over every line in leaderboard file
    for line in leaderboard_file:
      # Split into individual values
      line_split = line.strip().split(', ')
      # Extract only player score from current leaderboard line, convert to float
      player_score = float(line_split[1])
      # Append to the leaderboard scores
      leaderboard_scores.append(player_score)

  # If current player's score is less than the max value the leaderboard
  # the player belongs on leaderboard so return True (time = lower better)
  return score < max(leaderboard_scores)


def update_leaderboard_file_with_new_player(filename, new_player_score,
                                            new_player_name):
  # Open leaderboard file with read-only permissions
  with open(filename, 'r') as leaderboard_file:
    # Initialise leaderboard_data list
    leaderboard_data = []
    # Loop through every line in leaderboard_file (3 top scores so will be three lines)
    for line in leaderboard_file:
      # Strip each line into an 'entry'
      entry = line.strip().split(',')
      # Add the player name and score from the stripped 'entry'
      # to the leaderboard_data list
      leaderboard_data.append((entry[0], entry[1]))

  # Leaderboard hasn't been updated (if applicable... yet) so set value as such
  updated_leaderboard = False
  # Loop through the index of leaderboard_data
  for i, entry in enumerate(leaderboard_data):
    # Create an entry based on existing player names and player scores found already
    existing_player_name, player_score = entry

    # Compare float of (current) new_player_score and
    # the float of (prior leaderboard) player_score
    if float(new_player_score) < float(player_score):
      # Insert into leaderboard_data list with correct index and float converted to string
      leaderboard_data.insert(i, (new_player_name, str(new_player_score)))
      # Leaderboard has been updated now so change value to reflect this
      updated_leaderboard = True
      # Break out of the loop because the update is done! I could not see another way
      # to do this hence why this structue has been utilised.
      break

  # If the length is too short (i.e. file doesn't exist or too short of scores)
  if updated_leaderboard or len(leaderboard_data) < 3:
    # Open in write-mode the leaderboard file (which creates / overwrites file)
    with open(filename, 'w') as leaderboard_file:
      # For every entry in the leaderboard (reduced to 3 values max)
      for entry in leaderboard_data[:3]:
        # Format string with new empty entry
        entry_string = f'{entry[0]}, {entry[1]}\n'
        # Finally write this string to file
        leaderboard_file.write(entry_string)


def main():
  # Set value to ensure invalid options keep menu in loop
  remain_on_main_menu = True
  while remain_on_main_menu == True:
    # Show welcome messages
    # Show main menu options
    print("\*/ WELCOME! \*/")
    game_start = input(show_main_menu())
    # Convert to upper to ensure non-capitalised input not rejected
    game_start = game_start.upper()
    clear_screen()

    if game_start == "VLB":
      # User selected for leaderboard to be output
      load_and_display_leaderboard_from_file("leaderboard.txt")

    elif game_start == "NEW":
      # User selected a NEW game to be created
      # Escape main menu options loop by changing value to False
      remain_on_main_menu = False

      # Configure board object, player starting health
      board = []
      start_health = 100

      # Set board size in height, width squares
      board = set_board(10, 10)
      # Spawn random wall objects into the board
      board = spawn_random_walls(board)
      # Spawn random landmine_traps (hidden) into board
      board = spawn_random_landmine_traps(board)
      # Spawn random health powerups into the board
      board = spawn_random_health_powerups(board)
      # Configure start + end-points of game to start and end game at
      board, start_point, end_point = set_start_end_points(board)

      # Set-up player dictionary with start position, health and set gamewon state
      player = {
          "health": start_health,
          "game_won": False,
          "current_pos": start_point
      }

      # Add player to board, replacing start-point with '@' to denote player current position
      board = add_player_to_start_point(board, start_point)

      # Officially start game timer (score for game... lower = better)
      game_start_time = set_start_time()
      # Tell player timer has been started
      print("Timer started!")

      # Show player start board
      show_board(board)

      while player['game_won'] == False and player['health'] > 0:
        # While game not won (check state in player dictionary) AND player health > 0

        # Show action panel of actions usable to user
        command = input(show_action_panel())
        # Convert command(s) entered into upper-case to allow for lower-case input to work
        command = command.upper()

        # Split the command into a list so a sub-command can be found e.g the two command parts of 'move' and then the compass direction like 'north'
        commands_split_into_list = command.split()
        clear_screen()

        # Check if on health powerup
        on_health_powerup = is_player_on_health_powerup(
            board, player['current_pos'])
        if on_health_powerup:
          clear_screen()
          health_to_add = 50
          print(
              f"You consumed a health powerup which has added {health_to_add} to your health!"
          )
          player = update_health(player, health_to_add, '+')
          display_health(player)
          # Remove health powerup from board because it has been used
          board = remove_health_powerup_from_board_and_reset_player(
              board, player['current_pos'])

        # Check if player on (hidden) landmine
        on_landmine = is_player_on_landmine(board, player['current_pos'])
        if on_landmine:
          clear_screen()
          health_to_remove = 50
          print(
              f"[EXPLOSION] 💣💥\nYou stumbled across a mine which has taken {health_to_remove} from your health!"
          )
          player = update_health(player, health_to_remove, '-')
          display_health(player)
          board = remove_mine_from_board_and_reset_player(
              board, player['current_pos'])

        if commands_split_into_list[0] == "HEALTH":
          # If player wishes to view their current health stat
          display_health(player)

        if commands_split_into_list[0] == "QUIT":
          # Game end message to user and show them their time up to that point
          print("Goodbye!")
          end_time = set_end_time(game_start_time, 0)
          print(f"Your time upon exit was {end_time}")
          exit()

        if commands_split_into_list[0] == "TIMER":
          # Show the player how much time has passed at present
          end_time = set_end_time(game_start_time, 0)
          print(f"Time so far is {end_time}")

        if commands_split_into_list[0] == "MOVE":
          # Verify sub-command with direction for move is in valid directions set
          is_move_valid_command = check_move_player_commands_legal(
              commands_split_into_list[1])
          if is_move_valid_command == True:
            # Move player direction by parsed in number of squares (1)
            board = move_player(commands_split_into_list[1], player, board, 1)
            # Update player dictionary with new player current position
            player['current_pos'] = get_current_player_position_on_board(board)

          else:
            # User direction not present on set of valid directions
            print("Move direction not valid. Please try again.")

        else:
          # Command not valid, ask user to try again
          print("Not a valid command! Try again")

        # Check whether player has 'died' of no health --> quit game if so
        if player['health'] <= 0:
          clear_screen()
          print("GAME OVER!")
          time.sleep(2)
          print(
              "YOU LOST ALL OF YOUR HEALTH. TRY AGAIN NEXT TIME.\n\n\nQUITTING IN 5 SECONDS."
          )
          # Give player timeout before quitting for effect
          time.sleep(5)
          exit()

        # Check whether player has reached end-point (won)... or if game should continue
        if player_reached_end_and_won(board, player['current_pos'], end_point):
          player['game_won'] = True
          # Stop timer
          timeout_to_subtract = 0
          # Subtract any timeouts given to player which would have affected time
          final_time = set_end_time(game_start_time, timeout_to_subtract)

          # See whether time is leaderboard worthy
          player_made_leaderboard = has_current_player_made_leaderboard(
              'leaderboard.txt', final_time)

          clear_screen()
          print("PLAYER WON!\n\n")
          time.sleep(1)

          # Process, display stats for current player's just won game
          health = player['health']
          print(
              f"-- YOUR STATS --\nYour Time : {final_time}\nYour Health : {health}\n\nThank you for playing ..... now let's see whether you made the leaderboard."
          )
          # Add a wait period for effect before leaderboard position announced to player / not
          time.sleep(1.5)
          print("DRUMROLL....")
          time.sleep(2)

          if player_made_leaderboard:
            # Player time was low enough for leaderboard !
            print("YOU DID MAKE THE LEADERBOARD! :)")
            # Ask player to enter name which is used on leaderboard
            current_player_leaderboard_name = input("Enter your name : ")

            # Update leaderboard file with this new time, player name and player score
            # Compute position to add in file + which to delete / move
            update_leaderboard_file_with_new_player(
                'leaderboard.txt', final_time, current_player_leaderboard_name)

          else:
            # Player did NOT make leaderboard
            print("YOU DID NOT MAKE THE LEADERBOARD :(")

          # Display leaderboard (which may or may not have been updated by prior function)
          load_and_display_leaderboard_from_file('leaderboard.txt')
          # Quit game
          quit()

        else:
          show_board(board)

    else:
      # User selected any key which quit the game
      print("Goodbye...")
      exit()


if __name__ == "__main__":
  main()
