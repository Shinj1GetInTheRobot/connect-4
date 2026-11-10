#pragma once
#include <cstdint>
#include <bit>
using namespace std;
using u64 = uint64_t;

constexpr int COLS = 7;
constexpr int ROWS = 6;
constexpr u64 rowMask0() {
  u64 m = 0;
  for (int c = 0; c < COLS; ++c) m |= 1ULL << (c * (ROWS + 1));
  return m;
}
constexpr u64 BOARD_MASK = rowMask0() * ((1ULL << ROWS) - 1);
constexpr u64 colMask(int c) { return ((1ULL << ROWS) - 1) << (c * (ROWS + 1)); }
constexpr u64 rowMask(int r) { return rowMask0() << r; }

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
  u64 legalMoves() const { return (occupied() + rowMask0()) & BOARD_MASK; }   // carry trick: each column has no gaps
  Position after(u64 move) const {    // Doesn't modify the original, only returns a copy
    Position p = *this;
    p.bb[moves & 1] |= move;
    ++p.moves;
    return p;
  }
  bool lastMoverWon() const { return hasWon(bb[(moves & 1) ^ 1]); }
  int lastMoverWinType() const { return getIfWinType(bb[(moves & 1) ^ 1]); }
  // Unique key used for position transposition table
  // Key is a bitboard of the highest slot in each column + current player's pieces
  // (this can overflow into the sentinel row) 
  u64 key() const { return occupied() + rowMask0() + bb[moves & 1]; }
};