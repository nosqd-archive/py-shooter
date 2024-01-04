from typing import Optional
from pyray import *
from .utils.game_getter import GAME_GETTER
from network.packet import Packet
from .config import *
from network.client import Client
from network.server import Server
from collections import deque

from .shooter.player import Player


class Game:
    _instance = None

    client: Client = None
    server: Server = None

    running: bool = False
    mode: str = None
    host: str = None
    port: int = None

    _tick_timer = 0

    packet_queue: deque = deque()

    players = []
    lp: int = None
    camera: Camera2D = None

    @staticmethod
    def get():
        GAME_GETTER["get"] = lambda: Game.get()

        if Game._instance is None:
            Game._instance = Game()

        return Game._instance

    def start(
            self,
            host: str,
            port: int,
            mode: str):
        print("Shooter Game")
        self.running = True
        self.mode = mode
        self.host = host
        self.port = port
        lp = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), "local player", 100, True, 0)
        e = Player((WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT // 2), "enemy player", 70, False, 1)
        self.lp = 0
        self.players.append(lp)
        self.players.append(e)
        if mode == "server":
            self._start_server(host, port)
        elif mode == "client":
            self._start_client(host, port)

    @property
    def local_player(self):
        return [p for p in self.players if p.player_id == self.lp][0]

    def _start_server(self, host: str, port: int):
        ...

    def _start_client(self, host: str, port: int):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.client = Client(host, port)
        self.client.create()

        def client_start_callback(err: Optional[Exception]):
            if err is not None:
                print("Client failed to connect")
                print(err)
                exit(1)
            else:
                self._gameloop()

        # self.client.run(client_start_callback)

        self.camera = Camera2D(
            (WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
            (0, 0),
            0,
            1
        )

        self._gameloop()

    def _gameloop(self):
        while self.running:
            if self.mode is "client" and window_should_close():
                self.running = False

            if get_time() - self._tick_timer > GAME_TICK_DELAY:
                self._tick_timer = get_time()
                self._tick()

            if self.mode is "client":
                self._draw()

    def _tick(self):
        for player in self.players:
            player.tick()

    def _draw(self):
        begin_drawing()
        clear_background(BLACK)

        self.camera.target = self.local_player.position
        begin_mode_2d(self.camera)
        for player in self.players:
            player.draw()
        end_mode_2d()

        draw_text(
            f"Shooter Game\nTPS: ?/{GAME_TICKS_PER_SECOND}\nFPS: {get_fps()}\nPlayer position: {self.local_player.position}", 5,
            5, 18,
            RAYWHITE)

        end_drawing()

    def _on_packet(self, client, packet: Packet):
        self.packet_queue.append({"client": client, "packet": packet})
