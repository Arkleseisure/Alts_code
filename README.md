# Alts Code
*Hello! This is the code for the Oxford Alternative Ice Hockey Club (Alts).*

For those of you just looking through my GitHub unfamiliar with Alts, some background:
Alts is a biweekly event at the Oxford ice rink where people turn up, pay for entry, and play casual hockey. 
Players are split into teams of 6, which play each other in small, friendly 3 minute games across the rink. Each team is given a number at the start of the session, and there are usually between 15-25 teams.
The rink is usually split into 3 pads, one in each of the end zones and one between the blue lines, each containing one match between 2 teams. On occasion when there are fewer people the ice is split into 2 pads instead.

The aim of this program is to match teams so that:
1. They all get the same amount of ice time
2. They all spend the same amount of time on each part of the rink (the centre of the ice is known for being much more chopped up and worse to skate on)
3. The first set of games is always teams 1vs2, 3vs4, 5vs6, and so on, because this makes everyone's life easier.

Additional features I've added to make it easier for the committee (the program this is replacing didn't have these features - or feature 2 above come to think of it):
1. Add/remove teams mid-session (for early departures and late arrivals)
2. Change the number of pads being played on (in the system this is called "number of sides", allows future committees to try different setups with e.g 6 simultaneous matches between smaller teams)
3. Edit current and future games (allowing for requests from players which want to play particular teams)
4. Timer to time the games being played, with play and pause buttons in case of necessity.
5. Skip button to skip a match or go to the next match.

For anyone just interested in how the matching process works, have a look at the documentation for the "make_match" function, under the Global Functions header below. If interested in how it's ensured that different teams end up playing on each part of the rink approximately the same amount, look at the "even_sides" function, under the same header.

