from utils.configs.level import LevelConfig

class LevelUtil:
    @staticmethod
    def level_to_exp(level):
      return int(LevelConfig.EXP_SCALE * LevelConfig.CURVE_COEFFICIENT * (level ** 3)) 

    @staticmethod
    def exp_to_level(exp):
      return int((exp / (LevelConfig.EXP_SCALE * LevelConfig.CURVE_COEFFICIENT)) ** (1/3))