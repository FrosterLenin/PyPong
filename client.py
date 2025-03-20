import pyxel
import socket
import struct
import select
import zlib
from ball import Ball
from player import FirstPlayer, SecondPlayer
from pong_constants import GameConstants, PacketType, ObjectType, PacketLenghts
from managers import TickManager, RenderManager, PhysicsManager

class Client:
    def __init__(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 12345)
        self.client_id = ""       
        self.client_socket.setblocking(False)
        self.socket_list = [self.client_socket]
        self.read_sockets, _ , _ = select.select(self.socket_list,[],[],0)
        self.clients = {} #ClientID, Player
        self.clients_status = {} #ClientID, False = Not ready to play
        self.set_game_objects()

        pyxel.init(width= GameConstants.WIDTH, height=GameConstants.HEIGHT, title= "pong")
        
    def set_game_objects(self):
        self.tick_manager = TickManager()
        self.physics_manager = PhysicsManager()
        self.render_manager = RenderManager()

        if GameConstants.DEBUG == 1:
            self.ball = Ball()
            self.ball.is_running = True
            self.ball.register_to_managers([self.tick_manager, self.render_manager, self.physics_manager])
            self.player1 = FirstPlayer()
            self.player1.register_to_managers([self.tick_manager, self.render_manager, self.physics_manager])
            self.player2 = SecondPlayer()
            self.player2.register_to_managers([self.tick_manager, self.render_manager, self.physics_manager])
        if GameConstants.DEBUG == 2:
            self.ball = Ball()

    # def create_packet(self, data):
    #     #creating a packet for position. Ideally this should be generalized in order to be used for every type of packet
    #     self.position_packet_counter += 1
    #     if self.position_packet_counter > 255:
    #         self.position_packet_counter = 0        
    #     crc = zlib.crc32(data)
    #     out_packet = data + struct.pack(">I", crc)
    #     return out_packet

    def send_request_id(self):
        data = struct.pack(">BB", PacketType.REQUEST_ID, PacketLenghts.client_request_id_packet_length)
        #packet = self.create_packet(data)
        self.client_socket.sendto(data, self.server_address)

    def send_position(self):
        x = self.clients[self.client_id].x
        y = self.clients[self.client_id].y
        data = struct.pack(">BBBII", PacketType.POSITION, ObjectType.PLAYER, PacketLenghts.client_position_packet_lenght, x, y)
        #packet = self.create_packet(data)
        self.client_socket.sendto(data, self.server_address)

    def send_game_start(self):
        data = struct.pack(">BB", PacketType.REQUEST_ID, PacketLenghts.client_game_start_packet_length)
        #packet = self.create_packet(data)
        self.client_socket.sendto(data, self.server_address)

    def handle_spawn(self, data):
        if GameConstants.DEBUG == 2:
            print("Received spawn packet.")
        _, packet_length, received_client_id = struct.unpack(">BBI",data)
        if packet_length == len(data):     
            self.client_id = received_client_id
            if GameConstants.DEBUG == 2:
                print("Assigned ID {0} at client {1}".format(received_client_id))
            # add the player based on how much players are in the server
            if self.client_id == 0:
                self.clients[self.client_id] = FirstPlayer()
                self.clients[self.client_id].register_to_managers([self.tick_manager, self.render_manager])
            else:
                self.clients[self.client_id] = SecondPlayer()
                self.clients[self.client_id].register_to_managers([self.tick_manager, self.render_manager])
            self.clients_status[self.client_id] = False
    def handle_scored(self, data):
        _, packet_length, has_scored = struct.unpack(">BB?", data)
        if packet_length == len(data):  
            for current_client_id, current_player in self.clients.items():
                if has_scored and current_client_id == self.client_id:
                    current_player.points += 1
                elif has_scored == False and current_client_id != self.client_id :
                    current_player.points += 1
            

    def handle_position(self, data):
        _, object_type, client_id, packet_length, x, y = struct.unpack(">BBBBII",data)                        
        if packet_length != len(data):
            return
        if object_type == ObjectType.PLAYER:
            for current_client_id, current_player in self.clients.items():
                if client_id not in self.clients_status:
                    self.clients_status[self.client_id] = False
                if current_client_id != self.client_id:
                    current_player.x = x
                    current_player.y = y
        elif object_type == ObjectType.BALL:
            self.ball.x = x
            self.ball.y = y

    def receive_data(self):
        if GameConstants.DEBUG == 2:
            print(f"Socket List: {self.socket_list}")  
            print(f"Read sockets: {self.read_sockets}")  
        for read_socket in self.read_sockets:
            if read_socket == self.client_socket:
                try:
                    data, _ = self.client_socket.recvfrom(1024)
                    if GameConstants.DEBUG == 2:
                        print("Received {0} bytes of data.".format(len(data)))
                    packet_type = struct.unpack(">B",data[:1])[0] # first element of the packed is always the packet type
                    if packet_type == PacketType.SPAWN:
                        self.handle_spawn(data)
                    if packet_type == PacketType.POSITION:   
                        self.handle_position(data)
                    if packet_type == PacketType.SCORED:   
                        self.handle_scored(data)
                except:
                    pass

    def run(self):
        #run client is not into a while since it gets incorporated into the game loop
        self.receive_data()
        if self.client_id:
            if self.clients_status[self.client_id]:
                self.send_position()
            elif pyxel.btn(pyxel.KEY_RETURN):
                self.clients_status[self.client_id] = True
                self.send_game_start()
        else:
            self.send_request_id()
        pyxel.run(self.tick, self.render)

    def tick(self):
        self.tick_manager.manage()
        self.physics_manager.manage()
        if GameConstants.DEBUG == 1:
            self.scores()
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

    def render(self):
        if GameConstants.DEBUG == 0 and self.clients_status[self.client_id] == False:
            pyxel.text(GameConstants.WIDTH , GameConstants.HEIGHT, "Press Enter to get Ready", GameConstants.AGENTS_COLOR)
        self.render_manager.manage()
    
    def scores(self):
        # Score and reset the ball when it goes out of bounds
        if self.ball.x <= 0:
            self.player2.points += 1
            self.ball.reset()

        if self.ball.x >= GameConstants.WIDTH - self.ball.width:
            self.player1.points += 1
            self.ball.reset()

if __name__ == "__main__":
    game = Client()
    game.run()