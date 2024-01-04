import argparse
import game.game

parser = argparse.ArgumentParser(description='Shooter Game')
parser.add_argument('--mode', type=str, help='Game Mode "server" of "client"', default='client')
parser.add_argument("--host", type=str, help='Server host', default='localhost')
parser.add_argument("--port", type=int, help='Server port', default=27015)

args = parser.parse_args()
game.game.Game.get().start(args.host, args.port, args.mode)