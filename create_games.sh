#!/bin/bash

bots=("random" "center" "high" "low" "left" "right")

# Everyone else
for b1 in 0 1 2 3 4 5; do
  for b2 in 0 1 2 3 4 5; do

    bot1=${bots[b1]}
    bot2=${bots[b2]}

    for d1 in 0 1 2 3 4 5 6 7 8 9 10; do
      for d2 in 0 1 2 3 4 5 6 7 8 9 10; do

        if [[ $d1 -eq 0 && $d2 -eq 0 ]]; then
          ./generate.exe "$bot1" "$bot2" "${bot1}_d${d1}_v_${bot2}_d${d2}" \
            -n=100000 -d1=$d1 -d2=$d2
        else
          ./generate.exe "$bot1" "$bot2" "${bot1}_d${d1}_v_${bot2}_d${d2}" \
            -n=10000 -d1=$d1 -d2=$d2
        fi

      done
    done
  done
done