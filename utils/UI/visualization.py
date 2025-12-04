class VisualUtil:
    @staticmethod
    def create_progress_bar(percentage: float, length: int) -> str:
        total_fill = (percentage / 100) * length
        filled_blocks = int(total_fill)
        bar = ""
        bar += '█' * filled_blocks
        remaining_length = length - len(bar) 
        bar += '░' * remaining_length
        
        return bar[:length]