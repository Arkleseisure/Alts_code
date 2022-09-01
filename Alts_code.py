import display_module
import time
from random import random
import threading

num_teams = 10
num_sim_matches = 3
num_total_matches = 20

'''
Main class for the teams.
'''
class Team():
    def __init__(self, number):
        self.not_played = []
        self.matches_played = 0
        self.sides = [0 for i in range(num_sim_matches)]
        self.team_number = number
        self.consecutive_games = 0
        self.consecutive_off = 0
        self.max_consec = 0
        self.max_off = 0
        self.prev_consec = 0
        self.prev_off = 0
        self.prev_max_consec = 0
        self.prev_max_off = 0
        self.prev_last_team_played = 0
        self.last_team_played = 0

    # adds a game to the team's stats, given the opponent and location of the match
    def add_game(self, opponent, loc):
        self.prev_consec = self.consecutive_games
        self.prev_off = self.consecutive_off
        self.prev_max_consec = self.max_consec
        self.prev_max_off = self.max_off
        if opponent in self.not_played:
            self.not_played.pop(self.not_played.index(opponent))
        self.consecutive_games += 1
        self.matches_played += 1
        self.consecutive_off = 0
        self.sides[loc] += 1
        self.prev_last_team_played = self.last_team_played
        self.last_team_played = opponent
        if self.consecutive_games > self.max_consec:
            self.max_consec = self.consecutive_games

    # adds a match period where the team is off the ice
    def add_off(self):
        self.prev_consec = self.consecutive_games
        self.prev_off = self.consecutive_off
        self.prev_max_consec = self.max_consec
        self.prev_max_off = self.max_off
        self.consecutive_off += 1
        self.consecutive_games = 0
        if self.consecutive_off > self.max_off:
            self.max_off = self.consecutive_off

    # undo the changes made by the add_game function
    def undo_add_game(self, opponent, loc):
        self.consecutive_games = self.prev_consec
        self.consecutive_off = self.prev_off
        self.max_consec = self.prev_max_consec
        self.not_played.append(opponent)

        # when the number of sides are changed, the sides lists are reset to 0, 
        # this checks that that hasn't happened before removing one from that side
        if loc < len(self.sides) and self.sides[loc] > 0:
            self.sides[loc] -= 1

        self.matches_played -= 1
        self.last_team_played = self.prev_last_team_played

    # undo changes made by the add_off function
    def undo_add_off(self):
        self.consecutive_games = self.prev_consec
        self.consecutive_off = self.prev_off
        self.max_off = self.prev_max_off

    # function to print out the team details
    def __str__(self):
        if num_sim_matches == 1:
            side_descriptor = ''
        elif num_sim_matches == 2:
            side_descriptor = 'Stairs: ' + str(self.sides[0]) + ' Clock: ' + str(self.sides[1])
        elif num_sim_matches == 3:
            side_descriptor = 'Stairs: ' + str(self.sides[0]) + ' Middle: ' + str(self.sides[1]) + ' Clock: ' + str(self.sides[2])
        else:
            side_descriptor = ''
            for i in range(num_sim_matches):
                side_descriptor += 'Side ' + str(i + 1) + ': ' + str(self.sides[i]) + ' '

        return 'Team ' + str(self.team_number) + ': Matches played: ' + str(self.matches_played) + ' ' + side_descriptor + ' max on: ' + str(self.max_consec) + ' max off: ' + str(self.max_off)


