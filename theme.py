import importlib
color_module = importlib.import_module("color")#no extra modules

class Theme:

    def __init__(self, light_bg, dark_bg, 
                       light_trace, dark_trace,
                       light_moves, dark_moves):
        
        self.bg = color_module.Color(light_bg, dark_bg)
        self.trace = color_module.Color(light_trace, dark_trace)
        self.moves = color_module.Color(light_moves, dark_moves)
