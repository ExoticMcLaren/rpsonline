import React, { Component } from "react";

class Game extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            messages: [],
        };
        this.fetchStatistics = this.fetchStatistics.bind(this);
    }

    fetchStatistics() {
        fetch('/api/statistics')
            .then((result) => result.json())
            .then((result) => {
                this.setState({
                    data: result,
                })
            })
    }

    componentDidMount() {
        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        const user = JSON.parse(document.getElementById('user').textContent);
        var self = this;
        var game_timer;

        function setCountdown(seconds) {
            var distance = seconds;
            var timer = setInterval(function() {
                distance--;
                document.getElementById("countdown").innerHTML = distance;
                if (distance < 0) {
                    clearInterval(timer);
                    document.getElementById("countdown").innerHTML = "EXPIRED";

                    socket.send(JSON.stringify({
                        'action': 'move',
                        'player': user,
                        'option': 'T'
                    }));

                    $('#btn-rock').hide();
                    $('#btn-paper').hide();
                    $('#btn-scissors').hide();
                    $('#btn-retry').show();
                    $('#btn-exit').show();
                }
            }, 1000);

            return timer;
        }

        function removeCountdown(timer) {
            clearInterval(timer)
        }

        const socket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/game/'
            + roomName
            + '/'
        );

        socket.onopen = function(e) {
            game_timer = setCountdown(15);
        }

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            document.querySelector('#chat-log').innerHTML += (data.message + '\n');

            if (data.type === "end") {
                $('#btn-retry').show();
                $('#btn-exit').show();
            }
            else if (data.type === "retry") {
                $('#btn-rock').show();
                $('#btn-paper').show();
                $('#btn-scissors').show();
                $('#btn-retry').hide();
                $('#btn-exit').hide();
                game_timer = setCountdown(15);
            }
            self.fetchStatistics();
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#btn-rock').onclick = function(e) {
            socket.send(JSON.stringify({
                'action': 'move',
                'player': user,
                'option': 'R'
            }));
            $('#btn-rock').hide();
            $('#btn-paper').hide();
            $('#btn-scissors').hide();
            removeCountdown(game_timer);
        };

        document.querySelector('#btn-paper').onclick = function(e) {
            socket.send(JSON.stringify({
                'action': 'move',
                'player': user,
                'option': 'P'
            }));
            $('#btn-rock').hide();
            $('#btn-paper').hide();
            $('#btn-scissors').hide();
            removeCountdown(game_timer);
        };

        document.querySelector('#btn-scissors').onclick = function(e) {
            socket.send(JSON.stringify({
                'action': 'move',
                'player': user,
                'option': 'S'
            }));
            $('#btn-rock').hide();
            $('#btn-paper').hide();
            $('#btn-scissors').hide();
            removeCountdown(game_timer);
        };

        document.querySelector('#btn-retry').onclick = function(e) {
            socket.send(JSON.stringify({
                'action': 'retry',
                'player': user
            }));
            removeCountdown(game_timer);
        };
    }

    render() {
        const {data} = this.state

        const stats = data.map(player => {
            return <div key={player.id}>Wins: { player.wins }<br />Ties: { player.ties }<br />Loses: { player.loses }</div>
        })

        return (
            <div className="container mt-3">
                <h3>Game Log</h3>
                <div className="border w-100" style={{height: 200 + "px"}}>
                    <textarea id="chat-log" className="w-100 h-100"></textarea>
                </div>
                <div className="btn-group w-100 mt-2" role="group">
                    <button className="btn btn-primary" id="btn-rock">Rock</button>
                    <button className="btn btn-primary" id="btn-paper">Paper</button>
                    <button className="btn btn-primary" id="btn-scissors">Scissors</button>
                </div>
                <div className="btn-group w-100 mt-2" role="group">
                    <button className="btn btn-primary" id="btn-retry" style={{display: 'none'}}>Retry</button>
                    <a className="btn btn-primary" id="btn-exit" href="/" style={{display: 'none'}}>Exit</a>
                </div>
                <div className="w-100 mt-2">
                    <div id="countdown"></div>
                </div>
                <h3 className="mt-2">Player Statistics</h3>
                <div className="w-100 mt-2">
                    { stats }
                </div>
            </div>
        );
    }
}

export default Game;