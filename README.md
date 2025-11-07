# Alts Code
*Hello! This is the code for the Oxford Alternative Ice Hockey Club (Alts).*

For those of you just looking through my GitHub unfamiliar with Alts, some background:
Alts is a biweekly event at the Oxford ice rink where people turn up, pay for entry, and play casual hockey. 
Players are split into teams of 6, which play each other in small, friendly 3 minute games across the rink. Each team is given a number at the start of the session, and there are usually between 15-25 teams.
The rink is usually split into 3 matches, one in each of the end zones and one between the blue lines, but on occasion when there are fewer people the ice is split into 2 matches instead.

The aim of this program is to match teams so that:
1. They all get the same amount of ice time
2. They all spend the same amount of time on each part of the rink (the centre of the ice is known for being much more chopped up and worse to skate on)
3. The first set of games is always teams 1vs2, 3vs4, 5vs6, and so on, because this makes everyone's life easier.

Additional features I've added to make it easier for the committee (the program this is replacing didn't have these features, or feature 2 above come to think of it):
1. Add/remove teams mid-session (for early departures and late arrivals)
2. Change the number of pads being played on (noted "number of sides", allows future committees to try experimental numbers of pads)
3. Edit current and future games (allowing for requests from players which want to play particular teams)
4. Timer to time the games being played, with play and pause buttons in case of necessity.
5. Skip button to skip a match or go to the next match.

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
- not_played: List of the team numbers which have not yet been played
- matches_played: Number of matches played
- sides: Number of times each pad (noted side throughout, I unfortunately cannot be bothered to change it to better terminology) has been played on by the team
- team_number: Number of the team (i.e, the number that gets called out over the mic when this team plays)
- consecutive_games: Number of consecutive games this team has been on the ice. (Used for prioritising teams to play next)
- consecutive_off: Number of consecutive games this team has been off the ice. (Used for prioritising teams to play next)
- max_consec: Maximum number of consecutive games this team has played. (Currently only used for debugging purposes)
- max_off: Maximum number of consecutive games this team has been off the ice. (Currently only used for debugging purposes)
- last_team_played: Last team played by this team (Used for avoiding playing the same team twice in a row once all teams have played each other)

Previous variables (used for undoing actions):
- prev_consec: Value of consecutive_games at the previous iteration (i.e after the previous set of games, what was the value of consecutive_games?)
- prev_off: Value of consecutive_off at the previous iteration
- prev_max_consec: Value of max_consec at the previous iteration
- prev_max_off: Value of max_off at the previous iteration
- prev_last_team_played: value of last_team_played at the previous iteration

#### Functions
- add_game(opponent, loc): Updates the team with a match against opponent (team number of said opponent) at loc (0, 1 or 2 if there are 3 sides being played on)
- add_off: Updates the team with a period off the ice
- undo_add_game(opponent, loc): Undoes add_game
- undo_add_off: Undoes add_off
- str: Turns the information about a team into the string. Used for interest and/or debugging purposes


### Match Class
Match(team1, team2): Creates an instance of the match class, representing a match between team1 and team2
#### Variables
- teams: List of teams participating in the match. Each team is an instance of the Team class.
- preference_order: Ordered preferences of locations to play (e.g [2, 0, 1], if these teams playing on pad 2 is preferable, and playing on pad 1 is unwanted). Preferences are determined by number of times the teams have played on each pad.
- min_matches_at_loc: Lesser of the number of matches played at each location between the 2 teams, ordered by preference order.
  (e.g, team 1 has played [1, 0, 3] games on pads 0, 1, 2. team 2 has played [2, 2, 0]. Preference order is [1, 0, 2] in this situation.  min_matches_at_loc[0] = smaller number of games played at preference_order[0], between team 1 and 2.
  Preference_order[0] is 1, and team 1 played 0 games at location 1. team 2 played 2 games, so the minimum is team 1's 0. min_matches_at_loc[0] would therefore be 0 and the full array would be [0, 1, 0].
- max_matches_at_loc: Same as above, but maximum value. In the example, max_matches_at_loc = [2, 2, 3]

Note min, max_matches_at_loc are somewhat messy as variables, but they make the code for getting the teams in the right locations a fair amount simpler.
  
#### Functions
- update(team1, team2): Reinitialises the match with 2 different teams
- location_unavailable(location): updates the preference order, min, max_matches_at_loc with the information that the match can no longer be played at location.

## Global Functions
[UNFINISHED, will continue soon]
