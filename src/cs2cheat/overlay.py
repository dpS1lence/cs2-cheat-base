import sys
import pygetwindow as gw
from PyQt5 import QtWidgets, QtCore, QtGui
import math


class Overlay(QtWidgets.QWidget):
    def __init__(self, game_title):
        super().__init__()
        self.game_title = game_title
        self.enemy_positions = []
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.update_overlay_position()

    def update_overlay_position(self):
        game_window = gw.getWindowsWithTitle(self.game_title)
        if game_window:
            game_window = game_window[0]
            self.setGeometry(game_window.left, game_window.top, game_window.width, game_window.height)
        else:
            print("Game window not found. Make sure the game is running and the title is correct.")
            self.setGeometry(100, 100, 800, 600)

    def set_enemy_positions(self, positions):
        self.enemy_positions = positions
        self.repaint()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 5))
        for x, y, distance in self.enemy_positions:
            radius = self.calculate_circle_size(distance)
            qp.drawEllipse(int(x - radius / 2), int(y - radius / 2), int(radius), int(radius))

    @staticmethod
    def calculate_circle_size(distance):
        base_size = 50
        scale_factor = 1 - (distance / 1000.0)
        return max(10, min(base_size * scale_factor, 50))

    @staticmethod
    def get_enemy_positions():
        """
        Conceptual function to get enemy positions and convert them to screen coordinates.
        This is a placeholder and would need to be implemented based on available, legitimate game data.

        Returns:
            List of tuples, each representing an enemy's (screen_x, screen_y, distance) to the player.
        """
        enemy_positions = []

        # Hypothetical loop over game data to extract enemy positions
        for enemy in game_data.get_enemies():
            # Assume game_data.get_enemies() is a method that returns a list of enemy objects
            # Each enemy object has attributes x, y, z in the game world

            # Convert game world coordinates (x, y, z) to screen coordinates (screen_x, screen_y)
            # This step requires knowledge of the game's camera and projection matrix, which
            # varies by game and is not trivial to obtain or calculate without official support.
            screen_x, screen_y = Overlay.world_to_screen(enemy.x, enemy.y, enemy.z)

            # Calculate distance from the player to the enemy
            # This could be a simple Euclidean distance calculation in 3D space
            distance = Overlay.calculate_distance(player_position, (enemy.x, enemy.y, enemy.z))

            # Append the screen position and distance to the list
            enemy_positions.append((screen_x, screen_y, distance))

        return enemy_positions

    @staticmethod
    def calculate_distance(player_position, enemy_position):
        """
        Calculate the 3D Euclidean distance between two points.

        Args:
            player_position (tuple): The (x, y, z) coordinates of the player.
            enemy_position (tuple): The (x, y, z) coordinates of the enemy.

        Returns:
            float: The distance between the player and the enemy.
        """
        return ((enemy_position[0] - player_position[0]) ** 2 +
                (enemy_position[1] - player_position[1]) ** 2 +
                (enemy_position[2] - player_position[2]) ** 2) ** 0.5

    @staticmethod
    def world_to_screen(world_position, view_matrix, screen_width, screen_height):
        """
        Convert a point from world coordinates to screen coordinates.

        Args:
            world_position (tuple): The (x, y, z) coordinates in the world.
            view_matrix (list of lists): The game's view matrix.
            screen_width (int): The width of the screen in pixels.
            screen_height (int): The height of the screen in pixels.

        Returns:
            tuple: The (x, y) screen coordinates, or None if the point is not on the screen.
        """
        # Matrix multiplication (world position * view matrix)
        clip_coords = [0, 0, 0, 0]
        clip_coords[0] = world_position[0] * view_matrix[0][0] + world_position[1] * view_matrix[1][0] + world_position[
            2] * view_matrix[2][0] + view_matrix[3][0]
        clip_coords[1] = world_position[0] * view_matrix[0][1] + world_position[1] * view_matrix[1][1] + world_position[
            2] * view_matrix[2][1] + view_matrix[3][1]
        clip_coords[2] = world_position[0] * view_matrix[0][2] + world_position[1] * view_matrix[1][2] + world_position[
            2] * view_matrix[2][2] + view_matrix[3][2]
        clip_coords[3] = world_position[0] * view_matrix[0][3] + world_position[1] * view_matrix[1][3] + world_position[
            2] * view_matrix[2][3] + view_matrix[3][3]

        if clip_coords[3] < 0.1:
            return None  # Object is behind the camera

        # Perspective division
        ndc = (clip_coords[0] / clip_coords[3], clip_coords[1] / clip_coords[3])

        # Convert to screen coordinates
        screen_x = (ndc[0] + 1) * screen_width / 2
        screen_y = (1 - ndc[1]) * screen_height / 2

        return (int(screen_x), int(screen_y))
