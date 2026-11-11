#pragma once
#include <concepts>
#include <algorithm>
#include <random>
#include "Position.h"
using namespace std;

template <class Heur>
class Search {
  public:
    Search(Heur h, int depth, unsigned seed = random_device{}()) 
      : heur(h), maxDepth(depth), rng(seed) {}

    int getBestMove(const Position& pos) {
      int bestCol = -1, bestScore = -INF, ties = 0;
      u64 moves = pos.legalMoves();
      for (int c : ORDER) {
        u64 move = moves & colMask(c);
        if (!move) continue;

        int alpha = (bestScore == -INF) ? -INF : bestScore - 1;     
          // check against (bestScore - 1) to allow consideration of tied moves
        int score = (maxDepth == 0) 
          ? -heur.evaluate(pos.after(move))
          : -negamax(pos.after(move), maxDepth - 1, -INF, -alpha);

        if (score > bestScore) {
          bestScore = score;
          bestCol = c;
          ties = 1;
        } else if (score == bestScore) {    // Reservoir Sampling
          ties++;
          if (rng() % ties == 0) bestCol = c;
        }
      }
      return bestCol;
    }

  private:
    static constexpr int INF = 1000000, WIN = 100000;
    static constexpr int ORDER[7] = {3, 2, 4, 1, 5, 0, 6};

    Heur heur;
    int maxDepth;
    mt19937 rng;

    int negamax(const Position& p, int depth, int alpha, int beta) {
      if (p.lastMoverWon()) return -(WIN + depth);
      u64 moves = p.legalMoves();
      if (!moves) return 0;
      if (depth == 0) return heur.evaluate(p);

      int best = -INF;
      for (int c : ORDER) {
        u64 move = moves & colMask(c);
        if (!move) continue;
        int score = -negamax(p.after(move), depth - 1, -beta, -alpha);
        best = max(best, score);
        alpha = max(alpha, score);
        if (alpha >= beta) break;
      }
      return best;
    }
    
};