from utils.configs.level import LevelConfig


class LevelUtil:
    @staticmethod
    def level_to_exp(level):
        return int(LevelConfig.EXP_SCALE * LevelConfig.CURVE_COEFFICIENT * (level**3))

    @staticmethod
    def exp_to_level(exp):
        return int(
            (exp / (LevelConfig.EXP_SCALE * LevelConfig.CURVE_COEFFICIENT)) ** (1 / 3)
        )
    
    @staticmethod
    def exp_to_next_level(current_exp):
        current_level = LevelUtil.exp_to_level(current_exp)
        next_level = current_level + 1
        next_level_total_exp = LevelUtil.level_to_exp(next_level)
        remaining_exp = next_level_total_exp - current_exp

        return remaining_exp
    
    @staticmethod
    def percent_of_remaining_exp(current_exp):
        current_level = LevelUtil.exp_to_level(current_exp)
        current_level_start_exp = LevelUtil.level_to_exp(current_level)
        next_level_total_exp = LevelUtil.level_to_exp(current_level + 1)
        exp_needed_for_current_level = next_level_total_exp - current_level_start_exp
        exp_earned_in_current_level = current_exp - current_level_start_exp
        
        if exp_needed_for_current_level <= 0:
            return 100.0
        
        progress = (exp_earned_in_current_level / exp_needed_for_current_level) * 100
        
        return min(100.0, progress)