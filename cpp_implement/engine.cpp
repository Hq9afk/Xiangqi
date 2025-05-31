// engine.cpp
#include "engine.hpp"
#include <vector>
#include <string>
#include <utility>  // for pair
#include <map>
#include <array>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <iostream>
#include <algorithm>
#include <limits>

using namespace std;

// cd /d D:/git_repo/Xiangqi
// python setup.py clean --all
// python setup.py build_ext --inplace --plat-name=win-amd64


map<string, int> startPower = {
    {"ch", 90}, {"hs", 40}, {"ep", 25}, {"ad", 30},
    {"gn", 9000}, {"cn", 45}, {"sd", 10}
};

map<string, int> midPower = {
    {"ch", 90}, {"hs", 40}, {"ep", 25}, {"ad", 30},
    {"gn", 9000}, {"cn", 50}, {"sd", 20}
};

map<string, int> endPower = {
    {"ch", 100}, {"hs", 50}, {"ep", 40}, {"ad", 40},
    {"gn", 9000}, {"cn", 40}, {"sd", 25}
};

map<string, vector<vector<float>>> bottomHalfPosition;
map<string, vector<vector<float>>> upperHalfPosition;

void load_piece_square_tables(const string& base_dir) {
    vector<string> piece_keys = {"ch", "hs", "ep", "ad", "gn", "cn", "sd"};

    for (const auto& key : piece_keys) {
        string filename = base_dir + "/" + key + ".csv";
        ifstream file(filename);
        if (!file.is_open()) {
            throw runtime_error("Failed to open: " + filename);
        }

        vector<vector<float>> rows;
        string line;
        while (getline(file, line)) {
            stringstream ss(line);
            string cell;
            vector<float> row;
            while (getline(ss, cell, ',')) {
                row.push_back(stof(cell));
            }
            rows.push_back(row);
        }

        bottomHalfPosition[key] = rows;

        vector<vector<float>> reversedRows = rows;
        reverse(reversedRows.begin(), reversedRows.end());
        upperHalfPosition[key] = reversedRows;
    }
}

Move::Move(const vector<vector<string>>& board,
           pair<int, int> first,
           pair<int, int> second) {
    startRow = first.first;
    startCol = first.second;
    endRow = second.first;
    endCol = second.second;

    chess_pieceSelected = board[startRow][startCol];
    chess_pieceMoveTo = board[endRow][endCol];
}

// class Move {
// public:
//     int startRow, startCol;
//     int endRow, endCol;
//     string chess_pieceSelected;
//     string chess_pieceMoveTo;

//     Move(const vector<vector<string>>& board,
//          pair<int, int> first,
//          pair<int, int> second)
//     {
//         startRow = first.first;
//         startCol = first.second;
//         endRow = second.first;
//         endCol = second.second;

//         chess_pieceSelected = board[startRow][startCol];
//         chess_pieceMoveTo = board[endRow][endCol];
//     }
// };

vector<pair<int,int>> chariotValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    // Move down
    for (int x = row + 1; x < 10; ++x) {
        if (board[x][col] == "---")
            validMoveList.emplace_back(x, col);
        else if (board[x][col][0] != chessSide) {
            validMoveList.emplace_back(x, col);
            break;
        } else
            break;
    }
    // Move up
    for (int x = row - 1; x >= 0; --x) {
        if (board[x][col] == "---")
            validMoveList.emplace_back(x, col);
        else if (board[x][col][0] != chessSide) {
            validMoveList.emplace_back(x, col);
            break;
        } else
            break;
    }
    // Move right
    for (int y = col + 1; y < 9; ++y) {
        if (board[row][y] == "---")
            validMoveList.emplace_back(row, y);
        else if (board[row][y][0] != chessSide) {
            validMoveList.emplace_back(row, y);
            break;
        } else
            break;
    }
    // Move left
    for (int y = col - 1; y >= 0; --y) {
        if (board[row][y] == "---")
            validMoveList.emplace_back(row, y);
        else if (board[row][y][0] != chessSide) {
            validMoveList.emplace_back(row, y);
            break;
        } else
            break;
    }
    return validMoveList;
}


