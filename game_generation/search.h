#pragma once
#include <concepts>
#include <algorithm>
#include <random>
#include <vector>
#include <cstdint>
#include "Position.h"
using namespace std;

// Make the compiler check each heuristic has an evaluate() function that returns an int
template <class T>
concept Heuristic = requires(const T h, const Position& p) {
  { h.evaluate(p) } -> convertible_to<int>;
};

template <Heuristic Heur>
class Search {
  public:
    Search(Heur h, int depth, unsigned seed = random_device{}(), int ttBits = 22)
      : heur(h), maxDepth(depth), rng(seed),
        tt(size_t(1) << ttBits), ttMask((size_t(1) << ttBits) - 1) {}

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

    void clearTable() { fill(tt.begin(), tt.end(), Entry{}); }

  private:
    static constexpr int INF = 1000000, WIN = 100000;
    static constexpr int ORDER[7] = {3, 2, 4, 1, 5, 0, 6};

    Heur heur;
    int maxDepth;
    mt19937 rng;

    enum Flag : uint8_t { EXACT, LOWER, UPPER };
    struct Entry {
      u64 key = 0;          // a real key is never 0
      int32_t score = 0;
      int8_t depth = -1;    // depth used to overwrite table on subsequent searches
      uint8_t flag = EXACT;
    };
    vector<Entry> tt;
    size_t ttMask;

    size_t index(u64 key) const {
      return size_t((key * 0x9E3779B97F4A7C15ULL) >> 20) & ttMask;
    }

    // Negamax + Alpha-Beta + Transposition Table
    // https://en.wikipedia.org/wiki/Negamax#Negamax_with_alpha_beta_pruning_and_transposition_tables
    int negamax(const Position& p, int depth, int alpha, int beta) {
      if (p.lastMoverWon()) return -(WIN + depth);
      u64 moves = p.legalMoves();
      if (!moves) return 0;
      if (depth == 0) return heur.evaluate(p);

      const int alphaOrig = alpha;
      const u64 key = p.key();
      Entry& e = tt[index(key)];

      if (e.key == key && e.depth == int8_t(depth)) {   // Found this position before
        if (e.flag == EXACT) return e.score;
        if (e.flag == LOWER) alpha = max(alpha, e.score);
        else                 beta  = min(beta,  e.score);
        if (alpha >= beta) return e.score;
      }

      int best = -INF;
      for (int c : ORDER) {
        u64 move = moves & colMask(c);
        if (!move) continue;
        best = max(best, -negamax(p.after(move), depth - 1, -beta, -alpha));
        alpha = max(alpha, best);
        if (alpha >= beta) break;
      }

      e.key = key;
      e.score = best;
      e.depth = depth;
      e.flag = (best <= alphaOrig) ? UPPER : (best >= beta) ? LOWER : EXACT;
      return best;
    }
    
};