'''
Class holding the information about a particular match and priorities for where it should be played
'''
class Match():
    def __init__(self, team1, team2):
        self.teams = [team1, team2]

        # makes arrays holding higher/lower values for the number of games played at each spot
        # e.g team1 has played 1, 0, 3 times at locations 0, 1 and 2 and team2 has done this 2, 2, 0 times
        # this will then return [1, 0, 0] for the min list and [2, 2, 3] for the max list
        max_played_in_loc = [max(team1.sides[i], team2.sides[i]) for i in range(num_sim_matches)]
        min_played_in_loc = [min(team1.sides[i], team2.sides[i]) for i in range(num_sim_matches)]

        # uses the min and max lists to make a preference order for which sides to play on.
        self.preference_order = sorted(range(num_sim_matches), key=lambda i: (max_played_in_loc[i], min_played_in_loc[i]))
        # min, max matches lists, but ordered so that it aligns itself with the preference order.
        # for the example above, preference order would be [1, 0, 2], indicating the preferred location for the match is 1, then 0, then 2
        # this gives a min list of [0, 1, 0] and a max list of [2, 2, 3]
        self.min_matches_at_loc = [min_played_in_loc[self.preference_order[i]] for i in range(len(self.preference_order))]
        self.max_matches_at_loc = [max_played_in_loc[self.preference_order[i]] for i in range(len(self.preference_order))]

    # reinitializes the match with 2 new teams
    def update(self, team1, team2):
        self.teams = [team1, team2]
        max_played_in_loc = [max(team1.sides[i], team2.sides[i]) for i in range(num_sim_matches)]
        min_played_in_loc = [min(team1.sides[i], team2.sides[i]) for i in range(num_sim_matches)]
        self.preference_order = sorted(range(num_sim_matches), key=lambda i: (max_played_in_loc[i], min_played_in_loc[i]))
        self.min_matches_at_loc = [min_played_in_loc[self.preference_order[i]] for i in range(len(self.preference_order))]
        self.max_matches_at_loc = [max_played_in_loc[self.preference_order[i]] for i in range(len(self.preference_order))]

'''
Initializes the team list with the teams in.
'''
def init_teams():
    team_list = [Team(i + 1) for i in range(num_teams)]
    for team in team_list:
        for i in range(num_teams):
            if i + 1 != team.team_number:
                team.not_played.append(i + 1)

    return team_list

'''
Makes a match with the following priorities:
1. Number of consecutive games a team has been off
2. Number of consecutive games a team has played
3. Total number of games a team has played
4. Number of the team for first game (so that the first match is always teams 1v2, 3v4, 5v6)
and random thereafter
'''
def make_match(team_list, first_match=False):
    matches = []
    sorted_teams = sorted(team_list, key = lambda team: (-team.consecutive_off, team.consecutive_games, team.matches_played, team.team_number if first_match else random()))
    teams_picked = []

    # Finds the best opponent for the team input
    def find_opponent(team):
        for team2 in sorted_teams:
            if team2.team_number in team.not_played and not team2 in teams_picked and team2.team_number != team.last_team_played:
                # adds a new match class holding both of the teams
                matches.append(Match(team, team2))
                teams_picked.append(team)
                teams_picked.append(team2)
                return
    attempts = 0
    while len(matches) < num_sim_matches:
        for team in sorted_teams:
            if not team in teams_picked:
                find_opponent(team)        

            if len(matches) == num_sim_matches:
                return matches

        # reshuffles the teams so that they're in a different order
        matches = []
        teams_picked = []
        sorted_teams = sorted(team_list, key = lambda team: (-team.consecutive_off, team.consecutive_games, team.matches_played, team.team_number if first_match else random()))
        attempts += 1
        # after 20 attempts, the requirement that matches cannot be repeated is lifted, as it is assumed that the 
        if attempts == 20:
            for team in team_list:
                team.last_team_played = 0

        # if the algorithm was unable to make enough matches and there aren't enough potential matches in terms of 
        # teams which haven't played each other, it restarts the table by saying that no team has played any other 
        # (i.e adding each team to the list of teams not played on every other team)
        potential_matches = 0
        for team in sorted_teams:
            potential_matches += len(team.not_played)
        # after 20 attempts, it assumes that the problem with finding matches is that there is no possible configuration which allows teams 
        # to play teams it hasn't previously played
        if potential_matches <= 2 * num_sim_matches or attempts > 10:
            for team in sorted_teams:
                for i in range(len(sorted_teams)):
                    if sorted_teams[i].team_number != team.team_number:
                        team.not_played.append(sorted_teams[i].team_number)


