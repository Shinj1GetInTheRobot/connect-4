#pragma once
#include "Search.h"
using namespace std;

struct Bot {
    virtual ~Bot() = default;
    virtual int chooseMove(const Position& p) = 0;   // returns a column
};

template <Heuristic Heur>
struct SearchBot : Bot {
    Search<Heur> search;
    SearchBot(Heur h, int depth) : search(h, depth) {}
    int chooseMove(const Position& p) override { return search.bestMove(p); }
};