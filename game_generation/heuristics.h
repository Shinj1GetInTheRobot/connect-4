#pragma once
#include "Position.h"
using namespace std;

struct Random { int evaluate(const Position& p) const { return 0; } };

struct Center {
  static constexpr u64 ONES = colMask(1) | colMask(5) | colMask(3);
  static constexpr u64 TWOS = colMask(2) | colMask(4) | colMask(3);
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return (popcount(me & ONES) - popcount(opp & ONES))
      + 2 * (popcount(me & TWOS) - popcount(opp & TWOS));
  }
};

struct High {
  static constexpr u64 ONES  = rowMask(1) | rowMask(3) | rowMask(5);
  static constexpr u64 TWOS  = rowMask(2) | rowMask(3);
  static constexpr u64 FOURS = rowMask(4) | rowMask(5);
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return (popcount(me & ONES) - popcount(opp & ONES))
      + 2 * (popcount(me & TWOS) - popcount(opp & TWOS))
      + 4 * (popcount(me & FOURS) - popcount(opp & FOURS));
  }
};

struct Low {
  static constexpr u64 ONES  = rowMask(4) | rowMask(2) | rowMask(0);
  static constexpr u64 TWOS  = rowMask(3) | rowMask(2);
  static constexpr u64 FOURS = rowMask(1) | rowMask(0);
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return (popcount(me & ONES) - popcount(opp & ONES))
      + 2 * (popcount(me & TWOS) - popcount(opp & TWOS))
      + 4 * (popcount(me & FOURS) - popcount(opp & FOURS));
  }
};

struct Left {
  static constexpr u64 ONES  = colMask(1) | colMask(3) | colMask(5);
  static constexpr u64 TWOS  = colMask(0) | colMask(3) | colMask(4);
  static constexpr u64 FOURS = colMask(0) | colMask(1) | colMask(2);
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return (popcount(me & ONES) - popcount(opp & ONES))
      + 2 * (popcount(me & TWOS) - popcount(opp & TWOS))
      + 4 * (popcount(me & FOURS) - popcount(opp & FOURS));
  }
};

struct Right {
  static constexpr u64 ONES  = colMask(5) | colMask(3) | colMask(1);
  static constexpr u64 TWOS  = colMask(6) | colMask(3) | colMask(2);
  static constexpr u64 FOURS = colMask(6) | colMask(5) | colMask(4);
  int evaluate(const Position& p) const {
    u64 me  = p.bb[p.moves & 1];
    u64 opp = p.bb[(p.moves & 1) ^ 1];
    return (popcount(me & ONES) - popcount(opp & ONES))
      + 2 * (popcount(me & TWOS) - popcount(opp & TWOS))
      + 4 * (popcount(me & FOURS) - popcount(opp & FOURS));
  }
};