vector<pair<int,int>> GeneralValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    vector<pair<int,int>> candidateMoveList = {
        {row + 1, col},
        {row, col + 1},
        {row, col - 1},
        {row - 1, col}
    };

    if (!redIsMachine) {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 3 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (7 <= x.first && x.first < 10 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        }
    } else {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (7 <= x.first && x.first < 10 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 3 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        }
    }

    return validMoveList;
}


vector<pair<int,int>> advisorValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    vector<pair<int,int>> candidateMoveList = {
        {row + 1, col + 1},
        {row + 1, col - 1},
        {row - 1, col + 1},
        {row - 1, col - 1}
    };

    if (!redIsMachine) {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 3 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (7 <= x.first && x.first < 10 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        }
    } else {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (7 <= x.first && x.first < 10 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 3 && 3 <= x.second && x.second < 6) {
                    if (board[x.first][x.second][0] != chessSide) validMoveList.push_back(x);
                }
            }
        }
    }

    return validMoveList;
}

vector<pair<int,int>> elephantValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    vector<pair<int,int>> candidateMoveList = {
        {row + 2, col + 2},
        {row + 2, col - 2},
        {row - 2, col + 2},
        {row - 2, col - 2}
    };

    if (!redIsMachine) {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 5 && 0 <= x.second && x.second < 9) {
                    if (board[(row + x.first)/2][(col + x.second)/2] == "---" && board[x.first][x.second][0] != chessSide) {
                        validMoveList.push_back(x);
                    }
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (4 < x.first && x.first < 10 && 0 <= x.second && x.second < 9) {
                    if (board[(row + x.first)/2][(col + x.second)/2] == "---" && board[x.first][x.second][0] != chessSide) {
                        validMoveList.push_back(x);
                    }
                }
            }
        }
    } else {
        if (chessSide == 'b') {
            for (auto &x : candidateMoveList) {
                if (5 <= x.first && x.first < 10 && 0 <= x.second && x.second < 9) {
                    if (board[(row + x.first)/2][(col + x.second)/2] == "---" && board[x.first][x.second][0] != chessSide) {
                        validMoveList.push_back(x);
                    }
                }
            }
        } else {
            for (auto &x : candidateMoveList) {
                if (0 <= x.first && x.first < 6 && 0 <= x.second && x.second < 9) {
                    if (board[(row + x.first)/2][(col + x.second)/2] == "---" && board[x.first][x.second][0] != chessSide) {
                        validMoveList.push_back(x);
                    }
                }
            }
        }
    }

    return validMoveList;
}

vector<pair<int,int>> horseValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    if (col + 1 < 9) {
        if (board[row][col + 1] == "---") {
            if (col + 2 < 9 && row + 1 < 10 &&
               (board[row + 1][col + 2] == "---" || board[row + 1][col + 2][0] != chessSide))
                validMoveList.emplace_back(row + 1, col + 2);

            if (col + 2 < 9 && row - 1 >= 0 &&
               (board[row - 1][col + 2] == "---" || board[row - 1][col + 2][0] != chessSide))
                validMoveList.emplace_back(row - 1, col + 2);
        }
    }
    if (col - 1 >= 0) {
        if (board[row][col - 1] == "---") {
            if (col - 2 >= 0 && row + 1 < 10 &&
               (board[row + 1][col - 2] == "---" || board[row + 1][col - 2][0] != chessSide))
                validMoveList.emplace_back(row + 1, col - 2);

            if (col - 2 >= 0 && row - 1 >= 0 &&
               (board[row - 1][col - 2] == "---" || board[row - 1][col - 2][0] != chessSide))
                validMoveList.emplace_back(row - 1, col - 2);
        }
    }
    if (row + 1 < 10) {
        if (board[row + 1][col] == "---") {
            if (col + 1 < 9 && row + 2 < 10 &&
               (board[row + 2][col + 1] == "---" || board[row + 2][col + 1][0] != chessSide))
                validMoveList.emplace_back(row + 2, col + 1);

            if (col - 1 >= 0 && row + 2 < 10 &&
               (board[row + 2][col - 1] == "---" || board[row + 2][col - 1][0] != chessSide))
                validMoveList.emplace_back(row + 2, col - 1);
        }
    }
    if (row - 1 >= 0) {
        if (board[row - 1][col] == "---") {
            if (col + 1 < 9 && row - 2 >= 0 &&
               (board[row - 2][col + 1] == "---" || board[row - 2][col + 1][0] != chessSide))
                validMoveList.emplace_back(row - 2, col + 1);

            if (col - 1 >= 0 && row - 2 >= 0 &&
               (board[row - 2][col - 1] == "---" || board[row - 2][col - 1][0] != chessSide))
                validMoveList.emplace_back(row - 2, col - 1);
        }
    }

    return validMoveList;
}

