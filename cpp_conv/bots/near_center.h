#pragma once
#include "../Position.h"
using namespace std;

struct NearCenter {
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return 3 * (popcount(me & colMask(3)) - popcount(opp & colMask(3)));
  }
  
};