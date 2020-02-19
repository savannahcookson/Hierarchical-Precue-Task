round=$1
runs=$2
session=$3

make_random_timing.py -run_time 246 \
-num_stim 32 \
-stim_labels 2OL_C 2OL_S 2SL_C 2SL_S 2OR_C 2OR_S 2SR_C 2SR_S \
      1HOL_C 1HOL_S 1HSL_C 1HSL_S 1HOR_C 1HOR_S 1HSR_C 1HSR_S \
      1JOL_C 1JOL_S 1JSL_C 1JSL_S 1JOR_C 1JOR_S 1JSR_C 1JSR_S \
      0OL_C 0OL_S 0SL_C 0SL_S 0OR_C 0OR_S 0SR_C 0SR_S \
-stim_dur 1.9 \
-ordered_stimuli 1 2 \
-ordered_stimuli 3 4 \
-ordered_stimuli 5 6 \
-ordered_stimuli 7 8 \
-ordered_stimuli 9 10 \
-ordered_stimuli 11 12 \
-ordered_stimuli 13 14 \
-ordered_stimuli 15 16 \
-ordered_stimuli 17 18 \
-ordered_stimuli 19 20 \
-ordered_stimuli 21 22 \
-ordered_stimuli 23 24 \
-ordered_stimuli 25 26 \
-ordered_stimuli 27 28 \
-ordered_stimuli 29 30 \
-ordered_stimuli 31 32 \
-num_reps 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 \
-num_runs $runs \
-min_rest .25 \
-tr 2.0 \
-prefix ${round}_${session} \
-save_3dd_cmd rm_design_test.sh
