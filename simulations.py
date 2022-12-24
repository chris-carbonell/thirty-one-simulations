# Dependencies

# general
import copy
import csv
from datetime import datetime
import logging
import sys
import time

# game
from game import ThirtyOne

# Constants

GAMES_PER_SIMULATION = 10000

# Classes

class Simulator():
    '''
    a simulator simulates games and tracks their results
    '''

    # constants
    NOW = datetime.now().strftime('%Y-%m-%d %H%M')
    PATH_CSV_OUTPUT = f"output/{NOW}_results.csv"
    PATH_LOG_OUTPUT = f"output/{NOW}_log.log"
    
    def __init__(self):
        
        self.game_id = 0  # unique ID for game (i.e., deck, number of players)
        
        # set up output file
        self.output_file = open(self.PATH_CSV_OUTPUT, 'w+', newline='')
        self.writer = csv.writer(self.output_file, delimiter=',')
        self.writer.writerow([
            "ts_created",
            
            "game_id",
            "game_iteration_id",

            "num_players",
            "rounds_played",
            "turns_played",

            "knocker",
            "knocker_score",
            "knocker_hand",
            "knocker_survived",

            "scores",
            "hands",

            "deck",
            "discard"
        ])

        # set up logger
        # https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout

        self.logger = logging.getLogger(__name__)

        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
        fileHandler = logging.FileHandler(self.PATH_LOG_OUTPUT)  # log to file
        fileHandler.setFormatter(logFormatter)
        self.logger.addHandler(fileHandler)

        # consoleHandler = logging.StreamHandler(sys.stdout)  # log to stdout
        consoleHandler = logging.StreamHandler()  # log to stderr
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)

        self.logger.setLevel(logging.INFO)

    def simulate(self, num_players):
        
        # create base game
        base_game = ThirtyOne(num_players=num_players)

        # copy game once for each player in the game
        # for each of those games, set a new knocker in each
        # e.g., if 6 players, first game has the first player knocker,
        # second game has the second player knock
        
        # simulate
        for knocker in range(num_players):

            # log
            self.logger.info(f"game_id = {str(self.game_id).zfill(6)}, num_players = {num_players}, knocker = {knocker}")

            # get starting time
            unix_ts = time.mktime(datetime.now().timetuple())

            # copy game
            game = copy.deepcopy(base_game)

            # play and set knocker
            game.play(knocker=knocker)

            # save info
            self.writer.writerow([
                unix_ts,

                self.game_id,
                knocker,

                len(game.players),
                game.round,
                game.turns,

                knocker,
                game.scores[knocker],
                game.hands[knocker],
                game.knocker_survived,

                game.scores,
                game.hands,

                game.deck.cards,
                game.discard
            ])

        # clean up
        self.output_file.flush()
        self.game_id += 1

    def shutdown(self):
        self.output_file.close()

if __name__ == "__main__":

    # simulate
    simulator = Simulator()
    for num_players in range(2,7):
        for gm in range(GAMES_PER_SIMULATION):
            simulator.simulate(num_players)

    # clean up
    simulator.shutdown()