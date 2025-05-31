# import csv
# import os

# import numpy as np
# import chessEngine as s

# startPower = {
#     "ch": 90,
#     "hs": 40,
#     "ep": 25,
#     "ad": 30,
#     "gn": 9000,
#     "cn": 45,
#     "sd": 10,
# }  # Value of pieces at the start of the game
# midPower = {
#     "ch": 90,
#     "hs": 40,
#     "ep": 25,
#     "ad": 30,
#     "gn": 9000,
#     "cn": 50,
#     "sd": 20,
# }  # Value of pieces at the middle of the game
# endPower = {
#     "ch": 100,
#     "hs": 50,
#     "ep": 40,
#     "ad": 40,
#     "gn": 9000,
#     "cn": 40,
#     "sd": 25,
# }  # Value of pieces at the end of the game

# # Count score at the bottom half of the board
# bottomHalfPosition = {
#     "ch": [],
#     "hs": [],
#     "ep": [],
#     "ad": [],
#     "gn": [],
#     "cn": [],
#     "sd": [],
# }
# for i in bottomHalfPosition.keys():
#     name = i + ".csv"
#     with open(os.path.join(os.path.dirname(__file__), "unity", name), "r") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             for r in range(len(row)):
#                 row[r] = float(row[r])
#             bottomHalfPosition[i] += [row]

# # Count score at the upper half of the board
# upperHalfPosition = {
#     "ch": [],
#     "hs": [],
#     "ep": [],
#     "ad": [],
#     "gn": [],
#     "cn": [],
#     "sd": [],
# }
# for i in bottomHalfPosition.keys():
#     upperHalfPosition[i] = bottomHalfPosition[i][::-1]