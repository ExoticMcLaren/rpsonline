import Game from "./components/Game";
import React from "react";
import {render} from "react-dom";

const gameContainer = document.getElementById("game");
render(<Game />, gameContainer);
