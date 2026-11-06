#pragma once
#include <cstdint>
#include <bit>
using namespace std;
using u64 = uint64_t;

constexpr u64 ROW_0_MASK = 0x40810204081ULL;
constexpr u64 BOARD_MASK  = ROW_0_MASK * 63;
constexpr u64 colMask(int c) { return u64(63) << (c * 7); }

inline bool hasWon(u64 b) {
  for (int s : {1, 7, 6, 8}) {
    u64 m = b & (b >> s);
    if (m & (m >> (2 * s))) return true;
  }
  return false;
}

inline int getIfWinType(u64 b) {
  int winType = 0;
  constexpr int directions[4] = {7, 1, 8, 6};
  for (int i = 0; i < 4; i++) {
    u64 m = b & (b >> directions[i]);
    if (m & (m >> (2 * directions[i]))) {
      winType |= 0b1 << i;
    }
  }
  return winType;
}

struct Position {
  u64 bb[2] = {0, 0};
  int moves = 0;

  u64 occupied() const   { return bb[0] | bb[1]; }
  u64 legalMoves() const { return (occupied() + ROW_0_MASK) & BOARD_MASK; }   // carry trick: each column has no gaps
  Position after(u64 move) const {    // Doesn't modify the original, only returns a copy
    Position p = *this;
    p.bb[moves & 1] |= move;
    ++p.moves;
    return p;
  }
  bool lastMoverWon() const { return hasWon(bb[(moves & 1) ^ 1]); }
  int lastMoverWinType() const { return getIfWinType(bb[(moves & 1) ^ 1]); }
};