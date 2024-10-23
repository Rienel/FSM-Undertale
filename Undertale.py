#This is the code that has a GUI for a better experience or visualization


import tkinter as tk
from PIL import Image, ImageTk

class GameFSM:
    def __init__(self, root):
        self.state = "Game Start State"
        self.route = None
        self.health = 100
        self.max_health = 100
        self.enemies = [
            {"name": "Centaur", "health": 50, "status": "alive", "image": "centaur.png"},
            {"name": "Minotaur", "health": 50, "status": "alive", "image": "minotaur.png"}
        ]
        self.enemy_image_labels = []

        self.root = root
        self.root.title("Undertale-like Game Interface")
        self.root.geometry("600x600")
        self.root.config(bg="black")

        #health bar and stats
        self.top_frame = tk.Frame(root, bg="black")
        self.top_frame.pack(pady=10)

        self.player_label = tk.Label(self.top_frame, text="CHARA", fg="white", bg="black", font=("Arial", 16))
        self.player_label.grid(row=0, column=0)

        self.lv_label = tk.Label(self.top_frame, text="LV 11", fg="white", bg="black", font=("Arial", 16))
        self.lv_label.grid(row=0, column=1, padx=10)

        self.hp_label = tk.Label(self.top_frame, text="HP", fg="white", bg="black", font=("Arial", 16))
        self.hp_label.grid(row=0, column=2, padx=10)

        self.hp_value_label = tk.Label(self.top_frame, text=f"{self.health} / {self.max_health}", fg="white", bg="black", font=("Arial", 16))
        self.hp_value_label.grid(row=0, column=3, padx=10)

        self.hp_bar = tk.Canvas(self.top_frame, width=200, height=20, bg="black")
        self.hp_bar.create_rectangle(0, 0, 180, 20, fill="yellow")
        self.hp_bar.grid(row=0, column=4)

        self.enemy_image_frame = tk.Frame(root, bg="white", width=400, height=120, highlightbackground="white", highlightthickness=1)
        self.enemy_image_frame.pack(pady=10)
        self.load_enemy_images()

        self.middle_frame = tk.Frame(root, bg="black")
        self.middle_frame.pack(pady=10)

        self.text_display = tk.Text(self.middle_frame, height=10, width=50, bg="white", fg="black", font=("Arial", 14), state="disabled")
        self.text_display.pack()

        self.bottom_frame = tk.Frame(root, bg="black")
        self.bottom_frame.pack(pady=20)

        self.fight_button = tk.Button(self.bottom_frame, text="FIGHT", font=("Arial", 14), fg="yellow", bg="black", width=10, command=self.fight_action)
        self.fight_button.grid(row=0, column=0, padx=10)

        self.act_button = tk.Button(self.bottom_frame, text="ACT", font=("Arial", 14), fg="orange", bg="black", width=10, command=self.act_action)
        self.act_button.grid(row=0, column=1, padx=10)

        self.item_button = tk.Button(self.bottom_frame, text="ITEM", font=("Arial", 14), fg="orange", bg="black", width=10, command=self.item_action)
        self.item_button.grid(row=0, column=2, padx=10)

        self.mercy_button = tk.Button(self.bottom_frame, text="MERCY", font=("Arial", 14), fg="orange", bg="black", width=10, command=self.mercy_action)
        self.mercy_button.grid(row=0, column=3, padx=10)

        self.buttons = [self.fight_button, self.act_button, self.item_button, self.mercy_button]
        self.enable_buttons()

    def load_enemy_images(self):
        for enemy in self.enemies:
            if enemy['status'] == 'alive':
                img = Image.open(enemy['image'])
                img = img.resize((100, 100))
                enemy_photo = ImageTk.PhotoImage(img)

                label = tk.Label(self.enemy_image_frame, image=enemy_photo, bg="white")
                label.image = enemy_photo
                label.pack(side=tk.LEFT, padx=10)
                self.enemy_image_labels.append(label)

    #TODO remove enemy image after defeated
    def remove_enemy_image(self, index):
        label = self.enemy_image_labels[index]
        label.destroy()
        self.enemy_image_labels[index] = None

    #TODO make buttons disable after an action
    def disable_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")


    def enable_buttons(self):
        for button in self.buttons:
            button.config(state="normal")

    # Fight action
    def fight_action(self):
        self.update_text("Select an enemy to fight:")
        self.disable_buttons()
        alive_enemies = [i for i, e in enumerate(self.enemies) if e["status"] == "alive"]
        for enemy_index in alive_enemies:
            self.clickable_enemy_name(enemy_index, self.slash_enemy)

    # Act action
    def act_action(self):
        self.update_text("Checking enemies...")
        alive_enemies = [enemy for enemy in self.enemies if enemy["status"] == "alive"]
        if not alive_enemies:
            self.update_text("No enemies left to check!")
        else:
            for enemy in alive_enemies:
                self.update_text(f"{enemy['name']} - HP: {enemy['health']}, Damage: 50, - Status: {enemy['status']}")
        self.enemy_damage()


    # Item action
    def item_action(self):
        self.update_text("Click 'Legendary Hero' to heal 50 HP.")
        self.text_display.config(state="normal")
        start_index = self.text_display.index(tk.END)
        self.text_display.insert(tk.END, "Legendary Hero\n", "legendary_hero")
        self.text_display.tag_add("legendary_hero", start_index, f"{start_index} lineend")
        self.text_display.tag_bind("legendary_hero", "<Button-1>", lambda e: self.use_legendary_hero())
        self.text_display.config(state="disabled")

    def use_legendary_hero(self):
        self.heal(50)
        self.update_health_bar()
        self.update_text("You used Legendary Hero and healed 50 HP!")
        self.enable_buttons()

    # Mercy action
    def mercy_action(self):
        self.update_text("Select an enemy to spare:")
        self.disable_buttons()
        alive_enemies = [i for i, e in enumerate(self.enemies) if e["status"] == "alive"]
        for enemy_index in alive_enemies:
            self.clickable_enemy_name(enemy_index, self.spare_enemy)


    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        self.update_text(f"Player healed! Health: {self.health}")

        if any(e['status'] == 'alive' for e in self.enemies):
            self.enemy_damage()

    def update_health_bar(self):
        health_percent = self.health / self.max_health
        new_width = int(200 * health_percent)
        self.hp_bar.delete("all")
        self.hp_bar.create_rectangle(0, 0, new_width, 20, fill="yellow")
        self.hp_value_label.config(text=f"{self.health} / {self.max_health}")

    def damage(self, amount):
        self.health -= amount
        self.update_text(f"Player took {amount} damage! Health: {self.health}")
        
        if self.health <= 0:
            self.update_text("You have died! Respawning...")
            self.respawn()
        else:
            self.update_health_bar()


    def enemy_damage(self):
        alive_enemies = sum(1 for e in self.enemies if e["status"] == "alive")

        if alive_enemies == 2:
            self.damage(100)
        elif alive_enemies == 1:
            self.damage(50)

        self.update_health_bar()
        if self.health <= 0:
            self.state = "Player Dies"
            self.update_text("Player has died!")
            self.disable_buttons()


    def slash_enemy(self, enemy_index):
        enemy = self.enemies[enemy_index]
        enemy["health"] -= 50
        if enemy["health"] <= 0:
            enemy["status"] = "defeated"
            self.update_text(f"{enemy['name']} has been defeated!")
            self.remove_enemy_image(enemy_index)
        else:
            self.update_text(f"{enemy['name']} took 50 damage! Remaining HP: {enemy['health']}")

        if any(e['status'] == 'alive' for e in self.enemies):
            self.enemy_damage()

        self.enable_buttons()
        self.check_game_end()

    def spare_enemy(self, enemy_index):
        enemy = self.enemies[enemy_index]
        enemy["status"] = "spared"
        self.update_text(f"{enemy['name']} was spared!")
        self.remove_enemy_image(enemy_index)

        if any(e['status'] == 'alive' for e in self.enemies):
            self.enemy_damage()

        self.enable_buttons()
        self.check_game_end()

    def respawn(self):
        self.health = self.max_health
        self.update_health_bar()
        self.update_text("You have respawned with full health!")


    #TODO make text clickable for attack or spare
    def clickable_enemy_name(self, enemy_index, action):
        enemy = self.enemies[enemy_index]
        self.text_display.config(state="normal")
        self.text_display.insert(tk.END, f"{enemy['name']}\n", f"enemy_{enemy_index}")
        self.text_display.config(state="disabled")
        self.make_clickable(f"enemy_{enemy_index}", lambda e, idx=enemy_index: action(idx))

    def update_text(self, text):
        self.text_display.config(state="normal")
        self.text_display.insert(tk.END, text + "\n")
        self.text_display.config(state="disabled")

    def make_clickable(self, tag, action):
        if self.state == "Game Ends State":
            return
        self.text_display.tag_add(tag, f"{tag}.first", f"{tag}.last")
        self.text_display.tag_bind(tag, "<Button-1>", action)


    def check_game_end(self):
        if all(e["status"] == "defeated" for e in self.enemies):
            self.route = "Genocide Route"
            self.update_text("All enemies were killed. You are on the Genocide Route.")
            self.state = "Game Ends State"
            self.update_text("Game Finished!")

        elif all(e["status"] == "spared" for e in self.enemies):
            self.route = "Pacifist Route"
            self.update_text("All enemies were spared. You are on the Pacifist Route.")
            self.state = "Game Ends State"
            self.update_text("Game Finished!")

        elif all(e["status"] in ["defeated", "spared"] for e in self.enemies):
            self.route = "Neutral Route"
            self.update_text("An enemy was spared and killed. You are on the Neutral Route.")
            self.state = "Game Ends State"
            self.update_text("Game Finished!")

        if self.state == "Game Ends State":
            self.disable_buttons()
            self.text_display.config(state="disabled")




if __name__ == "__main__":
    root = tk.Tk()
    game = GameFSM(root)
    root.mainloop()
