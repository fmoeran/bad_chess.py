from game import Game
import search

bot = search.search


if __name__ == "__main__":
    game = Game(debug=False, black_is_ai=True, white_is_ai=False)
    game.set_ai(bot)
    game.set_ai(bot, colour=0)
    #game.load_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ")
    print(game.run(show_fps=True))
