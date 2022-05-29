# Jaron_Has_Bachelor_Project
This is repository consists of all the code used for my bachelor's thesis. Three_player_binary corresponds to chapter 4 and example1 to chapter 5.

## Usage:
#### Install dependencies:
```
pip3 install -r requirements.txt
```
#### Running a file:
```
python3 *.py
```
#### Three_player_binary:
Files should be run in the following order: three_player_polytope_extrema.py then filter_three_player_strategies.py then max_gap.py. 
It is also possible to run the files separately as long as the required .txt files are present in the current directory: 
filter_three_player_strategies.py requires three_player_vertices.txt and
max_gap.py requires relevant_det_strats.txt and three_player_all_relevant_strats.txt.

Keep in mind that running three_player_polytope_extrema.py takes a long time (about 30 minutes for me).

#### example1:
To recreate the figures in my thesis, run example1.py.
It is possible to create different figures, by changing the parameters passed to create_graph().
It is also possible to find classical and no-signaling winning probabilities for specific alpha and number of copies by running either classical.py or 
nosignalling.py (and changing the parameters within those files).
