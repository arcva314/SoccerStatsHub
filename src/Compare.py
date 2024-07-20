class Compare:
    def __init__(self, info_list):
        self.info_list = info_list

    def get_data_list(self, db_handler):
        player_data = [info.get_player_data(db_handler) for info in self.info_list]
        return player_data