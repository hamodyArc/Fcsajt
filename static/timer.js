function updateTimers() {
    document.querySelectorAll('.timer').forEach(timer => {
        let startTime = new Date(timer.getAttribute('data-start-time')).getTime();
        let now = new Date().getTime();
        let endTime = startTime + (1 * 60 * 1000); 
        let timeLeft = Math.max(0, endTime - now);
        let matchContainer = timer.closest('.match-result'); 
        let stats = matchContainer.querySelectorAll(".stats");

        if (timeLeft > 0) {
            let minutes = Math.floor(timeLeft / (1000 * 60));
            let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
            timer.innerText = `${minutes}m ${seconds}s`;

            stats.forEach(stat => stat.style.display = "none");
        } else {
            timer.innerText = "Match Ended";

            stats.forEach(stat => stat.style.display = "block");
        }
    });
}

setInterval(updateTimers, 1000);
updateTimers();
