# Alts Code

*Hello! This is the code for the **Oxford Alternative Ice Hockey Club (Alts)**.*

For those of you just looking through my GitHub unfamiliar with Alts, some background:
**Alts** is a biweekly event at the Oxford ice rink where people turn up, pay for entry, and play casual hockey.
Players are split into teams of 6, which play each other in small, friendly 3-minute games across the rink. Each team is given a number at the start of the session, and there are usually between 15–25 teams.
The rink is usually split into 3 **rink sections** (or **pads**), one in each of the end zones and one between the blue lines, each containing one match between 2 teams. On occasion when there are fewer people the ice is split into 2 pads instead.

The aim of this program is to match teams so that:
1. They all get the **same amount of ice time**.
2. They all spend the **same amount of time on each part of the rink** (the center of the ice is known for being much more chopped up and worse to skate on).
3. The first set of games is always teams **1v2, 3v4, 5v6**, and so on, because this makes everyone's life easier.

Additional features I've added to make it easier for the committee (the program this is replacing didn't have these features—or feature 2 above come to think of it):
1. **Add/remove teams mid-session** (for early departures and late arrivals).
2. **Change the number of pads** being played on (in the system this is called "**number of sides**," allows future committees to try different setups with e.g., 6 simultaneous matches between smaller teams).
3. **Edit current and future games** (allowing for requests from players which want to play particular teams).
4. **Timer** to time the games being played, with play and pause buttons in case of necessity.
5. **Skip button** to skip a match or go to the next match.

For anyone just interested in how the matching process works, have a look at the documentation for the **`make_match`** function, under the Global Functions header below. If interested in how it's ensured that different teams end up playing on each part of the rink approximately the same amount, look at the **`even_sides`** function, under the same header.

***

# Docs

For Altsers who want to improve the code, it may be a good idea to familiarise yourself with the working of the code here.
The logic for the system is in **`Alts_code.py`**, while the stuff for the **Pygame display** is in **`display_module.py`**. If you just want to download and run the code, you can do this on Windows by downloading and running "**`Alts_code.exe`**".
People not on Windows have to sort their life out (and probably find a way to run the base python files, which shouldn't be too hard hopefully).
The pngs are just the images used in the code—you can see them for yourself by clicking on them.

If you want to turn the whole code into an exe, I think I used the package buildozer, although nowadays I would definitely just ask ChatGPT to figure that bit out for me.

## Classes

There are 2 major classes in the code: the **`Team`** class and the **`Match`** class.

Instances of the **`Team`** class hold information about a team with a particular team number.
For instance, the instance for team no 9 would store information such as "**`matches_played = 5`**" (team 9 has played 5 games),
"**`not_played = [2, 5, 6]`**" (team 9 has not yet played teams 2, 5 or 6), and "**`consecutive_off = 2`**" (team 9 has been off for 2 consecutive games).

The **`Match`** class holds 2 teams and information about where those teams would prefer to play.
Information includes things like "**`self.teams = [team1, team2]`**", where `team1` and `team2` are instances of the **`Team`** class.

### Team Class

`Team(number)`: Creates an instance of the **`Team`** class with `team_number = number`.

#### Variables

**Main variables:**
* **`not_played`** - `list(int)`: List of the team numbers which have not yet been played.
* **`matches_played`** - `int`: Number of matches played.
* **`sides`** - `list(int)`: Number of times each **rink section** (noted `side` or `loc` in the code) has been played on by the team.
* **`team_number`** - `int`: Number of the team.
* **`consecutive_games`** - `int`: Number of consecutive games this team has been on the ice.
* **`consecutive_off`** - `int`: Number of consecutive games this team has been off the ice.
* **`max_consec`** - `int`: Maximum number of consecutive games this team has played.
* **`max_off`** - `int`: Maximum number of consecutive games this team has been off the ice.
* **`last_team_played`** - `int`: Last team played by this team (Used for avoiding playing the same team twice in a row).

**Previous variables (used for undoing actions):**
* **`prev_consec`**, **`prev_off`**, **`prev_max_consec`**, **`prev_max_off`**, **`prev_last_team_played`**: Stores the value of the corresponding main variable from the previous iteration.

#### Functions

* **`add_game(opponent, loc)`** -> `None`: Updates the team with a match against `opponent` at `loc` (the index of the rink section).
* **`add_off()`** -> `None`: Updates the team with a period off the ice.
* **`undo_add_game(opponent, loc)`** -> `None`: Undoes `add_game`. Includes a check to prevent errors if the number of pads (`num_sim_matches`) was recently changed.
* **`undo_add_off()`** -> `None`: Undoes `add_off`.
* **`__str__()`** -> `str`: Returns a string summary of the team's statistics.

### Match Class

`Match(team1, team2)`: Creates an instance of the **`Match`** class.

#### Variables

* **`teams`** - `list(Team)`: List of teams participating in the match.
* **`preference_order`** - `list(int)`: Ordered preferences of locations to play. Determined by which location minimizes the total number of games played there by *either* team.
* **`min_matches_at_loc`** - `list(int)`: The **lesser** of the number of matches played at each location, ordered by the `preference_order`.
* **`max_matches_at_loc`** - `list(int)`: The **greater** of the number of matches played at each location, ordered by the `preference_order`.

> **Conceptual Note:** These ordered lists (`min_matches_at_loc` and `max_matches_at_loc`) facilitate the `even_sides` algorithm by quickly providing the spread of location usage between the two teams at their most preferred spots.

#### Functions

* **`update(team1, team2)`** -> `None`: Reinitialises the match with 2 different teams.
* **`location_unavailable(location)`** -> `None`: Updates the preference lists with the information that the match can no longer be played at `location`.

***

## Global Variables

* **`num_teams`** - `int`: The total number of teams currently playing.
* **`num_sim_matches`** - `int`: The number of games occurring at any one time (number of pads/rink sections).
* **`quit_code`** - `bool`: Holds whether the user chose to exit the program.
* **`game_time`** - `int` (in `display_module.py`): The length, in seconds, of a single match (default is **180**).

***

## Global Functions (`Alts_code.py`)

### `init_teams`
*Input*: None
*Output*: `list(Team)`: Creates a list of teams.

### `make_match`
*Input*: (`team_list`: `list(Team)`, `first_matches=False`)
*Output*: `list(Match)`: Creates a list of `num_sim_matches` matches.
* **Priority Order:** Teams are sorted by: 1) Most `consecutive_off`, 2) Lowest `consecutive_games`, 3) Lowest `matches_played`, 4) random (or `team_number`, if `first_matches=True`).
* **Pairing logic:** The highest-priority team is paired with the next highest team it hasn't played yet. These teams are removed from the order and the same operation is repeated for each of the next matches.
* **Retry/Reset Logic:** If the algorithm fails after **10 attempts** to create the required matches, the `not_played` lists are reset to ensure a continuous schedule. If still unsuccessful after **20 attempts** the `last_team_played` constraint is lifted.

