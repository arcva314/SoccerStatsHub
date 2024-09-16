import matplotlib.pyplot as plt
import pandas as pd

# Sample DataFrame
data = {
    'name': ['Player1', 'Player1', 'Player1', 'Player1', 'Player1', 'Player1',
             'Player1', 'Player1', 'Player1', 'Player1', 'Player1', 'Player1'],
    'season': [2018, 2018, 2019, 2019, 2020, 2020,
               2021, 2021, 2022, 2022, 2023, 2023],
    'competition': ['League1', 'League2', 'League1', 'League2', 'League1', 'League2',
                    'League1', 'League2', 'League1', 'League2', 'League1', 'League2'],
    'stat1': [10, 15, 20, 25, 30, 35, 5, 7, 8, 10, 12, 15],
    'stat2': [20, 25, 30, 35, 40, 45, 10, 12, 15, 17, 20, 25],
    'stat3': [30, 35, 40, 45, 50, 55, 15, 18, 20, 25, 30, 35]
}

df = pd.DataFrame(data)
print(df)
# List of key stats to plot
key_stats = ['stat1', 'stat2', 'stat3']

# Group by competition
competitions = df['competition'].unique()

num_competitions = len(competitions)
cols = 2  # You can adjust the number of columns
rows = (num_competitions + cols - 1) // cols  # This ensures enough rows to fit all subplots

# Create subplots
fig, axes = plt.subplots(rows, cols, figsize=(14, 8))
axes = axes.flatten()  # Flatten the axes array for easy iteration

for idx, competition in enumerate(competitions):
    comp_df = df[df['competition'] == competition]

    for stat in key_stats:
        axes[idx].plot(comp_df['season'], comp_df[stat], marker='o', label=stat)

    axes[idx].set_title(f'{competition}')
    axes[idx].set_xlabel('Season')
    axes[idx].set_ylabel('Value')
    axes[idx].legend(title="Key Stats")
    axes[idx].grid(True)

#plt.tight_layout()
plt.show()