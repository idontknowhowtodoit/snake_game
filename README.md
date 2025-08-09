# Multiplayer Snake Game

!

## 📝 Introduction

This is a real-time multiplayer snake game built using **Python**. The project demonstrates a client-server architecture where multiple players can connect and play on the same game board.

## ✨ Key Features

-   **Multiplayer Networking:** The server uses `sockets` and `threading` to manage connections and synchronize game state in real time.
-   **Core Game Logic:** Implemented on the server, including snake movement, food spawning, and collision detection.
-   **User Interface:** A simple, graphical user interface is built with `Pygame` for an interactive experience.
-   **Game Flow:** Features a basic start screen and a restart function.

## 🚀 How to Run

1.  **Install Libraries:**
    Make sure you have `Pygame` installed.
    ```bash
    pip install pygame
    ```

2.  **Start the Server:**
    Open a terminal in the project directory and run the server.
    ```bash
    python server.py
    ```

3.  **Start the Clients:**
    Open one or two additional terminals and run the client script.
    ```bash
    python client.py
    ```

## 🛠️ Technologies Used

-   **Python 3**
-   **Pygame**
-   **Socket**
-   **Threading**
