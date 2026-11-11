#pragma once
#include <chrono>
#include <random>
#include "position.h"
#include "bot.h"
#include "heuristics.h"

// Random mid-game position after `plies` moves (retries if the game ends early)
Position randomPosition(mt19937& rng, int plies) {
  while (true) {
    Position p;
    bool ok = true;
    for (int i = 0; i < plies && ok; i++) {
      u64 moves = p.legalMoves();
      vector<u64> choices;
      for (int c = 0; c < 7; c++)
        if (u64 m = moves & colMask(c)) choices.push_back(m);
      if (choices.empty()) { ok = false; break; }
      p = p.after(choices[rng() % choices.size()]);
      if (p.lastMoverWon()) ok = false;
    }
    if (ok) return p;
  }
}

template <class F>
double timeMs(F&& f) {
  auto t0 = chrono::steady_clock::now();
  f();
  return chrono::duration<double, milli>(chrono::steady_clock::now() - t0).count();
}

void benchmark() {
  mt19937 rng(12345);
  vector<Position> positions;
  for (int i = 0; i < 10; i++) positions.push_back(Position{});
  
  
  for (int depth : {5, 6, 7, 8, 9, 10, 11, 12, 13, 14}) {
    // Baseline: no TT
    {
      unique_ptr<Bot> bot1 = make_unique<SearchBot<Random>>(Random{}, depth);
      double ms = timeMs([&] { for (auto& p : positions) bot1->chooseMove(p); });
      printf("depth %2d  noTT        %9.1f ms\n", depth, ms);
    }
    for (int bits = 10; bits <= 26; bits += 2) {
      double ctor = 0, search = 0;
      unique_ptr<Bot> bot2;
      
      ctor = timeMs([&] { bot2 = make_unique<SearchBotTT<Random>>(Random{}, depth, bits); });
      search = timeMs([&] { for (auto& p : positions) bot2->chooseMove(p); });
      printf("depth %2d  ttBits %2d   ctor %7.1f ms   search %9.1f ms\n",
             depth, bits, ctor, search);
    }
  }
}

int main() {
  benchmark();
  return 0;
}