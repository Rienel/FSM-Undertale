#This is the original/Main code for the Model

class GameFSM:
    def __init__(self):
        self.state = "Game Start State"
        self.route = None
        self.health = 100
        self.max_health = 100
        self.enemies = [{"name": "Centaur", "health": 50, "status": "alive"},
                        {"name": "Minotaur", "health": 50, "status": "alive"}]
        self.respawned = False

    # Player respawns, reset health
    def reset_health(self):
        self.health = self.max_health
        print("Player respawned. Health reset to 100.")
        
        self.enemies = [
            {"name": "Centaur", "health": 50, "status": "alive"},
            {"name": "Minotaur", "health": 50, "status": "alive"}
        ]
        
        self.state = "Fight State"
        self.respawned = True

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"Player healed! Health: {self.health}")

    # Player takes damage, if health = 0, state = Dead
    def damage(self, amount):
        self.health -= amount
        print(f"Player took {amount} damage! Health: {self.health}")
        if self.health <= 0:
            self.state = "Player Dies"
            print("Player has died!")

    def enemy_damage(self):
        self.damage(50)

    def slash_enemy(self, enemy_index):
        enemy = self.enemies[enemy_index]
        enemy["health"] -= 50
        if enemy["health"] <= 0:
            enemy["status"] = "defeated"
            print(f"{enemy['name']} has been defeated!")

    def spare_enemy(self, enemy_index):
        enemy = self.enemies[enemy_index]
        enemy["status"] = "spared"
        print(f"{enemy['name']} has been spared!")

    def check_all_slashed(self):
        return all(enemy["status"] == "defeated" for enemy in self.enemies)

    def check_all_spared(self):
        return all(enemy["status"] == "spared" for enemy in self.enemies)

    def check_all_slashed_or_spared(self):
        return all(enemy["status"] in ["defeated", "spared"] for enemy in self.enemies)

    # Start the transition
    def transition(self):
        if not self.respawned:
            self.route = input("Which route will you take?\n Pacifist Route/Genocide Route: ").strip()

            if self.state == "Game Start State":
                if self.route == "Pacifist Route":
                    self.state = "Pacifist Route State"
                elif self.route == "Genocide Route":
                    self.state = "Genocide Route State"
                else:
                    print("Invalid route. Please choose between Pacifist or Genocide Route.")
                    return

        # Entering Fight State
        print("\nAn Enemy Appears!")
        if self.state in ["Pacifist Route State", "Genocide Route State"]:
            self.state = "Fight State"

        while self.state == "Fight State":
            print(f"\nCURRENT HEALTH: {self.health}")
            print("\nPick between four options: \nFight\nAction\nItem\nMercy")
            action = input("Choose an action: ").strip()

            if action == "Fight":
                alive_enemies = [enemy for enemy in self.enemies if enemy["status"] == "alive"]
                
                if not alive_enemies:
                    print("No enemies are left to fight.")
                    break

                enemies_left = ", ".join([enemy["name"] for enemy in alive_enemies])
                target_enemy_name = input(f"Pick Enemy: {enemies_left}: ").strip()

                enemy_index = next((i for i, e in enumerate(self.enemies)
                                    if e["name"].lower() == target_enemy_name.lower() and e["status"] == "alive"), None)

                if enemy_index is None:
                    print("Invalid enemy name or enemy already defeated!")
                    continue

                player_slashes = input("Type 'slash' to attack the enemy: ").strip().lower()
                if player_slashes == "slash":
                    self.slash_enemy(enemy_index)

                    if any(e["status"] == "alive" for e in self.enemies):
                        self.enemy_damage()
                        if self.health <= 0:
                            self.reset_health()
                            return
                    else:
                        print("All enemies have been defeated!")
                        self.state = "Normal State"
                        break

            elif action == "Action":
                user_input = input("Check Enemies? Type 'check': ").strip().lower()
                if user_input == "check":
                    alive_enemies = [enemy for enemy in self.enemies if enemy["status"] == "alive"]
                    if not alive_enemies:
                        print("No enemies are left alive.")
                    else:
                        for enemy in alive_enemies:
                            print(f"{enemy['name']} - Health: {enemy['health']}, Status: {enemy['status']}")
                        
                        total_damage = sum(50 for enemy in alive_enemies)
                        self.damage(total_damage)

                else:
                    print("Invalid Action. Returning to fight.")

            if self.health <= 0:
                self.reset_health()



            elif action == "Item":
                print("Available Items: \nLegendary Hero")
                user_input = input("Want to consume Legendary Hero Item? Y/N: ").strip().lower()

                if user_input == "y":
                    self.heal(50)
                    alive_enemies = [enemy for enemy in self.enemies if enemy["status"] == "alive"]
                    total_damage = sum(50 for enemy in alive_enemies)
                    self.damage(total_damage)

                    if self.health <= 0:
                        self.reset_health()
                        return
                else:
                    print("No item used.")


            elif action == "Mercy":
                alive_enemies = [enemy for enemy in self.enemies if enemy["status"] == "alive"]
                
                if not alive_enemies:
                    print("No enemies are left to spare.")
                    break

                alive_enemy_names = ", ".join([enemy["name"] for enemy in alive_enemies])
                target_enemy_name = input(f"Which enemy will you spare? ({alive_enemy_names}): ").strip()

                enemy_index = next((i for i, e in enumerate(self.enemies)
                                    if e["name"].lower() == target_enemy_name.lower() and e["status"] == "alive"), None)

                if enemy_index is None:
                    print("Invalid enemy name or enemy already defeated!")
                    continue

                self.spare_enemy(enemy_index)

                if any(e["status"] == "alive" for e in self.enemies):
                    self.enemy_damage()
                    if self.health <= 0:
                        print("Player has died after enemy attack!")
                        self.reset_health()
                        return
                    else:
                        print(f"Player's health after enemy attack: {self.health}")
                else:
                    if all(enemy["status"] in ["defeated", "spared"] for enemy in self.enemies):
                        print("All enemies are gone. Returning to Normal State.")
                        self.state = "Normal State"
                        break
                    else:
                        print("There are still enemies alive.")


        if self.state == "Normal State":
            if self.check_all_spared():
                self.route = "Pacifist Route"
                print("All enemies were spared, You are in Pacifist Route!")
                self.state = "Game Ends State"
            elif self.check_all_slashed():
                self.route = "Genocide Route"
                print("All enemies were killed, You are in Genocide Route!")
                self.state = "Game Ends State"
            elif self.check_all_slashed_or_spared():
                self.route = "Neutral Route"
                print("An enemy was killed and spared, You are in Neutral Route!")
                self.state = "Game Ends State"

        # Game Ends State
        if self.state == "Game Ends State":
            print("Game Finished!")

    def run_game(self):
        while self.state != "Game Ends State":
            self.transition()


game_fsm = GameFSM()
game_fsm.run_game()