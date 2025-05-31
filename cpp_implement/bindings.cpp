// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "engine.hpp"

namespace py = pybind11;

PYBIND11_MODULE(xiangqi_cpp, m) {

      load_piece_square_tables("D:/git_repo/Xiangqi/unity");

      // Bind the power maps
    m.attr("startPower") = &startPower;
    m.attr("midPower") = &midPower;
    m.attr("endPower") = &endPower;

    // Bind the piece-square tables
    m.attr("bottomHalfPosition") = &bottomHalfPosition;
    m.attr("upperHalfPosition") = &upperHalfPosition;

    py::class_<Minimax>(m, "Minimax")
        .def(py::init<int>())
        .def("initiateMinimax", &Minimax::initiateMinimax,
             py::arg("board"),
             py::arg("red_chess_piece_pos_dict"),
             py::arg("black_chess_piece_pos_dict"),
             py::arg("redTurn"),
             py::arg("redIsMachine"),
             py::arg("depth"),
             py::arg("isMaximizingPlayer"),
             py::arg("moveCounter"),
             py::arg("testPointReal"),
             py::arg("preGuessMove") = std::vector<Move>(),
             py::arg("alpha") = -std::numeric_limits<float>::infinity(),
             py::arg("beta") = std::numeric_limits<float>::infinity())
        .def_readwrite("maxDepth", &Minimax::maxDepth)
        .def_readwrite("minimaxSuggestedMove", &Minimax::minimaxSuggestedMove);

    m.def("isChecked", &isChecked,
          py::arg("board"),
          py::arg("blackGeneral"),
          py::arg("redGeneral"),
          py::arg("red_pos"),
          py::arg("black_pos"),
          py::arg("redTurn"),
          py::arg("redIsMachine"));

    m.def("moveCheckValid", &moveCheckValid,
          py::arg("board"),
          py::arg("red_chess_piece_pos_dict"),
          py::arg("black_chess_piece_pos_dict"),
          py::arg("redTurn"),
          py::arg("redIsMachine"));

    m.def("getAllValid", &getAllValid,
          py::arg("board"),
          py::arg("red_piece_pos_dict"),
          py::arg("black_piece_pos_dict"),
          py::arg("redTurn"),
          py::arg("redIsMachine"));

    m.def("moveRule", &moveRule,
          py::arg("board"),
          py::arg("position"),
          py::arg("redIsMachine"));
}