vector<pair<int,int>> cannonValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];

    // Helper lambda to check if a cell is inside the board
    auto inBounds = [](int r, int c) {
        return r >= 0 && r < 10 && c >= 0 && c < 9;
    };

    // Check downward direction
    for (int x = row + 1; x < 10; ++x) {
        if (board[x][col] == "---") {
            validMoveList.emplace_back(x, col);
        } else {
            for (int y = x + 1; y < 10; ++y) {
                if (board[y][col][0] != chessSide && board[y][col] != "---") {
                    validMoveList.emplace_back(y, col);
                    break;
                }
                if (board[y][col][0] == chessSide) {
                    break;
                }
            }
            break;
        }
    }

    // Check upward direction
    for (int x = row - 1; x >= 0; --x) {
        if (board[x][col] == "---") {
            validMoveList.emplace_back(x, col);
        } else {
            for (int y = x - 1; y >= 0; --y) {
                if (board[y][col][0] != chessSide && board[y][col] != "---") {
                    validMoveList.emplace_back(y, col);
                    break;
                }
                if (board[y][col][0] == chessSide) {
                    break;
                }
            }
            break;
        }
    }

    // Check right direction
    for (int y = col + 1; y < 9; ++y) {
        if (board[row][y] == "---") {
            validMoveList.emplace_back(row, y);
        } else {
            for (int x = y + 1; x < 9; ++x) {
                if (board[row][x][0] != chessSide && board[row][x] != "---") {
                    validMoveList.emplace_back(row, x);
                    break;
                }
                if (board[row][x][0] == chessSide) {
                    break;
                }
            }
            break;
        }
    }

    // Check left direction
    for (int y = col - 1; y >= 0; --y) {
        if (board[row][y] == "---") {
            validMoveList.emplace_back(row, y);
        } else {
            for (int x = y - 1; x >= 0; --x) {
                if (board[row][x][0] != chessSide && board[row][x] != "---") {
                    validMoveList.emplace_back(row, x);
                    break;
                }
                if (board[row][x][0] == chessSide) {
                    break;
                }
            }
            break;
        }
    }

    return validMoveList;
}

vector<pair<int,int>> soldierValidMoveList(const vector<vector<string>>& board, pair<int,int> position, bool redIsMachine) {
    vector<pair<int,int>> validMoveList;
    int row = position.first;
    int col = position.second;
    char chessSide = board[row][col][0];  // first char of string, e.g. 'r' or 'b'

    // Helper lambda to check if a cell is inside the board
    auto inBounds = [](int r, int c) {
        return r >= 0 && r < 10 && c >= 0 && c < 9;
    };

    vector<pair<int,int>> candidate;

    if (!redIsMachine) {
        if (chessSide == 'b') {
            candidate.push_back({row + 1, col});
            if (row > 4) {
                candidate.push_back({row, col + 1});
                candidate.push_back({row, col - 1});
            }
        } else { // red side
            candidate.push_back({row - 1, col});
            if (row < 5) {
                candidate.push_back({row, col + 1});
                candidate.push_back({row, col - 1});
            }
        }
    } else {
        if (chessSide == 'b') {
            candidate.push_back({row - 1, col});
            if (row < 5) {
                candidate.push_back({row, col + 1});
                candidate.push_back({row, col - 1});
            }
        } else { // red side
            candidate.push_back({row + 1, col});
            if (row > 4) {
                candidate.push_back({row, col + 1});
                candidate.push_back({row, col - 1});
            }
        }
    }

    for (auto& x : candidate) {
        int r = x.first;
        int c = x.second;
        if (inBounds(r, c)) {
            if (board[r][c][0] != chessSide) {
                validMoveList.push_back(x);
            }
        }
    }

    return validMoveList;
}


