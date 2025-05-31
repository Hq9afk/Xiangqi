#ifndef ENGINE_HPP
#define ENGINE_HPP

#include <vector>
#include <string>
#include <utility>
#include <map>
#include <array>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <iostream>
#include <algorithm>
#include <limits>

using namespace std;

extern map<string, int> startPower;
extern map<string, int> midPower;
extern map<string, int> endPower;

extern map<string, vector<vector<float>>> bottomHalfPosition;
extern map<string, vector<vector<float>>> upperHalfPosition;

// moveRule dispatcher function
vector<pair<int,int>> moveRule(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine);

// Updated function declarations
bool isChecked(const vector<vector<string>>& board,
               pair<int,int> blackGeneral,
               pair<int,int> redGeneral,
               const map<string, vector<int>>& red_pos,
               const map<string, vector<int>>& black_pos,
               bool redTurn,
               bool redIsMachine);

bool moveCheckValid(const vector<vector<string>>& board,
                    const map<string, vector<int>>& red_chess_piece_pos_dict,
                    const map<string, vector<int>>& black_chess_piece_pos_dict,
                    bool redTurn,
                    bool redIsMachine);

vector<vector<pair<int, int>>> getAllValid(vector<vector<string>> board,
                                           map<string, vector<int>> red_piece_pos_dict,
                                           map<string, vector<int>> black_piece_pos_dict,
                                           bool redTurn,
                                           bool redIsMachine);

void load_piece_square_tables(const string& basePath);

class Move {
public:
    int startRow, startCol;
    int endRow, endCol;
    string chess_pieceSelected;
    string chess_pieceMoveTo;

    Move(const vector<vector<string>>& board,
         pair<int, int> first,
         pair<int, int> second);
};

vector<vector<string>> getNextGameState(
    const vector<vector<string>>& board,
    const vector<pair<int, int>>& nextMove
);

float evaluate(
    bool redIsMachine,
    int moveCounter,
    vector<Move> preGuessMove,
    float testPointReal
);

class Minimax {
public:
    int maxDepth;
    vector<pair<int,int>> minimaxSuggestedMove; // or your Move class

        Minimax(int maxDepth) : maxDepth(maxDepth) {}

    // This is your recursive function similar to `initiateMinimax`
    float initiateMinimax(
        const vector<vector<string>>& board,
        map<string, vector<int>> red_chess_piece_pos_dict,
        map<string, vector<int>> black_chess_piece_pos_dict,
        bool redTurn,   
        bool redIsMachine,
        int depth,
        bool isMaximizingPlayer,
        int moveCounter,
        float testPointReal,
        vector<Move> preGuessMove = vector<Move>(),
        float alpha = -numeric_limits<float>::infinity(),
        float beta = numeric_limits<float>::infinity()
    );
};

#endif // ENGINE_HPP
