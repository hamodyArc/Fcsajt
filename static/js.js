const positions = [
    { top: "10%", left: "10%" },  // Left wing
    { top: "70%", left: "40%" }, // Mid bottom
    { top: "10%", left: "70%" }  // Right wing
];

function selectPlayer(name, id) {
    let field = document.getElementById("field");
    let playersOnField = document.querySelectorAll(".player");
    if (playersOnField.length >= 3) return;

    let player = document.createElement("div");
    player.classList.add("player");
    player.innerText = name;
    player.setAttribute("data-id", id);  // Store ID in data attribute

    console.log(`Selected: ${name} with ID: ${id}`); // Debugging

    let pos = positions[playersOnField.length];
    player.style.top = pos.top;
    player.style.left = pos.left;

    player.onclick = function () {
        player.remove();
    };

    field.appendChild(player);
}

function savePlayers() {
    let players = document.querySelectorAll(".player");

    let selectedPlayers = Array.from(players).map(player => {
        let playerName = player.innerText;
        let playerId = player.getAttribute("data-id");  // Retrieve ID
        console.log(`Saving Player: ${playerName}, ID: ${playerId}`); // Debugging
        return { name: playerName, id: playerId };
    });

    let data = { players: selectedPlayers };

    fetch('/save_players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json()) 
    .then(data => console.log('Match found:', data))
    .catch(error => console.error('Error:', error));
}
