from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from src import Info, Database
import re
import base64
import sqlite3
def get_db_connection():
    conn = sqlite3.connect('../SoccerStatsHub.db')
    conn.row_factory = sqlite3.Row
    return conn
db_handler = get_db_connection()
player = Info.Info('Lionel Messi', ['2011/2012', '2018/2019', '2014/2015', '2010/2011', '2016/2017'], ['UCL', 'SLL'], ['Goals', 'Assists', 'MotM', 'Rating'])
result = player.get_player_data(db_handler)
result = result.applymap(lambda x: '0' if x == '-' else x)
def create_line_separate_prompt(player_name, seasons, competitions, key_stats, vis_description):
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
for idx, competition in enumerate(competitions): 
    comp_df = result[result['competition'] == competition]
    print(comp_df)
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
def create_bar_separate_prompt(player_name, seasons, competitions, key_stats, description):
    prompt = f'''
You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

The user wants a bar graph of the player’s stats. The user wants separate subplots for each competition.
Follow these instructions carefully to best execute the user’s request.
1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
(Code)
    key_stats = result.columns.difference(['name', 'season', 'competition']
2. Group the result df by competition
(Code)
    competitions = result['competition'].unique()
3. Based on the number of competitions, calculate the rows and columns for the subplots
(Code)
    cols = 2 if len(competitions) > 2 else 1
    rows = (len(competitions) + cols - 1) // cols
4. Create the subplots based on the calculated rows and columns
(Code)
    fig, axs = plt.subplots(row, col, figsize=(14,8))
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
def create_bar_aggregate_prompt(player_name, seasons, competitions, key_stats, description):
    prompt = f'''
You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

The user wants a bar graph of the player’s stats.
Follow these instructions carefully to best execute the user’s request.
1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
(Code)
    key_stats = result.columns.difference(['name', 'season', 'competition']
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
    plt.close(fig)
'''
    return prompt
def create_line_aggregate_prompt(player_name, seasons, competitions, key_stats, description):
    prompt =  f'''
You are a Python data visualization expert capable of generating code for data visualization. The user has provided data that has these columns: “name”, “season”, “competition”, {', '.join(key_stats)}.
The data is already stored in a dataframe called result. Please do not make any attempt to load the data as it will result in an error.

The user wants a line graph of the player’s stats.
Follow these instructions carefully to best execute the user's request.
1. Get the key stats. PLEASE COPY THIS CODE EXACTLY. THE NAMES OF THE COLUMNS MUST MATCH.
(Code)
    key_stats = result.columns.difference(['name', 'season', 'competition']
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
    plt.close(fig)
'''
    return prompt
def extract_code_block(output):
    match = re.search(r"`[Pp]ython(.*?)`", output, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None
def generate_non_llm(params):
    graph_type = params['graphType']
    plot_type = params['plotType']
    line_sep = '''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
competitions = result['competition'].unique()
cols = 2 if len(competitions) > 2 else 1
rows = (len(competitions) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(14,8))
axes = axes.flatten()
for idx, competition in enumerate(competitions): 
    comp_df = result[result['competition'] == competition]
    for stat in key_stats:
        axes[idx].plot(comp_df['season'], comp_df[stat], marker='o', label=stat, color=colors[stat])  
        axes[idx].set_title(f'{competition}') 
        axes[idx].set_xlabel('Season')   
        axes[idx].set_ylabel('Value')
        axes[idx].legend(title="Key Stats")
        axes[idx].grid(True)
plt.show()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
plt.close(fig)'''
    bar_sep = '''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
competitions = result['competition'].unique()
cols = 2 if len(competitions) > 2 else 1
rows = (len(competitions) + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(14,8))
for i, comp in enumerate(competitions): 
    comp_data = result[result['competition'] == comp] 
    avg_values = comp_data[key_stats].astype(float).mean()
    #axs only has a 1 dimensional index. Please do not make any attempt to use 2 dimensional indexing. 
    axs[i].bar(key_stats, avg_values, color=[colors[stat] for stat in key_stats]) 
    axs[i].set_title(f'Competition: {comp}') 
    axs[i].set_xlabel('Key Stats') 
    axs[i].set_ylabel('Average Value')
plt.show()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
plt.close(fig)
    '''
    line_agg = '''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
grouped_df = result.groupby(['season'])[key_stats].sum().reset_index()
seasons = grouped_df['season']
grouped_df = grouped_df[key_stats]
plt.figure(figsize=(14, 8))
for stat in grouped_df.columns:
    plt.plot(seasons, grouped_df[stat], marker='o', label=stat, color=colors[stat])
    plt.xlabel("Season")
    plt.ylabel("Aggregated Statistic")
    plt.title("Aggregated Statistics Across All Competitions by Season")
    plt.legend()
plt.show()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
plt.close()
    '''
    bar_agg = '''import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
key_stats = result.columns.difference(['name', 'season', 'competition'])
result[key_stats] = result[key_stats].astype(float)
summed_values_per_season = result.groupby(['season'])[key_stats].sum()
avg_values = summed_values_per_season.mean()
plt.figure(figsize=(10, 6))
plt.bar(key_stats, avg_values, color=[colors[stat] for stat in key_stats])
plt.title('Average Sum of Key Stats Across All Competitions and Seasons')
plt.xlabel('Key Stats')
plt.ylabel('Average Summed Value')
plt.show()
img_io = BytesIO()
plt.savefig(img_io, format='png')
img_io.seek(0)
img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
plt.close()
'''
    code_block = ''
    if graph_type == 'progression' and plot_type == 'multiple':
        code_block = line_sep
    elif graph_type == 'progression' and plot_type == 'aggregated':
        code_block = line_agg
    elif graph_type == 'bar' and plot_type == 'multiple':
        code_block = bar_sep
    elif graph_type == 'bar' and plot_type == 'aggregated':
        code_block = bar_agg
    return code_block

#prompt = create_bar_aggregate_prompt(player.name, player.seasons, player.competitions, player.key_stats, "Grouped bar graph with color red for goals, yellow for assists, purple for rating, and orange for MotM and include light blue background. The x-axis will have each of the seasons and for each season, have columns for each of the key stats. Have one plot for UCL data, and a separate plot for SLL data")
#llm = Ollama(model='llama3')
#output = llm.invoke(prompt)
params = {'graphType': 'bar', 'plotType': 'multiple', 'colors': {'Goals':'#4f5612', 'Assists': '#c25150', 'MotM': '#999999', 'Rating': '#8e4172'}}
colors = params['colors']
code_block = generate_non_llm(params)
if code_block:
    print(code_block)
    exec(code_block)
    #with open("output.png", "wb") as f:
        #f.write(base64.b64decode(img_base64))
else:
    print("GAY")