vector<pair<int,int>> moveRule(
    const vector<vector<string>>& board,
    pair<int,int> position,
    bool redIsMachine
) {
    vector<pair<int,int>> validMoveList;

    string chessPiece = board[position.first][position.second].substr(1);  // from 2nd char on

        if (chessPiece == "ch") {
        validMoveList = chariotValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "hs") {
        validMoveList = horseValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "cn") {
        validMoveList = cannonValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "gn") {
        validMoveList = GeneralValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "ad") {
        validMoveList = advisorValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "sd") {
        validMoveList = soldierValidMoveList(board, position, redIsMachine);
    }
    else if (chessPiece == "ep") {
        validMoveList = elephantValidMoveList(board, position, redIsMachine);
    }
    
    return validMoveList;
}

inline int encode_pos(int row, int col) {
    return row * 10 + col;
}

inline pair<int, int> decode_pos(int pos) {
    return {pos / 10, pos % 10};
}

void add_piece_position(map<string, vector<int>>& data, const string& piece, int row, int col) {
    int pos = encode_pos(row, col);
    data[piece].push_back(pos);
}

void remove_piece_position(map<string, vector<int>>& data, const string& piece, int row, int col) {
    int pos = encode_pos(row, col);
    if (data.find(piece) != data.end()) {
        auto& positions = data[piece];
        auto it = find(positions.begin(), positions.end(), pos);
        if (it != positions.end()) {
            positions.erase(it);
        }
    }
}

void change_piece_position(map<string, vector<int>>& data, const string& piece,
                           int old_row, int old_col, int new_row, int new_col) {
    int old_pos = encode_pos(old_row, old_col);
    int new_pos = encode_pos(new_row, new_col);
    if (data.find(piece) != data.end()) {
        auto& positions = data[piece];
        auto it = find(positions.begin(), positions.end(), old_pos);
        if (it != positions.end()) {
            *it = new_pos;
        }
    }
}

vector<pair<int, int>> get_chess_piece_positions(
    const map<string, vector<int>>& data,
    const string& piece)
{
    vector<pair<int, int>> positions;
    auto it = data.find(piece);
    if (it != data.end()) {
        const vector<int>& encoded_positions = it->second;
        for (int pos : encoded_positions) {
            positions.push_back(decode_pos(pos));
        }
    }
    return positions;
}

void universal_chess_piece_dict_update(
    map<string, vector<int>>& red_data,
    map<string, vector<int>>& black_data,
    const string& chess_pieceSelected,
    const string& chess_pieceMoveTo,
    int startRow,
    int startCol,
    int endRow,
    int endCol)
{
    if (chess_pieceSelected[0] == 'r') {
        change_piece_position(red_data, chess_pieceSelected.substr(1),
                              startRow, startCol, endRow, endCol);
        if (chess_pieceMoveTo != "---") {
            remove_piece_position(black_data, chess_pieceMoveTo.substr(1),
                                  endRow, endCol);
        }
    } else {
        change_piece_position(black_data, chess_pieceSelected.substr(1),
                              startRow, startCol, endRow, endCol);
        if (chess_pieceMoveTo != "---") {
            remove_piece_position(red_data, chess_pieceMoveTo.substr(1),
                                  endRow, endCol);
        }
    }
}

void universal_chess_piece_dict_reverse(
    map<string, vector<int>>& red_data,
    map<string, vector<int>>& black_data,
    const string& chess_pieceSelected,
    const string& chess_pieceMoveTo,
    int startRow, int startCol,
    int endRow, int endCol)
{
    if (!chess_pieceSelected.empty() && chess_pieceSelected[0] == 'r') {
        change_piece_position(red_data, chess_pieceSelected.substr(1), endRow, endCol, startRow, startCol);
        if (chess_pieceMoveTo != "---") {
            add_piece_position(black_data, chess_pieceMoveTo.substr(1), endRow, endCol);
        }
    } else {
        change_piece_position(black_data, chess_pieceSelected.substr(1), endRow, endCol, startRow, startCol);
        if (chess_pieceMoveTo != "---") {
            add_piece_position(red_data, chess_pieceMoveTo.substr(1), endRow, endCol);
        }
    }
}

