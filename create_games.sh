#!/bin/bash

bots=("random" "always_center" "always_high" "always_low" "always_left" "always_right")
heuristics=("none" "near_center" "far_up" "far_down" "far_left" "far_right")

# Everyone else
for b1 in 2 3 4 5; do
  for b2 in 0; do
  # for b2 in 0 1 2 3 4 5; do
    bot1=${bots[b1]}
    heuristic1=${heuristics[b1]}
    bot2=${bots[b2]}
    heuristic2=${heuristics[b2]}

    python games_generator.py $bot1 $bot2 \
      "${bot1}_v_${bot2}" \
      -n=100000

    for d1 in 1 2 3 4; do
      if [[ $d1 -lt 3 ]]; then
        python games_generator.py minimax_$heuristic1 $bot2 \
          "minimax_${heuristic1}_d${d1}_v_${bot2}" \
          -n=100000 -d1=$d1
        python games_generator.py $bot1 minimax_$heuristic2 \
          "${bot1}_v_minimax_${heuristic2}_d${d1}" \
          -n=100000 -d2=$d1
      else
        python games_generator.py minimax_$heuristic1 $bot2 \
          "minimax_${heuristic1}_d${d1}_v_${bot2}" \
          -n=10000 -d1=$d1
        python games_generator.py $bot1 minimax_$heuristic2 \
          "${bot1}_v_minimax_${heuristic2}_d${d1}" \
          -n=10000 -d2=$d1
      fi
    done

    for d1 in 1 2 3 4; do
      for d2 in 1 2 3 4; do

        if [[ $d1 -lt 3 && $d2 -lt 3 ]]; then
          python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
            "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
            -n=100000 -d1=$d1 -d2=$d2
        else
          python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
            "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
            -n=10000 -d1=$d1 -d2=$d2
        fi

      done
    done
  done
done


# # always_center_v partial done
# for b2 in 1 2; do
#   bot1=${bots[1]}
#   heuristic1=${heuristics[1]}
#   bot2=${bots[b2]}
#   heuristic2=${heuristics[b2]}

#   python games_generator.py $bot1 $bot2 \
#     "${bot1}_v_${bot2}" \
#     -n=100000

#   for d1 in 1 2; do
#     for d2 in 3 4; do

#       if [[ $d1 -lt 3 && $d2 -lt 3 ]]; then
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=100000 -d1=$d1 -d2=$d2
#       else
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=10000 -d1=$d1 -d2=$d2
#       fi

#     done
#   done
  
#   for d1 in 3 4; do
#     for d2 in 1 2 3 4; do

#       if [[ $d1 -lt 3 && $d2 -lt 3 ]]; then
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=100000 -d1=$d1 -d2=$d2
#       else
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=10000 -d1=$d1 -d2=$d2
#       fi

#     done
#   done
# done

# # always_center_v the rest
# for b2 in 3 4 5; do
#   bot1=${bots[1]}
#   heuristic1=${heuristics[1]}
#   bot2=${bots[b2]}
#   heuristic2=${heuristics[b2]}

#   python games_generator.py $bot1 $bot2 \
#     "${bot1}_v_${bot2}" \
#     -n=100000

#   for d1 in 1 2 3 4; do
#     if [[ $d1 -lt 3 ]]; then
#       python games_generator.py minimax_$heuristic1 $bot2 \
#         "minimax_${heuristic1}_d${d1}_v_${bot2}" \
#         -n=100000 -d1=$d1
#       python games_generator.py $bot1 minimax_$heuristic2 \
#         "${bot1}_v_minimax_${heuristic2}_d${d1}" \
#         -n=100000 -d2=$d1
#     else
#       python games_generator.py minimax_$heuristic1 $bot2 \
#         "minimax_${heuristic1}_d${d1}_v_${bot2}" \
#         -n=10000 -d1=$d1
#       python games_generator.py $bot1 minimax_$heuristic2 \
#         "${bot1}_v_minimax_${heuristic2}_d${d1}" \
#         -n=10000 -d2=$d1
#     fi
#   done

#   for d1 in 1 2 3 4; do
#     for d2 in 1 2 3 4; do

#       if [[ $d1 -lt 3 && $d2 -lt 3 ]]; then
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=100000 -d1=$d1 -d2=$d2
#       else
#         python games_generator.py minimax_$heuristic1 minimax_$heuristic2 \
#           "minimax_${heuristic1}_d${d1}_v_minimax_${heuristic2}_d${d2}" \
#           -n=10000 -d1=$d1 -d2=$d2
#       fi

#     done
#   done
# done