# Docs
For Altsers who want to improve the code, it may be a good idea to familiarise yourself with the working of the code here.
The logic for the system is in "Alts_code.py", while the stuff for the pygame display is in "display_module.py". If you just want to download and run the code, you can do this on Windows by downloading and running "Alts_code.exe". 
People not on Windows have to sort their life out (and probably find a way to run the base python files, which shouldn't be too hard hopefully).
The pngs are just the images used in the code - you can see them for yourself by clicking on them.

If you want to turn the whole code into an exe, I think I used the package buildozer, although nowadays I would definitely just ask ChatGPT to figure that bit out for me.

## Classes
There are 2 major classes in the code: the team class and the match class

Instances of the team class hold information about a team with a particular team number. 
For instance, the instance for team no 9 would store information such as "games_played = 5" (team 9 has played 5 games),
"not_played = [2, 5, 6]" (team 9 has not yet played teams 2, 5 or 6), and "consecutive_off = 2" (team 9 has been off for 2 consecutive games)

The Match class holds 2 teams and information about where those teams would prefer to play.
Information includes things like "self.teams = [team1, team2]", where team1 and team2 are instances of the team class.

### Team Class
Team(number): Creates an instance of the team class with team_number = number
#### Variables
Main variables:
- not_played - list(int): List of the team numbers which have not yet been played
- matches_played - int: Number of matches played
- sides - list(int): Number of times each pad (noted side throughout, I unfortunately cannot be bothered to change it to better terminology) has been played on by the team
- team_number - int: Number of the team (i.e, the number that gets called out over the mic when this team plays)
- consecutive_games - int: Number of consecutive games this team has been on the ice. (Used for prioritising teams to play next)
- consecutive_off - int: Number of consecutive games this team has been off the ice. (Used for prioritising teams to play next)
- max_consec - int: Maximum number of consecutive games this team has played. (Currently only used for debugging purposes)
- max_off - int: Maximum number of consecutive games this team has been off the ice. (Currently only used for debugging purposes)
- last_team_played - int: Last team played by this team (Used for avoiding playing the same team twice in a row once all teams have played each other)

Previous variables (used for undoing actions):
- prev_consec - int: Value of consecutive_games at the previous iteration (i.e after the previous set of games, what was the value of consecutive_games?)
- prev_off - int: Value of consecutive_off at the previous iteration
- prev_max_consec - int: Value of max_consec at the previous iteration
- prev_max_off - int: Value of max_off at the previous iteration
- prev_last_team_played - int: value of last_team_played at the previous iteration

#### Functions
- add_game(opponent, loc) -> None: Updates the team with a match against opponent (team number of said opponent) at loc (0, 1 or 2 if there are 3 sides being played on)
- add_off() -> None: Updates the team with a period off the ice
- undo_add_game(opponent, loc) -> None: Undoes add_game
- undo_add_off() -> None: Undoes add_off
- str() -> str: Turns the information about a team into the string. Used for interest and/or debugging purposes


### Match Class
Match(team1, team2): Creates an instance of the match class, representing a match between team1 and team2
#### Variables
- teams - list(Team): List of teams participating in the match. Each team is an instance of the Team class.
- preference_order - list(int): Ordered preferences of locations to play (e.g [2, 0, 1], if these teams playing on pad 2 is preferable, and playing on pad 1 is unwanted). Preferences are determined by number of times the teams have played on each pad.
- min_matches_at_loc - list(int): Lesser of the number of matches played at each location between the 2 teams, ordered by preference order.
  (e.g, team 1 has played [1, 0, 3] games on pads 0, 1, 2. team 2 has played [2, 2, 0]. Preference order is [1, 0, 2] in this situation.  min_matches_at_loc[0] = smaller number of games played at preference_order[0], between team 1 and 2.
  Preference_order[0] is 1, and team 1 played 0 games at location 1. team 2 played 2 games, so the minimum is team 1's 0. min_matches_at_loc[0] would therefore be 0 and the full array would be [0, 1, 0].
- max_matches_at_loc - list(int): Same as above, but maximum value. In the example, max_matches_at_loc = [2, 2, 3]

Note min, max_matches_at_loc are somewhat messy as variables, but they make the code for getting the teams in the right locations a fair amount simpler.
  
#### Functions
- update(team1, team2) -> None: Reinitialises the match with 2 different teams
- location_unavailable(location) -> None: updates the preference order, min, max_matches_at_loc with the information that the match can no longer be played at location.

## Global Variables
### num_teams - int
This is the total number of teams currently playing. The variable is set at the menu at the start and updated when teams are added or removed.
### num_sim_matches - int
This is the number of games occurring at any one time. Elsewhere in this document I have referred to this as the "number of pads" or the "number of sides". In a standard alts session it will be 3, or 2 if playing half ice. The code is built to work with any number of pads however (although the display starts to break at around 10 or 11). I imagine there could be a fun session in the future with e.g teams of 3 and the ice split into 6 (although we would need extra cones and ways to make goals).
### quit_code - bool
This is a simple variable which holds whether the user decided to exit the program via the cross at the top right.

## Global Functions
### init_teams() -> list(Team)
Creates a list of teams with numbers from 1 to num_teams

### make_match(team_list : list(Team), first_matches=False) -> list(Match)
Creates a list of num_sim_matches matches. 

For the matching process, the teams are first ordered by priority. The priority is determined by:
1. Most consecutive games off the ice
2. Lowest number of consecutive games played
3. Lowest number of total games
4. team_number if first_matches=True, otherwise random

At the time of writing, first_matches is set to True if there is any team which has not yet played any games (although it stays False if a team is added after all other teams have played a game).

Once the priority list is made, the first team in the list is paired with the next team in the priority list that it has not yet played. Both are set aside and the process is repeated until all games are complete.

If this fails, as is possible under certain circumstances, the randomisation in step 4 of the priority order is repeated and the process as a whole is redone.

If this repeatedly fails, or there aren't enough possible matches left to fill the remaining slots, it is assumed that all teams have played each other. Each team's not_played list is refilled with all possible opponents. Teams are prevented from playing each other twice in a row with a "last_team_played" variable, which is removed if attempts continue to fail (This could happen in e.g a simple scenario where there are 2 teams which are repeatedly playing each other on full ice).

### even_sides(matches: list(Match)) -> list(Match)
Function which takes in a list of matches generated by make_match, and allocates them to pads which the teams have played on a minimum amount.

It is explained in the Match class how min_matches_at_loc, max_matches_at_loc and preference_order work. We will not repeat it here, but the upshot of the code is that the match whose teams have played the lowest number of combined games on their first preference pad get their first preference. This pad is removed from the other matches' preference order and the process is repeated.

### change_team_num(team_list: list(Team), sides: list(Match), next_sides: list(Match), removed_teams: list(Team), time_remaining: list(float)) -> sides: list(Match), next_sides: list(Match), quit: bool
Adds/removes teams from the system or changes the number of sections in the rink (e.g changes the rink from third ice to half ice). Looking back on this now, I think the function could definitely be improved in terms of clarity for the end user - I would recommend someone looking to improve the software try to get this into a shape where there isn't this weird maze of choices to go through just to add another team. Also note that time_remaining is a list of 1 float, with the reason being that lists are mutable, so you can change the value in another thread and it will change instantly while you're doing something else in another funtion.

The main logic for this is implemented via Question and Answer nodes, with question nodes routing through different possibilities for what the user wants to do and answer nodes containing the function to be executed at the end of different chains of logic.

QuestionNode(question, answers) has 4 attributes: self.type, self.question, self.answers, self.children. self.type='q' denotes it is a question, not an answer node. self.question is a text question as it should be passed to the user, but broken down into sections as it should be formatted. self.answers is a multiple choice list of answers to the question and self.children is a list of the nodes those answers take you to.

example use: 

q = QuestionNode(["Do you prefer", "dogs or cats?"], ["dogs", "cats"])
q.children.append(display_dog, display_cat)

AnswerNode(answer_function) is called once the maze of QuestionNodes has been navigated. It contains a link to the function to be executed at different endpoints. It has attributes self.type='a', denoting it to be an answer node rather than a question node, and answer_function, which contains the function that should be called once that node is reached. The different functions called are:

- change_sides: Changes the number of pads the rink is split into, such as changing from third ice to half ice.
- remove_team: Removes a team from the system
- add_removed_team: Adds back a team that was previously removed
- add_team_to_end: Adds a new team to the system
- update_current_games: Updates the current set of games (the ones displayed in the middle of the screen) once the information has been changed.
- update_next_games: Updates the next set of games once the information has been changed.

The parameters of the first 4 are: (team_list: list(Team), removed_teams: list(Team)) -> exit: bool, quit: bool
And of the last 2: (team_list: list(Team), sides: list(Match), next_sides: list(Match)) -> sides: list(Match), next_sides: list(Match)
  
### change_match(sides: list(Match), next_sides: list(Match), team_list: list(Team), time_remaining: list(float)) -> sides: list(Match), next_sides: list(Match), quit: bool
Allows the user to change who is playing the next set of matches. 
Most of the functionality is contained within the display_module get_match_change function, but a few key things are done here:
- Checking whether the current or next set of matches is the set to be changed
- If it's the current set, checking whether the timer is running and warning the user if so
- Recomputing the next set of matches if the current set is changed
  
### print_matches(sides_given: list(Match)) -> None
Function to print a set of matches out (for e.g debugging purposes)

### print_stats(teams: list(Team), removed_teams: list(Team)) -> None
Function to print out the stats of the games played during a session. (for debugging or interest)

### update_clock(background_group: pygame.sprite.Group, time_remaining: list(float)) -> None
Function to update the display of the clock. Finds the clock sprite within the background group and then changes it to contain the current value of time_remaining (held in a list, which is mutable, so that any updates to it in another thread will affect everything else immediately).

### update_teams(team_list: list(Team), sides: list(Match), add: bool) -> None
Updates the teams after they have been added or removed from playing the current set of games. If add, then the stats from the new set of games are added, if not they are removed.

### main() -> quit: bool
Main function, which calls everything else. display_module.menu() is called first, so main has access to things like the number of teams and number of simultaneous matches. 
It uses this to set up the initial teams, matches, sides, etc.

It then loops through the following actions while the timer hasn't hit zero:
- Checking if the timer has started
- If it hasn't, and it should have, start timer.
- Update the display
- Checks if a button has been clicked
- If a button has been clicked, perform that action

Once the timer hits zero, the following is performed:
- Clock is reset
- Next set of matches becomes the current set of matches
- Checks if all teams have played their first match
- If so, first_matches is set to False, meaning the teams are no longer paired in order
- Next set of matches is generated
- Pause button on display is switched back to a play button

## Display module