vector<pair<int, int>> get_all_chess_piece_positions(const map<string, vector<int>>& data) {
    vector<pair<int, int>> positions;
    for (const auto& kv : data) {
        for (int pos : kv.second) {
            positions.emplace_back(decode_pos(pos));
        }
    }
    return positions;
}

map<string, vector<int>> copy_pieces_pos_dict(const map<string, vector<int>>& original) {
    map<string, vector<int>> copied;
    for (const auto& [key, value] : original) {
        copied[key] = value;  // std::vector has a copy constructor
    }
    return copied;
}

vector<vector<pair<int, int>>> getAllValid(
    vector<vector<string>> board,
    map<string, vector<int>> red_piece_pos_dict,
    map<string, vector<int>> black_piece_pos_dict,
    bool redTurn,
    bool redIsMachine) {

    vector<vector<pair<int, int>>> validMoveList;
    const map<string, vector<int>>& piece_pos_dict = redTurn ? red_piece_pos_dict : black_piece_pos_dict;
    vector<pair<int, int>> all_positions = get_all_chess_piece_positions(piece_pos_dict);

    for (const auto& pos : all_positions) {
        vector<pair<int, int>> candidateMoveList = moveRule(board, pos, redIsMachine);

        for (const auto& cell : candidateMoveList) {
            auto chess_pieceSelected = board[pos.first][pos.second];
            auto chess_pieceMoveTo = board[cell.first][cell.second];
            auto tmpBoard = board;
            auto tmpRed_piece_pos_dict = red_piece_pos_dict;
            auto tmpBlack_piece_pos_dict = black_piece_pos_dict;
            bool tmpRedTurn = redTurn;

            universal_chess_piece_dict_update(
                tmpRed_piece_pos_dict,
                tmpBlack_piece_pos_dict,
                chess_pieceSelected,
                chess_pieceMoveTo,
                pos.first,
                pos.second,
                cell.first,
                cell.second
            );

            tmpBoard[pos.first][pos.second] = "---";
            tmpBoard[cell.first][cell.second] = chess_pieceSelected;

            if (moveCheckValid(tmpBoard, tmpRed_piece_pos_dict, tmpBlack_piece_pos_dict, tmpRedTurn, redIsMachine)) {
                validMoveList.push_back({pos, cell});
            }

            universal_chess_piece_dict_reverse(
                tmpRed_piece_pos_dict,
                tmpBlack_piece_pos_dict,
                chess_pieceSelected,
                chess_pieceMoveTo,
                pos.first,
                pos.second,
                cell.first,
                cell.second
            );

            tmpBoard[pos.first][pos.second] = chess_pieceSelected;
            tmpBoard[cell.first][cell.second] = chess_pieceMoveTo;
        }
    }
    return validMoveList;
}

bool isHorseThreatensGeneral(const vector<vector<string>>& board, 
                             pair<int,int> horse_pos, pair<int,int> general_pos) {
    int hr = horse_pos.first;
    int hc = horse_pos.second;
    int gr = general_pos.first;
    int gc = general_pos.second;

    int dx = gr - hr;
    int dy = gc - hc;

    // Map direction quadrant to move candidates and their legs
    const static map<pair<int,int>, array<pair<pair<int,int>, pair<int,int>>, 2>> region_map = {
    {
        {1, 1}, 
        array<pair<pair<int,int>, pair<int,int>>, 2>{
            make_pair(make_pair(1, 2), make_pair(0, 1)),
            make_pair(make_pair(2, 1), make_pair(1, 0))
        }
    },
    {
        {1, -1}, 
        std::array<std::pair<std::pair<int,int>, std::pair<int,int>>, 2>{
            std::make_pair(std::make_pair(1, -2), std::make_pair(0, -1)),
            std::make_pair(std::make_pair(2, -1), std::make_pair(1, 0))
        }
    },
    {
        {-1, 1}, 
        std::array<std::pair<std::pair<int,int>, std::pair<int,int>>, 2>{
            std::make_pair(std::make_pair(-1, 2), std::make_pair(0, 1)),
            std::make_pair(std::make_pair(-2, 1), std::make_pair(-1, 0))
        }
    },
    {
        {-1, -1}, 
        std::array<std::pair<std::pair<int,int>, std::pair<int,int>>, 2>{
            std::make_pair(std::make_pair(-1, -2), std::make_pair(0, -1)),
            std::make_pair(std::make_pair(-2, -1), std::make_pair(-1, 0))
        }
    }
    };

    int dir_x = dx > 0 ? 1 : -1;
    int dir_y = dy > 0 ? 1 : -1;
    auto key = make_pair(dir_x, dir_y);

    auto it = region_map.find(key);
    if (it == region_map.end()) return false;

    for (const auto& [move, leg] : it->second) {
        if (dx == move.first && dy == move.second) {
            int leg_r = hr + leg.first;
            int leg_c = hc + leg.second;
            if (leg_r >= 0 && leg_r < (int)board.size() && leg_c >= 0 && leg_c < (int)board[0].size())
                return board[leg_r][leg_c] == "---";
        }
    }
    return false;
}