'''
Logic to even out how often each team plays on a side
'''
def even_sides(matches):
    sides_given = [0 for i in range(len(matches))]
    while 0 in sides_given:
        # giving sides is prioritized based off the total number of times the teams have played on the side... The teams which have played on their 
        # first choice side collectively the least number of times are given their first choice, then the side and team is removed and the process is repeated.
        min_score = 1000
        min_index = 0
        min_loc = 0
        for i in range(len(matches)):
            score = matches[i].min_matches_at_loc[0] + matches[i].max_matches_at_loc[0]
            if score < min_score:
                min_index = i
                min_score = score
                min_loc = matches[i].preference_order[0]

        # allocates the side to the match with the lowest score
        sides_given[min_loc] = matches[min_index]

        # removes the match with the side allocated from the matches list
        matches.pop(min_index)

        # removes that side from the list of available sides
        for match in matches:
            location_index = match.preference_order.index(min_loc)
            match.preference_order.pop(location_index)
            match.min_matches_at_loc.pop(location_index)
            match.max_matches_at_loc.pop(location_index)
    return sides_given


'''
Changes the number of teams playing and/or the number of sides they are playing on
'''
def change_team_num(team_list, sides, next_sides, removed_teams, time_remaining):
    # class to hold a multiple choice question, its possible answers and what should happen after each of the answers
    class QuestionNode:
        def __init__(self, question, answers):
            self.type = 'q'
            self.question = question
            self.answers = answers
            self.children = []

        def get_answer_node(self):
            answer = display_module.draw_question_box(self.question, self.answers)
            if answer == 'quit' or answer == 'exit':
                return answer
            return self.children[self.answers.index(answer)]

    # class to hold points which are at the end of a chain of questions. They hold the function which should be executed at this point.
    class AnswerNode:
        def __init__(self, answer_function):
            self.type = 'a'
            self.answer_function = answer_function

    # changes the number of matches played at the same time
    def change_sides(team_list, removed_teams):
        global num_sim_matches
        original_num_sim_matches = num_sim_matches
        params = {'Number of sides': num_sim_matches}
        param_min_max = {'Number of sides': [1, num_teams//2]}
        exit, quit = display_module.draw_arrow_box(params, param_min_max)
        num_sim_matches = params['Number of sides']

        # once the number of sides has been changed, the sides that each team has played on becomes irrelevant, so we start again from scratch
        if not exit and not quit and original_num_sim_matches != num_sim_matches:
            for team in team_list:
                team.sides = [0 for i in range(num_sim_matches)]
            for team in removed_teams:
                team.sides = [0 for i in range(num_sim_matches)]
        return exit, quit
    
    # removes a team from the team list
    def remove_team(team_list, removed_teams):
        global num_teams
        exit = False
        quit = False
        answers = []

        # sorts the number of teams in order of team number, so they are displayed in order
        sorted_teams = sorted(team_list, key=lambda team: team.team_number)
        for team in sorted_teams:
            answers.append(str(team.team_number))

        # gets the user input as to which team they would like to remove
        answer = display_module.draw_question_box(['Which team', 'would you like to remove?'], answers)

        # if the user has quit or exited the question box, performs these actions
        if answer == 'quit':
            quit = True
        elif answer == 'exit':
            exit = True
        # if an answer has been selected, removes that team from the team list and adds it to the list of removed teams
        elif answer in answers:
            for i in range(len(team_list)):
                if int(answer) == team_list[i].team_number:
                    removed_teams.append(team_list[i])
                    team_list.pop(i)
                    num_teams -= 1
                    break
        return exit, quit

    # replaces a team that was previously removed from the list
    def add_removed_team(team_list, removed_teams):
        global num_teams
        exit = False
        quit = False
        answers = []

        # sorts the number of teams in order of team number so that they are displayed in order
        sorted_teams = sorted(removed_teams, key= lambda team: team.team_number)
        for team in sorted_teams:
            answers.append(str(team.team_number))

        # asks the user which team they would like to put back in
        answer = display_module.draw_question_box(['Which team', 'would you like to replace?'], answers)

        # if the user has quit or exited the question box, performs these actions
        if answer == 'quit':
            quit = True
        elif answer == 'exit':
            exit = True
        # if an answer has been selected, replaces that team from the removed teams and adds it to the team list
        elif answer in answers:
            for i in range(len(removed_teams)):
                if int(answer) == removed_teams[i].team_number:
                    team_list.append(removed_teams[i])
                    removed_teams.pop(i)
                    num_teams += 1
                    break
        return exit, quit

    # adds a new team to the end of the list.
    def add_team_to_end(team_list, removed_teams):
        global num_teams
        num_teams += 1

        # the new team number is one more than the current maximum (including teams which were previously removed)
        try:
            new_team_number = max(max(team.team_number for team in team_list), max(team.team_number for team in removed_teams)) + 1
        except ValueError:
            new_team_number = max(team.team_number for team in team_list) + 1

        # creates the new team and adds the fact that it hasn't played any other teams yet, before adding it to the team list
        new_team = Team(new_team_number)
        for team in team_list:
            new_team.not_played.append(team.team_number)
            team.not_played.append(new_team_number)
        team_list.append(new_team)
        return False, False

    # creates a new set of current and next games with the new parameters
    def update_current_games(team_list, sides, next_sides):
        # removes the previous updates to the team stats from the current game
        update_teams(team_list, sides, add=False)

        # adds the new current matches
        matches = make_match(team_list)
        sides = even_sides(matches)
        update_teams(team_list, sides, add=True)

        # adds the new upcoming matches
        matches = make_match(team_list)
        next_sides = even_sides(matches)

        return sides, next_sides

    # creates a new set of next games with the new parameters
    def update_next_games(team_list, sides, next_sides):
        # adds the new upcoming games
        matches = make_match(team_list)
        next_sides = even_sides(matches)
        return sides, next_sides

    quit = False

    # creates the node objects with the questions and the answer functions
    root_node = QuestionNode(['Are you looking to change the', 'number of teams or sides?'], ['Teams', 'Sides'])
    teams = QuestionNode(['Do you want to add a team', 'or remove a team?'], ['Add team', 'Remove team'])
    side_change = AnswerNode(change_sides)
    add_team = QuestionNode(['Do you want to add a team', 'that has already been removed?'], ['Yes', 'No'])
    remove = AnswerNode(remove_team)
    add_removed = AnswerNode(add_removed_team)
    add_to_end = AnswerNode(add_team_to_end)

    # connects the nodes through the 'children' list, which holds the nodes which can come from each node 
    root_node.children.append(teams)
    root_node.children.append(side_change)
    teams.children.append(add_team)
    teams.children.append(remove)
    add_team.children.append(add_removed)
    add_team.children.append(add_to_end)

    # adds the end node, which is the question which comes at the end of everything for each of the options
    end_node = QuestionNode(['Are you changing this for', 'this game set or the next?'], ['Current games', 'Next games'])
    if time_remaining[0] == display_module.game_time:
        current_games = AnswerNode(update_current_games)
    else:
        current_games = QuestionNode(['The clock is running on these games', 'are you sure you', 'want to change them?'], ['Yes', 'No, change next games'])
        current_games.children.append(AnswerNode(update_current_games))
        current_games.children.append(AnswerNode(update_next_games))
    next_games = AnswerNode(update_next_games)
    end_node.children.append(current_games) 
    end_node.children.append(next_games)

    # finds out what the user wants to do by going through the question tree
    next_node = root_node
    while next_node.type != 'a':
        next_node = next_node.get_answer_node()
        if next_node == 'quit':
            return sides, next_sides, True
        elif next_node == 'exit':
            return sides, next_sides, False
        elif next_node == add_team and len(removed_teams) == 0:
            next_node = add_to_end
        elif next_node == teams and len(team_list) <= 2 * num_sim_matches:
            next_node = QuestionNode(['Min number of teams reached.', 'Increase the nbr of teams', 'or decrease the nbr of sides?'], ['Increase nbr of teams', 'Decrease nbr of sides'])
            next_node.children.append(add_team)
            next_node.children.append(change_sides)

    # gets whether the changes should be applied to this set of matches or the next
    exit = False
    final_func = end_node.get_answer_node()
    if final_func == 'quit':
        quit = True
    elif final_func == 'exit':
        quit = False
        exit = True
    elif final_func.type == 'q':
        final_func = final_func.get_answer_node()
    if not quit and not exit:
        # runs the function which the user wants before getting a new set of matches
        exit, quit = next_node.answer_function(team_list, removed_teams)
        if not exit and not quit:
            sides, next_sides = final_func.answer_function(team_list, sides, next_sides)
    return sides, next_sides, quit


'''
Allows the user to change who is playing in the next few matches.
'''
def change_match(sides, next_sides, team_list, time_remaining):
    quit = False
    question = ['Are you changing this set of', 'matches or the next?']
    answers = ['This set', 'The next']
    answer = display_module.draw_question_box(question, answers)

    # set of instructions for changing the current set of matches
    if answer == answers[0]:
        if time_remaining[0] != display_module.game_time:
            question = ['The clock is running on these games', 'are you sure you want to', 'change them?']
            answers = ['Yes', 'No, change next games']
            answer = display_module.draw_question_box(question, answers)

        if answer == answers[0]:
            # gets the changes to the current matches that the user wants
            update_teams(team_list, sides, add=False)
            sides, quit = display_module.get_match_change(sides, team_list, num_sim_matches)
            update_teams(team_list, sides, add=True)

            # makes the next set of matches
            matches = make_match(team_list)
            next_sides = even_sides(matches)
    if answer == answers[1]:
        next_sides, quit = display_module.get_match_change(next_sides, team_list, num_sim_matches)
    elif answer == 'quit':
        quit = True

    return sides, next_sides, quit


'''
prints the matches out, given the list of sides for each match
'''
def print_matches(sides_given):
    for i in range(num_sim_matches):
        print(str(sides_given[i].teams[0].team_number) + 'v' + str(sides_given[i].teams[1].team_number), end=' ')
    print()


'''
Prints out the stats of what the teams have played so far.
'''
def print_stats(teams, removed_teams):
    new_list = teams + removed_teams
    sorted_list = sorted(new_list, key=lambda team: team.team_number)
    for team in sorted_list:
        print(team)

'''
Updates the display of the clock
'''
def update_clock(background_group, time_remaining):
    for item in background_group:
        if item.name == 'clock':
            item.update(time_remaining[0])


'''
Updates the values held within the team objects
team_list: list of all team objects
sides: list of the matches, ordered by the side they are playing on
add: True if we are updating the teams with the new games, False if we are undoing the action
'''
def update_teams(team_list, sides, add):
    for team in team_list:
        team_playing = False
        # if the team is playing, finds the opponent
        for i in range(len(sides)):
            if team == sides[i].teams[0]:
                team_playing = True
                opponent = sides[i].teams[1].team_number
                match_loc = i
            elif team == sides[i].teams[1]:
                team_playing = True
                opponent = sides[i].teams[0].team_number
                match_loc = i

        # adds/removes the new game to the stats of the team
        if add:
            if team_playing:
                team.add_game(opponent, match_loc)
            else:
                team.add_off()
        # adds/removes the fact that the team doesn't play in that round from its stats
        else:
            if team_playing:
                team.undo_add_game(opponent, match_loc)
            else:
                team.undo_add_off()


'''
Main function where most of the action happens
'''
def main():
    # sets up the initial variables
    team_list = init_teams()
    prev_sides = ['', '', '']
    removed_teams = []
    matches = make_match(team_list, first_match=True)
    sides = even_sides(matches)
    update_teams(team_list, sides, add=True)
    next_matches = make_match(team_list)
    next_sides = even_sides(next_matches)
    quit = False
    timer_running = [False]
    time_remaining = [display_module.game_time]
    background_group, button_group = display_module.create_sprites(num_teams, num_sim_matches)
    game_timer = threading.Thread(target=display_module.clock, args=(timer_running, time_remaining,))

    # loops while the user hasn't quit the program
    while not quit:
        # updates the display
        display_module.draw_screen(prev_sides, sides, next_sides, background_group, button_group)

        # loops until the game has ended, either by the timer running out or the user skipping the next game
        while time_remaining[0] > 0:
            # starts the clock if it isn't running but is meant to be
            if timer_running[0] and not game_timer.is_alive():
                game_timer = threading.Thread(target=display_module.clock, args=(timer_running, time_remaining,))
                game_timer.start()

            # updates the display
            update_clock(background_group, time_remaining)
            display_module.draw_screen(prev_sides, sides, next_sides, background_group, button_group)

            # checks if a button has been clicked
            button_clicked = display_module.get_button_click(button_group)
            if button_clicked:
                # play button sets the timer running
                if button_clicked == 'play':
                    timer_running[0] = True
                # pause button stops the timer from running
                elif button_clicked == 'pause':
                    timer_running[0] = False
                # skip button stops the timer from running and sets it to 0
                elif button_clicked == 'skip':
                    timer_running[0] = False
                    time_remaining[0] = 0
                # change button allows the user to change the number of teams and sides
                elif button_clicked == 'change':
                    # allows the user to change the number of teams and sides
                    sides, next_sides, quit = change_team_num(team_list, sides, next_sides, removed_teams, time_remaining)

                    # the text displaying the number of matches and teams is given by pygame sprites, which now need to be repaced with the new text
                    new_sprites = display_module.get_team_and_match_sprites(num_teams, num_sim_matches)
                    for item in background_group:
                        if item.name == 'matches' or item.name == 'teams' or item.name == 'change':
                            background_group.remove(item)
                    background_group.add(new_sprites)

                # restart button returns the user to the menu to restart the whole process
                elif button_clicked == 'restart':
                    # checks the user intended to restart the program
                    answer = display_module.draw_question_box(['Are you sure', 'you want to restart?'], ['Yes', 'No'])
                    if answer == 'Yes':
                        return False
                    elif answer == 'quit':
                        quit = True
                # allows the user to change the teams currently playing
                elif button_clicked == 'change match':
                    sides, next_sides, quit = change_match(sides, next_sides, team_list, time_remaining)
                # if the user quits, quits the program
                if button_clicked == 'quit' or quit:
                    answer = display_module.draw_question_box(['Are you sure', 'you want to quit?'], ['Yes', 'No'])
                    if answer == 'Yes' or answer == 'quit':
                        print_stats(team_list, removed_teams)
                        return True

        # updates all the values after a match has taken place
        update_clock(background_group, time_remaining)
        time_remaining[0] = display_module.game_time
        timer_running[0] = False
        prev_sides = sides
        sides = next_sides
        update_teams(team_list, sides, add=True)
        matches = make_match(team_list)
        next_sides = even_sides(matches)

    '''
    for i in range(num_total_matches):
        matches = make_match(team_list)
        sides_given = even_sides(matches)
        print_matches(sides_given)
    print_stats(team_list)
    '''

# calls the main function
if __name__ == '__main__':
    quit_code = False
    while not quit_code:
        num_teams, num_sim_matches, quit_code = display_module.menu()
        if not quit_code:
            quit_code = main()
