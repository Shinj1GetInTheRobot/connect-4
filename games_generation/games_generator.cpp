#include <iostream>
#include <fstream>
#include <string>
#include <memory>
#include <vector>
#include <stdexcept>
#include "Bot.h"
#include "Heuristics.h"
#include "Position.h"
using namespace std;

struct Config {
  int rows = 6;
  int cols = 7;
  int numGames = 100;
  int depth1 = 2;
  int depth2 = 2;
  string filename;
  string player1;
  string player2;
};

struct Game {
  vector<int> moves;
  int result;
  int winTypeBits;
};

// Returns whatever is after the '=' if arg starts with `prefix`, puts it into value.
static bool matchOption(const string& arg, const string& prefix, string& value) {
  if (arg.rfind(prefix, 0) == 0) {
    value = arg.substr(prefix.size());
    return true;
  }
  return false;
}

static int parseInt(const string& text, const string& optionName) {
  try {
    size_t used = 0;
    int v = stoi(text, &used);
    if (used != text.size()) throw invalid_argument("trailing characters");
    return v;
  } catch (const exception&) {
    throw invalid_argument("Invalid value for " + optionName + ": '" + text + "'");
  }
}

Config parseArgs(int argc, char* argv[]) {
  Config cfg;
  vector<string> positional;
  for (int i = 1; i < argc; i++) {
    string arg = argv[i];
    string value;
    if      (matchOption(arg, "-n=",  value))   cfg.numGames = parseInt(value, "-n");
    else if (matchOption(arg, "-rows=", value)) cfg.rows     = parseInt(value, "-rows");
    else if (matchOption(arg, "-cols=", value)) cfg.cols     = parseInt(value, "-cols");
    else if (matchOption(arg, "-d1=", value))   cfg.depth1   = parseInt(value, "-d1");
    else if (matchOption(arg, "-d2=", value))   cfg.depth2   = parseInt(value, "-d2");
    else if (!arg.empty() && arg[0] == '-')     throw invalid_argument("Unknown option: " + arg);
    else                                        positional.push_back(arg);
  }
  if (positional.size() != 3) {
    throw invalid_argument("Expected exactly 2 bots and a file name");
  };
  cfg.player1 = positional[0];
  cfg.player2 = positional[1];
  cfg.filename = positional[2];
  if (cfg.numGames < 1)                 throw invalid_argument("-n must be at least 1");
  if (cfg.depth1 < 0 || cfg.depth2 < 0) throw invalid_argument("depths must be at least 0");
  if (cfg.rows != 6 || cfg.cols != 7)   throw invalid_argument("Only 6 rows and 7 columns are supported");
  return cfg;
}

unique_ptr<Bot> makeBot(const string& name, int depth) {
  if      (name == "Random")   return make_unique<SearchBot<Random>>(Random{}, depth);
  else if (name == "Center")   return make_unique<SearchBot<NearCenter>>(NearCenter{}, depth);
  throw invalid_argument("Invalid bot: " + name);
}

void resetGame(Game& game) {
  game.moves.clear();
  game.result = 0;
  game.winTypeBits = 0;
}

void playNewGame(Game& game, Bot* bots[2]) {
  resetGame(game);
  Position pos;
  int col;
  while (pos.legalMoves()) {
    col = bots[pos.moves & 1]->chooseMove(pos);
    game.moves.push_back(col);
    pos = pos.after(pos.legalMoves() & colMask(col));
    if (pos.lastMoverWon()) {
      game.winTypeBits = pos.lastMoverWinType();
      game.result = ((pos.moves & 0b1) * 2) - 1;
      return;
    }
  }
}

string wTBtoStr(int wTB) {
  string winTypeStr = "";
  if (wTB & 0b0001) winTypeStr += "h";
  if (wTB & 0b0010) winTypeStr += winTypeStr.empty() ? "v"  : "+v";
  if (wTB & 0b0100) winTypeStr += winTypeStr.empty() ? "d1" : "+d1";
  if (wTB & 0b1000) winTypeStr += winTypeStr.empty() ? "d2" : "+d2";
  return winTypeStr;
}

void writeGame(ostream& out, int index, int rows, int cols,
  const string& player1name, const string& player2name, const Game& game, bool isFirst)
{
  if (!isFirst) out << ",\n";
  out << "  \"" << index << "\": {\n"
      << "    \"rows\": " << rows << ",\n"
      << "    \"columns\": " << cols << ",\n"
      << "    \"players\": {\"1\": \"" << player1name << "\", \"2\": \"" << player2name << "\"},\n"
      << "    \"moves\": [";
  for (size_t k = 0; k < game.moves.size(); k++)
      out << (k ? ", " : "") << game.moves[k];
  out << "],\n"
      << "    \"num_moves\": " << game.moves.size() << ",\n"
      << "    \"result\": " << game.result << ",\n"
      << "    \"winning_move_type\": \"" << wTBtoStr(game.winTypeBits) << "\"\n"
      << "  }";
}

string playerFullName(int i, Config cfg) {
  if (i == 1) return cfg.player1 + " D-" + to_string(cfg.depth1);
  return cfg.player2 + " D-" + to_string(cfg.depth2);
}

int main(int argc, char* argv[]) {
  // Read the command line args
  Config cfg;
  try {
    cfg = parseArgs(argc, argv);
  } catch (const exception& e) {
    cerr  << "Error: " << e.what() << "\n"
          << "Usage: " << argv[0]
          << " <heuristic1> <heuristic2> <filename> [-rows=ROWS] [-cols=COLS] [-n=GAMES] [-d1=DEPTH] [-d2=DEPTH]\n";
    return 1;
  }
  unique_ptr<Bot> bot1, bot2;
  try {
    bot1 = makeBot(cfg.player1, cfg.depth1);
    bot2 = makeBot(cfg.player2, cfg.depth2);
  } catch (const exception& e) {
    cerr << "Error: " << e.what() << "\n";
    return 1;
  }
  // Read was successful -> Playing games and writing to file...
  Bot* bots[2] = {bot1.get(), bot2.get()};
  Game game;
  game.moves.reserve(42);
  ofstream out("./" + cfg.filename + ".json");
  out << "{\n";
  for (int i = 0; i < cfg.numGames; i++) {
    playNewGame(game, bots);
    writeGame(out, i + 1, cfg.rows, cfg.cols, playerFullName(1, cfg), playerFullName(2, cfg), game, i == 0);
  }
  out << "\n}\n";
}