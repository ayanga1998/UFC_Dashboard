from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Fighter_Data(object):
    """
    Extracts historical data for a selected fighter in the dataset
    """

    def __init__(self, name):
        data = pd.read_csv('Data/UFC_dataset_clean.csv')
        data['date'] = pd.to_datetime(data['date'], format="%d-%Y-%m")
        data = data.set_index(data['date'])

        self.name = name
        self.data = data
        self.fighter_list = list(set(list(set(self.data.red_fighter)) + list((set(self.data.blue_fighter)))))
        print(len(self.fighter_list))
        if self.name not in self.fighter_list:
            raise Exception(f"{self.name} is not a fighter listed in the database")

        self.fight_data = self.get_fight_data()
        self.fighter_career_stats = self.career_data()

    def get_fight_data(self):
        mask = (self.data['red_fighter'] == self.name) | (self.data['blue_fighter'] == self.name)
        columns = ['event_title', 'date', 'location', 'title_bout', 'weight_class', 'result', 'method', 'fight_time',
                   'round']
        fighter = self.data[mask]

        # Create masks to filter fighter data
        blue_cols = [col for col in self.data.columns if 'blue' in col] + columns + ['red_fighter']
        red_cols = [col for col in self.data.columns if 'red' in col] + columns + ['blue_fighter']

        red_to_none = {col: col.replace('red_', '') for col in red_cols}
        red_to_none['blue_fighter'] = 'opponent'

        blue_to_none = {col: col.replace('blue_', '') for col in blue_cols}
        blue_to_none['red_fighter'] = 'opponent'

        blue_mask = (fighter['blue_fighter'] == self.name)
        red_mask = (fighter['red_fighter'] == self.name)

        fighter_blue = fighter.loc[blue_mask, blue_cols].rename(blue_to_none, axis=1)
        fighter_red = fighter.loc[red_mask, red_cols].rename(red_to_none, axis=1)

        fighter_df = pd.concat([fighter_blue, fighter_red]).sort_index()

        fighter_df['Win'] = np.where(fighter_df['result'] == self.name, 1, 0)
        fighter_df['Draw'] = np.where(fighter_df.result == 'D', 1, 0)
        fighter_df['Loss'] = np.where(fighter_df.result != self.name, 1, 0)
        return fighter_df

    def career_data(self):
        strikes = ['kd', 'ss_landed', 'ts_landed', 'head_landed', 'body_landed', 'leg_landed',
                   'dist_landed', 'clinch_landed', 'grnd_landed', 'rev', 'td_landed', 'ctrl_time', 'fight_time',
                   'Win', 'Draw', 'Loss']
        cumulative = self.fight_data.loc[:, strikes].aggregate('sum')
        return cumulative

if __name__ == "__main__":
    UFC = Fighter_Data('Khabib Nurmagomedov')
    print(UFC.fight_data.columns)

    # plt.plot(izzy.ss_pct)
    # plt.show()
