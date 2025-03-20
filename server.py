import socket
import struct
import zlib
from pong_constants import PacketType, ObjectType, PacketLenghts
from ball import Ball
from player import SecondPlayer
from managers import TickManager, RenderManager, PhysicsManager
from pong_constants import GameConstants

HOST = 'localhost'
PORT = 12345

clients = {} #client addresses and client ID
clients_position = {} #client addresses and position
clients_status = {} #client addresses and status (false = not ready, true = ready)
next_client_id = 0
game_start = False
ball = Ball()
render_manager = RenderManager()
physics_manager = PhysicsManager()
tick_manager = TickManager()

def send_position(x, y, objectType, client_address, client_id):
    data_packed = struct.pack(">BBBBII", PacketType.POSITION, objectType, client_id, PacketLenghts.server_position_packet_lenght, x, y)
    server_socket.sendto(data_packed, client_address)

def send_scores():
    client_id_that_scored =-1
    data_packed
    if ball.x <= 0:
        client_id_that_scored = 0
    if ball.x >= GameConstants.WIDTH - ball.width:
        client_id_that_scored = 1
    for current_client_id, current_client_address in clients.items():
        if current_client_id == client_id_that_scored:
            data_packed = struct.pack(">BB?", PacketType.SCORED, PacketLenghts.server_scored_packet_lenght, True)
        else:
            data_packed = struct.pack(">BB?", PacketType.SCORED, PacketLenghts.server_scored_packet_lenght, False)
        server_socket.sendto(data_packed, current_client_address)
    return client_id_that_scored

def handle_request_id(data, client_address):
    _, packet_length = struct.unpack(">BB", data)
    if packet_length != len(data) or len(clients) > GameConstants.MAX_PLAYERS - 1:
        return
    else:
        global next_client_id
        client_id = next_client_id
        next_client_id += 1
        clients[client_address] = client_id
        clients_status[client_address] = False
        data_packed = struct.pack(">BBB", PacketType.SPAWN, PacketLenghts.server_spawn_packet_lenght, client_id)   
        if GameConstants.DEBUG == 2:
            print("Assigned ID {0} at client {1}".format(client_id, client_address))
            print("Resending client ID {0} to client {1}".format(clients[client_address], client_address))
        server_socket.sendto(data_packed, client_address)
        print(f"Sent response to {client_address}: {data_packed}")
        if client_id == 1:
            temp_player = SecondPlayer()
            for _, current_client_address in clients.items():
                if current_client_address != client_address:
                    if GameConstants.DEBUG == 2:
                        print("Sending SPAWN to client {0}".format(client_address))
                    send_position(temp_player.x, temp_player.y, ObjectType.PLAYER, client_id, current_client_address)

def handle_game_start(data, client_address):
    _, packet_length = struct.unpack(">BB", data)
    if packet_length != len(data):
        return
    if GameConstants.DEBUG == 2:
        print("Setting client {0} as ready".format(client_address))
    clients_status[client_address] = True

def handle_position(data, client_address):
    _, packet_length, object_type, packet_length, x, y = struct.unpack(">BBBII", data)
    if packet_length != len(data):
        return
    elif object_type == ObjectType.PLAYER:
        clients_position[client_address] = (x,y)
        for _, current_client_address in clients.items():
            if current_client_address != client_address:
                send_position(x, y, ObjectType.PLAYER, clients[client_address], current_client_address)

def tick():
    tick_manager.manage()
    physics_manager.manage()
    scores()

def scores():
    client_id_that_scored = send_scores()
    if client_id_that_scored != -1:
        ball.reset()


def start_server():
    global server_socket, clients, clients_status, game_start, ball, physics_manager, render_manager, tick_manager
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    if GameConstants.DEBUG == 2:
        print("Server listening on {0}:{1}".format(HOST, PORT))
    
    is_server_running = True
    ball.register_to_managers([physics_manager, render_manager])

    while is_server_running:
        try:
            data, client_address = server_socket.recvfrom(1024)
            if GameConstants.DEBUG == 2:
                print("Received {0} bytes of data.".format(len(data)))
            packet_type = struct.unpack(">B",data[:1])[0]
            if packet_type == PacketType.REQUEST_ID:
                handle_request_id(data, client_address)
            if packet_type == PacketType.POSITION:
                handle_position(data, client_address)

            if game_start == False and all(clients_status.values()):
                ball.register_to_managers(tick_manager)
                ball.is_running = True
                game_start = True
            if game_start:
                for _, current_client_address in clients.items():
                    send_position(ball.x, ball.y, ObjectType.BALL, current_client_address)
                tick()
                render_manager.manage()

        except Exception as e:
            print("Server error: {0}".format(e))


if __name__ == "__main__":
    print("Server main starting...")
    start_server()