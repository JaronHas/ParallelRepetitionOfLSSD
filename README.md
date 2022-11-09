# ParallelRepetitionOfLSSD
This is repository consists of all the code used for the paper "Parallel Repetition of LSSD". The folder "example1" corresponds to Section 4 and so does "NPA_hierarchy_BSC_Game.py", the folder "Three_player_binary" corresponds to Section 6.

## Usage:
#### Install dependencies:
```
pip3 install -r requirements.txt
```
#### Running a file:
```
python3 fileName.py
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

#### NPA_hierarchy_BSC_Game.py
We implement the level `1+AB' of the NPA hierarchy to see that the binary simmetric channel game for local simultaneus state discrimination has no quantum advantage when played twice in parallel.
