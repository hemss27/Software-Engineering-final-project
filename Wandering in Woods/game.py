import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from levels.level1 import Level
from resources.dimension import Dimensions

DIFFICULTY = ['EASY']
DIMS = [3]
ROWS = [3]
COLUMNS = [3]
PLAYERS = [2]
FPS = 60


class Stats:
    def __init__(self, difficulty="", max=0, min=0, avg=0, total=0, attempt=0):
        self.difficulty = difficulty
        self.max = max
        self.min = min
        self.avg = avg
        self.total = total
        self.attempt = attempt


class Game:
    def __init__(self):
        self.selected_menu_state = 'main'
        self.auto_play = False
        self.selected_level = 'EASY'
        self.is_running = True
        self.is_paused = True
        self.display_caption_prefix = "Lost into the Woods"
        self.stats = []

    def background(self):
        surface.fill((0, 0, 0))

    def update_stats(self, index, score):
        stat = self.stats[index]
        stat.attempt += 1
        stat.total += score
        if stat.min == 0:
            stat.min = score
        else:
            stat.min = min(score, stat.min)
        if stat.max == 0:
            stat.max = score
        else:
            stat.max = max(score, stat.max)
        stat.avg = stat.total / stat.attempt

        try:
            with open(f'scores{index}.txt', 'w') as file:
                file.write(f"{stat.min}\n")
                file.write(f"{stat.max}\n")
                file.write(f"{stat.avg}\n")
                file.write(f"{stat.attempt}\n")
        except FileNotFoundError:
            print("File not found!")

    def play_function(self, difficulty, font, test=False):
        assert isinstance(difficulty, list)
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)

        global main_menu, clock

        if difficulty in ['EASY', 'MEDIUM', 'HARD']:
            level = Level(autoplay=False, dimensions=Dimensions(COLUMNS[0], ROWS[0]), number_of_players=PLAYERS[0])
            score = level.start(clock)
        else:
            raise ValueError(f'Unknown difficulty {difficulty}')

        f_esc = font.render('Game Ended', True, (146, 2, 176))

        if self.selected_level in ["EASY", "MEDIUM", "HARD"]:
            self.update_stats(['EASY', 'MEDIUM', 'HARD'].index(self.selected_level), score)

        bg_color = (228, 209, 210)
        self.prep_play_menu()
        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=main_theme,
            title='Main Menu',
            width=WINDOW_WIDTH * 0.8,
        )
        main_menu.add.button('Play', self.play_menu)
        main_menu.add.selector('Difficulty ',
            [('1st level', 'EASY'), ('2nd level', 'MEDIUM'), ('3rd level', 'HARD')],
            onchange=self.change_difficulty,
            selector_id='select_difficulty')
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        main_menu.enable()

        while True:
            clock.tick(60)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        main_menu.enable()
                        return
            if main_menu.is_enabled():
                main_menu.update(events)
            surface.fill(bg_color)
            surface.blit(f_esc, (int((WINDOW_WIDTH - f_esc.get_width()) / 2),
                                 int(WINDOW_HEIGHT / 2 + f_esc.get_height())))
            pygame.display.flip()

    def change_difficulty(self, value, difficulty):
        self.selected_level = difficulty
        DIFFICULTY[0] = difficulty

    def change_rows(self, value, row):
        ROWS[0] = row

    def change_columns(self, value, col):
        COLUMNS[0] = col

    def change_dims(self, value, col):
        DIMS[0] = col

    def change_players(self, value, players):
        PLAYERS[0] = players

    def prep_play_menu(self):
        f = pygame_menu.font.FONT_COMIC_NEUE
        submenu_theme = pygame_menu.themes.THEME_DARK.copy()
        submenu_theme.background_color = (42, 2, 57)
        submenu_theme.widget_font = f
        submenu_theme.title_font = f
        submenu_theme.title_background_color = (42, 2, 57)
        submenu_theme.title_font_color = (191, 149, 222)
        self.play_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            title='                   ..........:::Game Menu:::.......... ',
            width=WINDOW_WIDTH * 0.8,
            theme=submenu_theme
        )
        play_submenu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=submenu_theme,
            title='Scores',
            width=WINDOW_WIDTH * 0.8
        )
        for stat in self.stats:
            min_score, max_score, avg_score, attempt = stat.min, stat.max, stat.avg, stat.attempt
            play_submenu.add.button(f'{stat.difficulty.lower()} minimum score {min_score} ', pygame_menu.events.BACK)
            play_submenu.add.button(f'{stat.difficulty.lower()} maximum score {max_score} ', pygame_menu.events.BACK)
            play_submenu.add.button(f'{stat.difficulty.lower()} average score {avg_score} ', pygame_menu.events.BACK)
            play_submenu.add.button(f'{stat.difficulty.lower()} attempts {attempt}', pygame_menu.events.BACK)
        play_submenu.add.button('MENU', pygame_menu.events.RESET)
        self.play_menu.add.button('Begin', self.play_function, DIFFICULTY, pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
        self.play_menu.add.selector('Rows: ',
                                   [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)],
                                   onchange=self.change_rows, selector_id='select_row')
        self.play_menu.add.selector('Columns: ',
                                   [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9)],
                                   onchange=self.change_columns, selector_id='select_cols')
        self.play_menu.add.selector('Players: ',
                                   [('2', 2), ('3', 3), ('4', 4)],
                                   onchange=self.change_players, selector_id='select_players')
        self.play_menu.add.button('points', play_submenu)
        self.play_menu.add.button('main menu', pygame_menu.events.BACK)

    def prep_menu(self):
        global clock, main_menu, surface
        surface = create_example_window('Lost into the woods', (WINDOW_WIDTH, WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        self.prep_play_menu()
        main_theme = pygame_menu.themes.THEME_DARK.copy()
        f = pygame_menu.font.FONT_COMIC_NEUE
        main_theme.background_color = (42, 2, 57)
        main_theme.widget_font = f
        main_theme.title_background_color = (42, 2, 57)
        main_theme.title_font_color = (191, 149, 222)
        main_theme.title_font = f
        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=main_theme,
            title='                ........:::Lost into the woods:::........',
            width=WINDOW_WIDTH * 0.8
        )
        main_theme.widget_font_size = 40
        main_menu.add.button('Start', self.play_menu)
        main_menu.add.selector('Difficulty ',
            [('1st level', 'EASY'), ('2nd level', 'MEDIUM'), ('3rd level', 'HARD')],
            onchange=self.change_difficulty,
            selector_id='select_difficulty')
        main_menu.add.button('Exit', pygame_menu.events.EXIT)

    def prev_stats(self):
        data0 = [0 for _ in range(4)]
        data1 = [0 for _ in range(4)]
        data2 = [0 for _ in range(4)]
        try:
            with open('./scores0.txt') as f:
                lines = f.readlines()
                for k, v in enumerate(lines):
                    data0[k] = round(float(v.strip()))
            with open('./scores1.txt') as f:
                lines = f.readlines()
                for k, v in enumerate(lines):
                    data1[k] = round(float(v.strip()))
            with open('./scores2.txt') as f:
                lines = f.readlines()
                for k, v in enumerate(lines):
                    data2[k] = round(float(v.strip()))
        except FileNotFoundError:
            print("")
        self.stats = [
            Stats('EASY', data0[0], data0[1], data0[2], data0[2] * data0[3], data0[3]),
            Stats('MEDIUM', data1[0], data1[1], data1[2], data1[2] * data1[3], data1[3]),
            Stats('HARD', data2[0], data2[1], data2[2], data2[2] * data2[3], data2[3]),
        ]

    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.prev_stats()
        self.prep_menu()
        pygame.mixer.music.load('./dream.mp3')
        pygame.mixer.music.play(loops=0)
        while True:
            clock.tick(FPS)
            self.background()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if main_menu.is_enabled():
                main_menu.mainloop(surface, self.background, disable_loop=False, fps_limit=FPS)
            pygame.display.flip()
