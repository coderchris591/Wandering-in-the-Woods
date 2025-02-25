class Config:
    def __init__(self, mode):
        self.mode = mode
        self.grid_size = (10, 10)
        self.num_players = 2
        self.start_positions = [(0, 0), (9, 9), (0, 9), (9, 0)]  # Initialize with 4 positions
        self.random_movement = True
        self.music = 'background_music.mp3'
        self.win_sound = 'win_sound.wav'
        self.background_image = 'forest_background.jpg'
        self.statistics = True
        self.reset_on_win = True

        if mode == 'K-2':
            self.grid_size = (10, 10)
            self.num_players = 2
            self.start_positions = [(0, 0), (9, 9)]
            self.random_movement = True
        elif mode == '3-5':
            self.grid_size = (10, 10)  # Can be set by students
            self.num_players = 2  # Can be 2, 3, or 4
            self.start_positions = [(0, 0), (9, 9), (0, 9), (9, 0)]  # Can be set by students
            self.random_movement = False
        elif mode == '6-8':
            self.grid_size = (10, 10)  # Can be set by students
            self.num_players = 2  # Can be 2, 3, or 4
            self.start_positions = [(0, 0), (9, 9), (0, 9), (9, 0)]  # Can be set by students
            self.random_movement = False
            self.experiments = True  # Additional feature for experiments

    def set_grid_size(self, width, height):
        self.grid_size = (width, height)

    def set_num_players(self, num_players):
        self.num_players = num_players

    def set_start_positions(self, positions):
        self.start_positions = positions