bool isCanonThreatensGeneral(const vector<vector<string>>& board, pair<int,int> from_pos, pair<int,int> to_pos) {
    int from_x = from_pos.first, from_y = from_pos.second;
    int to_x = to_pos.first, to_y = to_pos.second;

    if (from_x != to_x && from_y != to_y) return false;

    int count_between = 0;

    if (from_x == to_x) {
        int step = (to_y > from_y) ? 1 : -1;
        for (int y = from_y + step; y != to_y; y += step) {
            if (board[from_x][y] != "---") {
                count_between++;
                if (count_between > 1) return false;
            }
        }
    } else {
        int step = (to_x > from_x) ? 1 : -1;
        for (int x = from_x + step; x != to_x; x += step) {
            if (board[x][from_y] != "---") {
                count_between++;
                if (count_between > 1) return false;
            }
        }
    }
    return count_between == 1;
}


bool moveCheckValid(
    const vector<vector<string>>& board,
    const map<string, vector<int>>& red_chess_piece_pos_dict,
    const map<string, vector<int>>& black_chess_piece_pos_dict,
    bool redTurn,
    bool redIsMachine)
{
    bool Check = false;

    // Assume get_chess_piece_positions returns vector<pair<int,int>> for the piece
    pair<int, int> blackGeneral = get_chess_piece_positions(black_chess_piece_pos_dict, "gn")[0];
    pair<int, int> redGeneral = get_chess_piece_positions(red_chess_piece_pos_dict, "gn")[0];

    int step = (blackGeneral.first < redGeneral.first) ? 1 : -1;

    if (blackGeneral.second == redGeneral.second) {
        for (int i = blackGeneral.first + step; i != redGeneral.first + step; i += step) {
            if (board[i][blackGeneral.second] == "---") {
                continue;
            } else if (board[i][blackGeneral.second].substr(1) == "gn") {
                Check = true;
                break;
            } else {
                break;
            }
        }
        if (Check) {
            return false;
        }
    }

    if (isChecked(board, blackGeneral, redGeneral, red_chess_piece_pos_dict, black_chess_piece_pos_dict, !redTurn, redIsMachine)) {
        return false;
    }

    return true;
}