### `even_sides`
*Input*: (`matches`: `list(Match)`)
*Output*: `list(Match)`: Allocates a pad to each match to balance location usage.
* **Logic:** The match whose teams have played the lowest number of **combined games** on their first preference pad is allocated that pad first.

### `change_team_num`
*Input*: (`team_list`: `list(Team)`, `sides`: `list(Match)`, `next_sides`: `list(Match)`, `removed_teams`: `list(Team)`, `time_remaining`: `list(float)`)
*Output*: `sides`: `list(Match)`, `next_sides`: `list(Match)`, `quit`: `bool`
* **Purpose:** Manages adding/removing teams or changing the number of pads. Implemented using a decision tree of **`QuestionNode`** and **`AnswerNode`** objects.
> **Note on `time_remaining`:** This is passed as a mutable `list` containing a single float (e.g., `[180.0]`) to allow the timer thread to update the value instantly across the main application.

### `change_match`
*Input*: (`sides`: `list(Match)`, `next_sides`: `list(Match)`, `team_list`: `list(Team)`, `time_remaining`: `list(float)`)
*Output*: `sides`: `list(Match)`, `next_sides`: `list(Match)`, `quit`: `bool`
* **Purpose:** Allows the user to manually change teams in the current or next match set.

### Other Utilities
* **`print_matches`**: Prints a set of matches for debugging.
* **`print_stats`**: Prints final team statistics, including standard deviation of games played per side.
* **`update_clock`**: Updates the clock sprite on the display.
* **`update_teams`**: Updates team statistics based on a set of completed or scheduled matches.

### `main`
*Input*: `None`
*Output*: `quit`: `bool`: The core scheduling loop.

***

## Display module (`display_module.py`)

This file handles all graphical elements and user input using the **Pygame** library. 

### Classes

#### `RectangleSprite(pygame.sprite.Sprite)`
The base class for all rectangular display elements (backgrounds, labels, buttons).

* **Features:** Renders a colored background, handles centering/alignment, and renders text and/or an image asset.

#### `Button(RectangleSprite)`
A subclass for interactive buttons.

* **`is_clicked(x, y)`**: Checks collision with mouse coordinates.
* **`show_highlights()`/`unshow_highlights()`**: Draws/removes a border around the button when clicked, providing visual feedback.

#### `Clock(RectangleSprite)`
Displays the countdown timer.

* **`get_text(time_remaining)`**: Formats seconds into "MM:SS" string.
* **`update(time_remaining)`**: Redraws the clock face with the latest time.

### Functions

#### `print_screen(...)`
A utility to draw text onto any Pygame surface.

#### `get_team_and_match_sprites(num_teams, num_sides)`
Creates the static text displaying the current number of teams and matches in the top-right corner.

#### `create_sprites(num_teams, num_sides)`
Sets up the main session screen elements:
* **`background_group`**: Static elements (highlights, clock, team counts).
* **`button_group`**: Interactive elements (`play`, `skip`, `change`, etc.).

#### `get_button_click(button_group, down_click=False)`
*Input*: `button_group`, `down_click`
*Output*: `str` (name of button clicked, 'quit', or `False`)

The main input polling function, which detects button clicks and handles highlight states.

#### `draw_question_box(question, answers)`
*Input*: `question`: `list(str)`, `answers`: `list(str)`
*Output*: `str` (the answer clicked)

Draws a modal window for multiple-choice questions.

#### `draw_arrow_box(params, param_min_max)`
*Input*: `params`: `dict`, `param_min_max`: `dict`
*Output*: `exited`: `bool`, `quit`: `bool`

Draws a modal window with up/down arrows to modify numeric parameters within set minimum/maximum bounds.

#### `get_match_change(sides, team_list, num_sim_matches)`
*Input*: `sides`: `list(Match)`, `team_list`: `list(Team)`, `num_sim_matches`: `int`
*Output*: `sides`: `list(Match)`, `quit`: `bool`

Allows the user to manually rearrange teams in the match schedule using drag-and-drop functionality:
* **`drag(button)`**: Local function that handles moving a button with the mouse while clicked down, ensuring it stays within the boundary box.
* The function manages the interface for manually selecting and swapping teams in the match slots.
