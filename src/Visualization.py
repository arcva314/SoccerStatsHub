import re
from src import Database
class Visualization:
    def __init__(self, model, info):
        self.model = model
        self.info = info

    def extract_code_block(self, output):
        match = re.search(r"```[Pp]ython(.*?)```|```(.*?)```", output, re.DOTALL)
        print(match)
        if match:
            return match.group(1).strip()
        else:
            return None

    def create_line_separate_prompt(self, player_name, seasons, competitions, key_stats, vis_description):
        line_separate_prompt = f'''You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name", “season”, “competition”, {', '.join(key_stats)}.
    The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

    The user wants a line graph of the players stats. The user wants separate subplots for each competition.
    Follow these instructions carefully to write the code for the data visualization.
    1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
    (Code)
        key_stats = result.columns.difference(['name', 'season', 'competition']
        result[key_stats] = result[key_stats].astype(float)
    2. Group the result df by competition
    (Code)
        competitions = result['competition'].unique()
    3. Based on the number of competitions, calculate appropriate rows and columns for the subplots
    (Code)
        cols = 2 if len(competitions) > 2 else 1
        rows = (len(competitions + cols - 1) // cols
    4. Create the subplots based on the calculated rows and columns
    (Code)
        fig, axes = plt.subplots(rows, cols, figsize=(14,8))
        axes = axes.flatten()
    5. Iterate through and begin plotting. COPY THIS CODE EXACTLY PLEASE.
    ```Python
    fig.sup_title('Progression of Stats Separated by Competition')
    for idx, competition in enumerate(competitions): 
        comp_df = result[result['competition'] == competition]
            for stat in key_stats:
                axes[idx].plot(comp_df['season'], comp_df[stat], marker='o', label=stat)  
            axes[idx].set_title(f'{{competition}}') 
            axes[idx].set_xlabel('Season')   
            axes[idx].set_ylabel('Value')
            axes[idx].legend(title="Key Stats")
            axes[idx].grid(True)```
    6. Save the image as a 64-bit string. Follow this code.
    (Code)
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)
    '''
        return line_separate_prompt

    def create_bar_separate_prompt(self, player_name, seasons, competitions, key_stats, description):
        prompt = f'''
    You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
    The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

    The user wants a bar graph of the player’s stats. The user wants separate subplots for each competition.
    Follow these instructions carefully to best execute the user’s request.
    1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
    (Code)
        key_stats = result.columns.difference(['name', 'season', 'competition'])
        result[key_stats] = result[key_stats].astype(float)
    2. Group the result df by competition
    (Code)
        competitions = result['competition'].unique()
    3. Based on the number of competitions, calculate the rows and columns for the subplots
    (Code)
        cols = 2 if len(competitions) > 2 else 1
        rows = (len(competitions) + cols - 1) // cols
    4. Create the subplots based on the calculated rows and columns
    (Code)
        fig, axs = plt.subplots(rows, cols, figsize=(14,8))
    5. Iterate through and plot. PLEASE COPY THIS CODE EXACTLY. DO NOT CHANGE ANYTHING.
    (Code)
    ```Python
    for i, comp in enumerate(competitions): 
        comp_data = result[result['competition'] == comp] 
        avg_values = comp_data[key_stats].astype(float).mean()
        #axs only has a 1 dimensional index. Please do not make any attempt to use 2 dimensional indexing. 
        axs[i].bar(key_stats, avg_values) 
        axs[i].set_title(f'Competition: {{comp}}') 
        axs[i].set_xlabel('Key Stats') 
        axs[i].set_ylabel('Average Value') 
    ```
    6. Save the image
    (Code)
        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        plt.close(fig)
    '''
        return prompt

    def create_bar_aggregate_prompt(self, player_name, seasons, competitions, key_stats, description):
        prompt = f'''
    You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
    The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

    The user wants a bar graph of the player’s stats.
    Follow these instructions carefully to best execute the user’s request.
    1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
    (Code)
        key_stats = result.columns.difference(['name', 'season', 'competition'])
        result[key_stats] = result[key_stats].astype(float)
    2. Group the result df by season and sum across all competitions
    (Code)
        summed_values_per_season = result.groupby(['season'])[key_stats].sum()
    3. Average the summed values
    (Code)
        avg_values = summed_values_per_season.mean()
    4. Plot
    ```Python
    plt.figure(figsize=(10, 6))
    plt.bar(key_stats, avg_values)
    plt.title('Average Sum of Key Stats Across All Competitions and Seasons')
    plt.xlabel('Key Stats')
    plt.ylabel('Average Summed Value')
    ```
    5. Save the image
    (Code)
        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        plt.close()
    '''
        return prompt

    def create_line_aggregate_prompt(self, player_name, seasons, competitions, key_stats, description):
        prompt = f'''
    You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
    The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

    The user wants a line graph of the player’s stats.
    Follow these instructions carefully to best execute the user's request.
    1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
    (Code)
        key_stats = result.columns.difference(['name', 'season', 'competition'])
        result[key_stats] = result[key_stats].astype(float)
    2. Group the result df by season and sum across all competitions.
    (Code)
        grouped_df = result.groupby([“season”])[key_stats].sum().reset_index()
        seasons = grouped_df['season']
        grouped_df = grouped_df[key_stats]
    3. Plot
    ```Python
    plt.figure(figsize=(14, 8))
    for stat in grouped_df.columns:
        plt.plot(seasons, grouped_df[stat], marker='o', label=stat)
        plt.xlabel("Season")
        plt.ylabel("Aggregated Statistic")
        plt.title("Aggregated Statistics Across All Competitions by Season")
        plt.legend()
    ```
    4. Save the image
    (Code)
        img_io = BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        plt.close()
    '''
        return prompt
    def generate_visualization(self, params):
        graph_type = params['graphType']
        plot_type = params['plotType']
        name = self.info.name
        seasons = self.info.seasons
        competitions = self.info.competitions
        key_stats = self.info.key_stats
        func = None
        if graph_type == 'progression' and plot_type == 'multiple':
            func = self.create_line_separate_prompt
        elif graph_type == 'progression' and plot_type == 'aggregated':
            func = self.create_line_aggregate_prompt
        elif graph_type == 'bar' and plot_type == 'multiple':
            func = self.create_bar_separate_prompt
        elif graph_type == 'bar' and plot_type == 'aggregated':
            func = self.create_bar_aggregate_prompt
        prompt = func(name, seasons, competitions, key_stats, "")
        output = self.model.invoke(prompt)
        print(output)
        code_block = self.extract_code_block(output)
        print(code_block)
        return code_block

    def generate_non_llm(self, params):
        graph_type = params['graphType']
        plot_type = params['plotType']
        group_by = 'sum'
        if plot_type == 'aggregated':
            group_by = 'sum'
        elif plot_type == 'averaged':
            group_by = 'mean'
        line_sep = f'''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
competitions = result['competition'].unique()
cols = 2 if len(competitions) > 2 else 1
rows = (len(competitions) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(14,8))
if len(competitions) == 1:
    axes = [axes]
for idx, competition in enumerate(competitions): 
    comp_df = result[result['competition'] == competition]
    for stat in key_stats:
        axes[idx].plot(comp_df['season'], comp_df[stat], marker='o', label=stat, color=colors[stat])  
        axes[idx].set_title(f'Competition: {{competition}}') 
        axes[idx].set_xlabel('Season')   
        axes[idx].set_ylabel('Value')
        axes[idx].legend(title="Key Stats")
        axes[idx].grid(True)
fig.suptitle("Progression of Key Stats Across Competitions for " + player_name)
fig.tight_layout()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close(fig)'''
        bar_sep = f'''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
competitions = result['competition'].unique()
colorings = [colors[stat] for stat in key_stats]
cols = 2 if len(competitions) > 2 else 1
rows = (len(competitions) + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(14,8))
if len(competitions) == 1:
    axs = [axs]
for i, comp in enumerate(competitions): 
    comp_data = result[result['competition'] == comp] 
    avg_values = comp_data[key_stats].astype(float).mean()
    #axs only has a 1 dimensional index. Please do not make any attempt to use 2 dimensional indexing. 
    axs[i].bar(key_stats, avg_values, color=colorings) 
    axs[i].set_title(f'Competition: {{comp}}') 
    axs[i].set_xlabel('Key Stats') 
    axs[i].set_ylabel('Average Value')
fig.suptitle("Average of Key Stats Across " + ', '.join(player_seasons) + " for " + player_name)
fig.tight_layout()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close(fig)
    '''
        line_agg = f'''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
grouped_df = result.groupby(['season'])[key_stats].{group_by}().reset_index()
seasons = grouped_df['season']
grouped_df = grouped_df[key_stats]
plt.figure(figsize=(14, 8))
for stat in grouped_df.columns:
    plt.plot(seasons, grouped_df[stat], marker='o', label=stat, color=colors[stat])
    plt.xlabel("Season")
    plt.ylabel("{plot_type.capitalize()} Statistic")
    plt.title("{plot_type.capitalize()} Statistics for " + player_name + " Across " + ', '.join(player_competitions))
    plt.legend()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close()
    '''
        bar_agg = f'''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
summed_values_per_season = result.groupby(['season'])[key_stats].{group_by}()
avg_values = summed_values_per_season.mean()
colorings = [colors[stat] for stat in key_stats]
plt.figure(figsize=(10, 6))
plt.bar(key_stats, avg_values, color=colorings)
plt.title("{plot_type.capitalize()[:-1]} of Key Stats Across " + ', '.join(player_competitions) + " Averaged Across " + ', '.join(player_seasons) + " for " + player_name)
plt.xlabel('Key Stats')
plt.ylabel('Average {plot_type.capitalize()} Value')
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close()
    '''
        code_block = ''
        if graph_type == 'progression' and plot_type == 'multiple':
            code_block = line_sep
        elif graph_type == 'progression' and plot_type in ('aggregated', 'averaged'):
            code_block = line_agg
        elif graph_type == 'bar' and plot_type == 'multiple':
            code_block = bar_sep
        elif graph_type == 'bar' and plot_type in ('aggregated', 'averaged'):
            code_block = bar_agg
        return code_block
    def generate_manager(self, params):
        graph_type = params['graphType']
        line = f'''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season'])
result[key_stats] = result[key_stats].astype(float)
plt.figure(figsize=(10, 8))
for stat in key_stats:
    plt.plot(result['season'], result[stat], marker='o', label=stat, color=manager_colors[stat])  
    plt.title('Progression of Stats for ' + manager_name) 
    plt.xlabel('Season')   
    plt.ylabel('Value')
    plt.legend(title="Key Stats")
    plt.grid(True)
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close()
'''
        bar = '''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season'])
result[key_stats] = result[key_stats].astype(float)
colorings = [manager_colors[stat] for stat in key_stats]
avg_values = result[key_stats].mean()
plt.figure(figsize=(10,8))
plt.bar(key_stats, avg_values, color=colorings) 
plt.title('Average of Key Stats Across ' + ', '.join(manager_seasons) + ' for ' + manager_name) 
plt.xlabel('Key Stats') 
plt.ylabel('Average Value')
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
images.append(img_base64)
plt.close()
'''
        return line if graph_type == 'progression' else bar

