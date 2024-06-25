# Parallel repetition of LSSD
This is repository consists of all the code used for the paper ["Parallel repetition of local simultaneous state discrimination"](https://arxiv.org/abs/2211.06456). The folder **Example 1** corresponds to Section 4 and so does `NPA_hierarchy_BSC_Game.py`, the folder **Three-party binary LSSD** corresponds to Appendix C.

## Usage:
#### Install dependencies:
```bash
pip3 install -r requirements.txt
```
#### Running a file:
```bash
python3 fileName.py
```
#### Three-party binary LSSD:
Files should be run in the following order: `three_player_polytope_extrema.py` then `filter_three_player_strategies.py` then `max_gap.py`. 
It is also possible to run the files separately as long as the `required .txt` files are present in the current directory: 
`filter_three_player_strategies.py` requires `three_player_vertices.txt` and
`max_gap.py` requires `relevant_det_strats.txt` and `three_player_all_relevant_strats.txt`.
To solve the 174 linear programs exactly, you can use `Three-party binary LSSD.nb` which requires the same two files as `max_gap.py`.

Keep in mind that running `three_player_polytope_extrema.py` takes a long time (about 30 minutes).

#### Example 1:
To recreate the figures in my thesis, run `example1.py`.
It is possible to create different figures, by changing the parameters passed to `create_graph()`.
It is also possible to find classical and no-signaling winning probabilities for specific alpha and number of copies by running either `classical.py` or 
`nosignalling.py` (and changing the parameters within those files).

The classical value for two and three repetitions of the game is obtained in `BSC classical strategy n=2.nb` and `BSC classical strategy n=3.nb`, respectively, while the corresponding no-signalling values are verified in `BSC no-signalling strategy n=2.nb` and `BSC no-signalling strategy n=2.nb`, respectively.

#### NPA_hierarchy_BSC_Game.py
We implement the level `1+AB' of the NPA hierarchy to see that the binary symmetric channel game for local simultaneous state discrimination has no quantum advantage when played twice in parallel.
