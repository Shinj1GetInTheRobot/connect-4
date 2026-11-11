#pragma once
#include "Search.h"
#include "Search_tt.h"
using namespace std;

// Abstract Bot Interface Class
struct Bot {
  virtual ~Bot() = default;
  virtual int chooseMove(const Position& p) = 0;
};

// Specific Bot for minimax search (without tt), given a heuristic
template <class Heur>
struct SearchBot : Bot {
  Search<Heur> search;
  SearchBot(Heur h, int depth) : search(h, depth) {}
  int chooseMove(const Position& p) override { return search.getBestMove(p); }
};

// Specific Bot for minimax search (with tt), given a heuristic
template <class Heur>
struct SearchBotTT : Bot {
  SearchTT<Heur> search;
  // ttBits = 20 seems pretty good based on benchmarking results
  SearchBotTT(Heur h, int depth, int ttBits = 20) : search(h, depth, ttBits) {}
  int chooseMove(const Position& p) override { return search.getBestMove(p); }
};