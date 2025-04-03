function sendPlayer(playerId) {
    fetch('/save_players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: playerId })
    })
    .then(response => response.json()) 
    .then(data => console.log('Response:', data))
    .catch(error => console.error('Error:', error));
    console.log("Player ID sent:", playerId);
}

function removeplayer(playerId) {
    fetch('/remove_player', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: playerId })
    })
    .then(response => response.json()) 
    .then(data => console.log('Response:', data))
    .catch(error => console.error('Error:', error));
    console.log("Player ID removed:", playerId);
}
