# 2D Mining Adventure Game

## 📌 Project Description

Demo: https://youtu.be/1PJbU3Y5cd0

<img width="2242" height="2084" alt="game_demo" src="https://github.com/user-attachments/assets/e4a9d50b-3234-4b69-885d-f3f2ca1e3cfe" />


This project is a 2D grid-based adventure game written using Python where the player explores an ever-changing maze in search of treasure.

The player controls an adventurer sprite who can mine blocks, collect currency, and use keys to unlock doors. Progression is based on exploration, resource collection, and navigating through the maze.

The main objective is to reach the treasure chest at the end of the map as quickly as possible. The game tracks completion time, allowing players to measure improvement across multiple playthroughs.



---

## 🎮 Gameplay Features

- Player-controlled adventurer sprite  
- Block mining system that rewards currency  
- Currency system used to purchase keys  
- Key-based door unlocking mechanics  
- Exploration of an ever-changing maze environment  
- Treasure-based win condition  
- Time tracking for performance improvement  

---

## 🧠 Core Gameplay Loop

Mine blocks → Earn currency → Buy keys → Unlock doors → Reach treasure → Track completion time

Player progress is determined by both:
- Physical movement through the maze  
- Inventory progression (keys and currency)  

---

## 🛠️ Requirements / Installation

To run the game, open `LabyrinthFinal.py` in a Python IDE.

### Required Libraries:
- cmu_graphics  
- PIL (Pillow)  

---

### 📦 Installation Instructions

#### cmu_graphics
Download from:
https://academy.cs.cmu.edu/desktop

After downloading:
- Place the `cmu_graphics` folder into the same directory as the project  
- Ensure it is correctly placed so the program can import it  

#### Pillow (PIL)
Install via pip:

```bash
pip install Pillow
```
