import json

def parse_quake_log(file_path):
    games_data = []
    current_game = None
    game_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line is a new game start line (e.g., "InitGame")
            if "InitGame" in line:
                if current_game:
                    # Finish current game
                    games_data.append(current_game)
                # Start a new game
                game_count += 1
                current_game = {
                    "game": game_count,
                    "status": {
                        "total_kills": 0,
                        "players": {}
                    }
                }

            # Parse kill event lines
            if "Kill:" in line:
                parts = line.split()
                killer_id = int(parts[2])
                victim_id = int(parts[3])
                # Extract the killer and victim names
                killer_name = parts[6] if killer_id != 1022 else "<world>"
                victim_name = parts[7]

                # Update the total kills count
                current_game["status"]["total_kills"] += 1

                if killer_name == "<world>":
                    # World kills a player
                    # Decrease the victim's kill count by 1
                    if victim_name in current_game["status"]["players"]:
                        current_game["status"]["players"][victim_name] -= 1
                else:
                    # A player kills another player
                    # Increase the killer's kill count
                    if killer_name in current_game["status"]["players"]:
                        current_game["status"]["players"][killer_name] += 1
                    else:
                        current_game["status"]["players"][killer_name] = 1

                # Decrease the victim's kill count by 1
                if victim_name in current_game["status"]["players"]:
                    current_game["status"]["players"][victim_name] -= 1
                else:
                    current_game["status"]["players"][victim_name] = -1

        # Add the last game data if it exists
        if current_game:
            games_data.append(current_game)

    # Transform the data into the desired output format
    parsed_data = []
    for game in games_data:
        game_dict = {
            "game": game["game"],
            "status": {
                "total_kills": game["status"]["total_kills"],
                "players": []
            }
        }
        for player, kills in game["status"]["players"].items():
            game_dict["status"]["players"].append({
                "nome": player,
                "kills": kills
            })
        parsed_data.append(game_dict)

    return parsed_data


# Sample usage
file_path = "../Quake.txt"
parsed_data = parse_quake_log(file_path)
print(json.dumps(parsed_data, indent=4))
