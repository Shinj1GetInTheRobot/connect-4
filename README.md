# comp3821-connect-four

## Version 2.0

- `generate.exe`
  - New binary for making `games.json` (replaces `games_generator.py`).
  - Old command:
    ```bash
    python3 games_generator.py filename always_center minimax_near_center -d2=4
    ```
    New command:
    ```bash
    ./generate.exe filename center center filename -d1=0 -d2=4
    ```
  - Patched bot names:
    - `random` + `minimax_none` -> now just `random`
    - `always_center` + `minimax_near_center` -> now just `center`
    - `always_high` + `minimax_far_up` -> now just `high`
    - `always_low` + `minimax_far_down` -> now just `low`
    - `always_left` + `minimax_far_left` -> now just `left`
    - `always_right` + `minimax_far_right` -> now just `right`

- `./game_data`
  - Put your `.json` files in here.

- `./game_generation`
  - Raw code for the `generate.exe` binary.
  - You can recompile `game_generator.cpp` if you want to change the code.
  - Recompile:

    ```bash
    g++ -std=c++20 -O2 -march=native -Wall -Wextra game_generation/game_generator.cpp -o generate.exe
    ```

- `./game_simulation`
  - Raw CSS/JS code for index.html