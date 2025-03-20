from enum import IntEnum

class GameConstants:
    WIDTH = 360
    HEIGHT = 240
    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 40
    BALL_SIZE = 4
    AGENTS_COLOR = 7 # white
    MOVEMENT_SPEED = 2 # use only even numbers
    BALL_SPEED = 2
    DEBUG = 2 #0 = ONLINE (NO DEBUG), 1 = LOCAL DEBUG, 2 = ONLINE DEBUG
    MAX_PLAYERS = 2

class PacketType(IntEnum):
    REQUEST_ID = 1
    POSITION = 2
    SPAWN = 3
    GAME_START = 4
    SCORED = 5

class ObjectType(IntEnum):
    PLAYER = 1
    BALL = 2

class PacketLenghts:
    server_position_packet_lenght = 12  #4B + 2xI (I = 4B)      BBBBII
    server_spawn_packet_lenght = 3  #3B     BBB
    server_scored_packet_lenght = 3 # 2B + ?=Bool(1B)   BB?
    client_position_packet_lenght = 11 # 3B + 2xI (I = 4B)      BBBII
    client_request_id_packet_length = 2 # 2B    BB
    client_game_start_packet_length = 2 # 2B    BB

