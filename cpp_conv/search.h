#pragma once
#include <concepts>
#include <algorithm>
#include "Position.h"

template <class T>
concept Heuristic = requires(const T h, const Position& p) {
    { h.evaluate(p) } -> std::convertible_to<int>;
};

template <Heuristic Heur>
class Search {
public:
    Search(Heur h, int depth) : heur(h), maxDepth(depth) {}

    int bestMove(const Position& root) {          // returns a column 0-6
        int bestCol = -1, bestScore = -INF, alpha = -INF;
        u64 moves = root.legalMoves();
        for (int c : ORDER) {
            u64 m = moves & colMask(c);
            if (!m) continue;
            int score = -negamax(root.after(m), maxDepth - 1, -INF, -alpha, 1);
            if (score > bestScore) { bestScore = score; bestCol = c; }
            alpha = std::max(alpha, score);
        }
        return bestCol;
    }

private:
    static constexpr int INF = 1'000'000, WIN = 100'000;
    static constexpr int ORDER[7] = {3, 2, 4, 1, 5, 0, 6};

    int negamax(const Position& p, int depth, int alpha, int beta, int ply) {
        if (p.lastMoverWon()) return -(WIN - ply);   // side to move has lost
        u64 moves = p.legalMoves();
        if (!moves) return 0;                        // board full: draw
        if (depth == 0) return heur.evaluate(p);     // inlined at compile time

        int best = -INF;
        for (int c : ORDER) {
            u64 m = moves & colMask(c);
            if (!m) continue;
            int score = -negamax(p.after(m), depth - 1, -beta, -alpha, ply + 1);
            best = std::max(best, score);
            alpha = std::max(alpha, score);
            if (alpha >= beta) break;                // prune
        }
        return best;
    }

    Heur heur;
    int maxDepth;
};