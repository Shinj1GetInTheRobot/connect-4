#pragma once
#include "Search.h"
using namespace std;

// Abstract Bot Interface Class
struct Bot {
  virtual ~Bot() = default;
  virtual int chooseMove(const Position& p) = 0;
};

// Specific Bot for minimax search, given a heuristic
template <Heuristic Heur>
struct SearchBot : Bot {
  Search<Heur> search;
  SearchBot(Heur h, int depth) : search(h, depth) {}
  int chooseMove(const Position& p) override { return search.getBestMove(p); }
};