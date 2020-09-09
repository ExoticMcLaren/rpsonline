import React, { Component } from "react";

class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            messages: [],
        };
    }

    componentDidMount() {
        const user = JSON.parse(document.getElementById('user').textContent);

        fetch('api/statistics')
            .then((result) => result.json())
            .then((result) => {
                this.setState({
                    data: result,
                })
            })

        var socketPath = 'ws://'
            + window.location.host
            + '/ws/room/';

        const socket = new WebSocket(socketPath);

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.message === "Waiting for opponents...") {
                document.querySelector('#chat-log').value += (data.message + '\n');
            } else {
                window.location.href = 'http://' + window.location.host + '/game/' + data.message;
            }
        };

        socket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#btn-ready').onclick = function(e) {
            socket.send(JSON.stringify({
                'action': 'ready',
                'player': user
            }));
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
                    <button className="btn btn-primary" id="btn-ready">Ready to Play</button>
                </div>
                <h3 className="mt-2">Player Statistics</h3>
                <div className="w-100 mt-2">
                    { stats }
                </div>
            </div>
        );
    }
}

export default Room;