bool isChecked(const vector<vector<string>>& board,
               pair<int,int> blackGeneral,
               pair<int,int> redGeneral,
               const map<string, vector<int>>& red_pos,
               const map<string, vector<int>>& black_pos,
               bool redTurn,
               bool redIsMachine)
{
    int x, y;
    string chessSide;
    const map<string, vector<int>>* chess_piece_pos_dict;

    if (redTurn) {
        x = blackGeneral.first;
        y = blackGeneral.second;
        chessSide = "b";
        chess_piece_pos_dict = &red_pos;
    } else {
        x = redGeneral.first;
        y = redGeneral.second;
        chessSide = "r";
        chess_piece_pos_dict = &black_pos;
    }

    // Horse check
    auto horsePositions = get_chess_piece_positions(*chess_piece_pos_dict, "hs");
    for (auto& pos : horsePositions) {
        if (isHorseThreatensGeneral(board, pos, {x, y})) return true;
    }

    // Chariot check
    auto chariotPositions = get_chess_piece_positions(*chess_piece_pos_dict, "ch");
    for (auto& pos : chariotPositions) {
        int r = pos.first;
        int c = pos.second;

        if (r == x) {
            if (c < y) {
                for (int j = c; j < y; j++) {
                    if (j == y - 1) return true;
                    if (board[x][j + 1] != "---") break;
                }
            }
            if (c > y) {
                for (int j = y; j < c; j++) {
                    if (j == c - 1) return true;
                    if (board[x][j + 1] != "---") break;
                }
            }
        }
        if (c == y) {
            if (r < x) {
                for (int j = r; j < x; j++) {
                    if (j == x - 1) return true;
                    if (board[j + 1][y] != "---") break;
                }
            }
            if (r > x) {
                for (int j = x; j < r; j++) {
                    if (j == r - 1) return true;
                    if (board[j + 1][y] != "---") break;
                }
            }
        }
    }

    // Cannon check
    auto cannonPositions = get_chess_piece_positions(*chess_piece_pos_dict, "cn");
    for (auto& pos : cannonPositions) {
        if (isCanonThreatensGeneral(board, {x, y}, pos)) return true;
    }

    // Soldier check
    auto soldierPositions = get_chess_piece_positions(*chess_piece_pos_dict, "sd");
    vector<pair<int,int>> candidateThreats = { {x, y+1}, {x, y-1} };
    if (chessSide == "r") candidateThreats.push_back({x-1, y});
    else candidateThreats.push_back({x+1, y});

    for (auto& pos : soldierPositions) {
        for (auto& threat : candidateThreats) {
            if (pos == threat) return true;
        }
    }

    return false;
}

// class Minimax {
// public:
//     int maxDepth;
//     vector<pair<int,int>> minimaxSuggestedMove; // or your Move class

//     Minimax(int maxDepth) : maxDepth(maxDepth) {}

    // This is your recursive function similar to `initiateMinimax`
float Minimax::initiateMinimax(
        const vector<vector<string>>& board,
        map<string, vector<int>> red_chess_piece_pos_dict,
        map<string, vector<int>> black_chess_piece_pos_dict,
        bool redTurn,
        bool redIsMachine,
        int depth,
        bool isMaximizingPlayer,
        int moveCounter,
        float testPointReal,
        vector<Move> preGuessMove,
        float alpha,
        float beta
    ) {
        // Generate all valid moves (implement getAllValid in C++)
        auto MinimaxNextMoveList = getAllValid(board, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine);
        
        if (depth == 0 || MinimaxNextMoveList.empty()) {
            // Evaluate board (implement evaluate in C++)
            return evaluate(redIsMachine, moveCounter, preGuessMove, testPointReal);
        }

        if (isMaximizingPlayer) {
            float best = -numeric_limits<float>::infinity();
            for (const auto& move : MinimaxNextMoveList) {
                Move moveInfo(board, move[0], move[1]);
                
                auto nextRed_chess_piece_pos_dict = red_chess_piece_pos_dict;
                auto nextBlackPos = black_chess_piece_pos_dict;
                if (moveInfo.chess_pieceSelected[0] == 'r') {
                    nextRed_chess_piece_pos_dict = copy_pieces_pos_dict(red_chess_piece_pos_dict);
                } else {
                    nextBlackPos = copy_pieces_pos_dict(black_chess_piece_pos_dict);
                }
                // update piece position dictionaries (implement universal_chess_piece_dict_update in C++)
                universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict, 
                                                  nextBlackPos, 
                                                  moveInfo.chess_pieceSelected,
                                                  moveInfo.chess_pieceMoveTo,
                                                  moveInfo.startRow,
                                                  moveInfo.startCol,
                                                  moveInfo.endRow,
                                                  moveInfo.endCol);

                // get next board state (implement getNextGameState in C++)
                auto nextBoard = getNextGameState(board, move);

                preGuessMove.push_back(moveInfo);
                float value = initiateMinimax(nextBoard,
                                              nextRed_chess_piece_pos_dict,
                                              nextBlackPos, 
                                              !redTurn, 
                                              redIsMachine,
                                              depth - 1, 
                                              false, 
                                              moveCounter, 
                                              testPointReal,
                                              preGuessMove, alpha, beta);
                preGuessMove.pop_back();

                if (value > best) {
                    best = value;
                    if (depth == maxDepth) {
                        minimaxSuggestedMove = move;
                    }
                }
                alpha = max(alpha, best);
                if (alpha >= beta)
                    break;
            }
            return best;
        } else {
            float best = numeric_limits<float>::infinity();
            for (const auto& move : MinimaxNextMoveList) {
                Move moveInfo(board, move[0], move[1]);

                auto nextRed_chess_piece_pos_dict = red_chess_piece_pos_dict;
                auto nextBlackPos = black_chess_piece_pos_dict;
                if (moveInfo.chess_pieceSelected[0] == 'r') {
                    nextRed_chess_piece_pos_dict = copy_pieces_pos_dict(red_chess_piece_pos_dict);
                } else {
                    nextBlackPos = copy_pieces_pos_dict(black_chess_piece_pos_dict);
                }
                universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict, 
                                                  nextBlackPos, 
                                                  moveInfo.chess_pieceSelected,
                                                  moveInfo.chess_pieceMoveTo,
                                                  moveInfo.startRow,
                                                  moveInfo.startCol,
                                                  moveInfo.endRow,
                                                  moveInfo.endCol);

                auto nextBoard = getNextGameState(board, move);

                preGuessMove.push_back(moveInfo);
                float value = initiateMinimax(nextBoard,
                                              nextRed_chess_piece_pos_dict, 
                                              nextBlackPos, 
                                              !redTurn, 
                                              redIsMachine,
                                             depth - 1, 
                                             true, 
                                             moveCounter, 
                                             testPointReal,
                                             preGuessMove, alpha, beta);
                preGuessMove.pop_back();

                if (value < best) {
                    best = value;
                    if (depth == maxDepth) {
                        minimaxSuggestedMove = move;
                    }
                }
                beta = min(beta, best);
                if (alpha >= beta)
                    break;
            }
            return best;
        }
}
// };

