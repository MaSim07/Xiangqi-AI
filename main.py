"""
Copyright (C) 2021-2022 Simon Ma <https://github.com/Simuschlatz> 
- All Rights Reserved. You may use, distribute and modify this code
under the terms of the GNU General Public License
"""
import pygame
from core.Engine import Board, LegalMoveGenerator, Clock, UI, ZobristHashing
from core.Engine.AI import Dfs, Evaluation
from core.Utils import init_imgs, get_perft_result
from time import perf_counter

FPS = 45
WIDTH = 1400
HEIGHT = 900
UNIT = HEIGHT // 11
BOARD_WIDTH = 9 * UNIT
BOARD_HEIGHT = 10 * UNIT
BUTTON_DIMS = (UNIT * 2.2, UNIT * .83)
OFFSET_X = (WIDTH - BOARD_WIDTH) // 2
OFFSET_Y = (HEIGHT - BOARD_HEIGHT) // 2

MOVE_MARKER_CIRCLE = UNIT / 7
CAPTURE_CIRCLE_D = UNIT * 1.1

# Style of piece images
piece_style_western = True

IMGS = init_imgs(UNIT, (WIDTH, HEIGHT), (BOARD_WIDTH, BOARD_HEIGHT), BUTTON_DIMS, piece_style_western)
# PIECES_IMGS, BOARD_IMG, BG_IMG, BUTTON_IMGS = IMGS

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("JOE MAMA")
# pygame.display.set_icon(PIECES_IMGS[7])
pygame.font.init()


INITIAL_FEN_BLACK_DOWN = "RHEAKAEHR/9/1C5C/P1P1P1P1P/9/9/p1p1p1p1p/1c5c/9/rheakaehr"
INITIAL_FEN_RED_DOWN = "rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR"

search = None
AI_SEARCH_DEPTH = 4

def get_num_positions(depth, board):
    p_t = perf_counter()
    num_positions = get_perft_result(depth, board)
    time = perf_counter() - p_t
    print(f"depth: {depth} || nodes searched: {num_positions} || time: {round(time, 2)}")

    
def main():
    only_display_mode = False
    play_as_red = True
    fen = INITIAL_FEN_RED_DOWN if play_as_red else INITIAL_FEN_BLACK_DOWN

    Clock.init(600, "MIKE", "OXLONG")
    # If you play as red, red pieces are gonna be at the bottom, else they're at the top
    ZobristHashing.init_table()
    board = Board(fen, play_as_red, red_moves_first=True)
    if not only_display_mode:
        LegalMoveGenerator.init_board(board)
        LegalMoveGenerator.load_moves()

    Evaluation.init(board)
    Dfs.init(board)

    ui = UI(WIN, (WIDTH, HEIGHT), board, (OFFSET_X, OFFSET_Y), UNIT, IMGS)

    # ------To run perft search------
    # iterative = True
    # depth = 4
    # depths = [depth]
    # if iterative:
    #     depths = range(1, depth + 1)
    # for d in depths:
    #     get_num_positions(d, board)
    # -------------------------------

    py_clock = pygame.time.Clock()
    run = True
    while run:
        if only_display_mode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            ui.render()
            continue    
        ui.update()
        py_clock.tick(FPS)

if __name__ == "__main__":
    main()