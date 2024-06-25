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
Files should be run in the following order:
1. `three_player_polytope_extrema.py` - computes the extremal points of the binary three-party no-signalling polytope,
2. `filter_three_player_strategies.py` - uses symmetry to reduce the number of relevant classical and no-signalling strategies,
3. `max_gap.py` (numeric) or `Three-party binary LSSD.nb` (exact) - solves 174 linear programs to determine that there is no separation between classical and no-signalling strategies.

It is also possible to run the files separately as long as the required `*.txt` files are present in the current directory: 
* `filter_three_player_strategies.py` requires `three_player_vertices.txt`,
* `max_gap.py` and `Three-party binary LSSD.nb` require `relevant_det_strats.txt` and `three_player_all_relevant_strats.txt`.

Keep in mind that running `three_player_polytope_extrema.py` takes a long time (about 30 minutes).

#### Example 1:
To recreate the figures, run `example1.py`.
It is also possible to create different figures by changing the parameters passed to `create_graph()`.
It is also possible to find classical and no-signaling winning probabilities for specific alpha and number of copies by running either `classical.py` or `nosignalling.py` (and changing the parameters within those files).

The classical value for two and three repetitions of the game is obtained in
* `BSC classical strategy n=2.nb` (2 repetitions),
* `BSC classical strategy n=3.nb` (3 repetitions),
while the solutions of the corresponding no-signalling linear programs are verified in
* `BSC no-signalling strategy n=2.nb` (2 repetitions),
* `BSC no-signalling strategy n=3.nb` (3 repetitions).

#### NPA_hierarchy_BSC_Game.py
This program implements the level '1+AB' of the NPA hierarchy to see that the binary symmetric channel game for local simultaneous state discrimination has no quantum advantage when played twice in parallel.