vector<vector<string>> getNextGameState(
    const vector<vector<string>>& board,
    const vector<pair<int, int>>& nextMove
) {
    vector<vector<string>> tmpBoard = board;  // Deep copy

    pair<int, int> start = nextMove[0];
    pair<int, int> end = nextMove[1];

    string selectedPiece = tmpBoard[start.first][start.second];
    tmpBoard[start.first][start.second] = "---";
    tmpBoard[end.first][end.second] = selectedPiece;

    return tmpBoard;
}

float evaluate(
    bool redIsMachine,
    int moveCounter,
    vector<Move> preGuessMove,
    float testPointReal
) {
    bool tmpRedTurn = redIsMachine;
    float testPoint = testPointReal;

    for ( auto& move : preGuessMove) {
        const string testChessPiece = move.chess_pieceSelected.substr(1);
        const string moveToPiece = move.chess_pieceMoveTo.substr(1);
        bool isCapture = move.chess_pieceMoveTo != "---";

        map<string, int> power;
        if (moveCounter <= 14)
            power = startPower;
        else if (moveCounter <= 50)
            power = midPower;
        else
            power = endPower;

        if (redIsMachine) {
            if (tmpRedTurn) {
                testPoint += -upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                             + upperHalfPosition[testChessPiece][move.endRow][move.endCol];
                if (isCapture)
                    testPoint += power[moveToPiece]
                                 + bottomHalfPosition[moveToPiece][move.endRow][move.endCol];
            } else {
                testPoint += bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                             - bottomHalfPosition[testChessPiece][move.endRow][move.endCol];
                if (isCapture)
                    testPoint -= power[moveToPiece]
                                 + upperHalfPosition[moveToPiece][move.endRow][move.endCol];
            }
        } else {
            if (tmpRedTurn) {
                testPoint += bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                             - bottomHalfPosition[testChessPiece][move.endRow][move.endCol];
                if (isCapture)
                    testPoint -= power[moveToPiece]
                                 + upperHalfPosition[moveToPiece][move.endRow][move.endCol];
            } else {
                testPoint += -upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                             + upperHalfPosition[testChessPiece][move.endRow][move.endCol];
                if (isCapture)
                    testPoint += power[moveToPiece]
                                 + bottomHalfPosition[moveToPiece][move.endRow][move.endCol];
            }
        }

        moveCounter++;
        tmpRedTurn = !tmpRedTurn;
    }

    return testPoint;
}