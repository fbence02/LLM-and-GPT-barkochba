async function sendGuess() {
    const el = document.getElementById('input');
    const word = el.value;
    if (!word) return;
    el.value = '';

    const res = await fetch('http://127.0.0.1:5000/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: word })
    });
    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    const color = data.score > 70 ? 'high' : (data.score > 40 ? 'mid' : 'low');
    const html = `<div class="guess"><span>${data.word}</span><span class="${color}">${data.score}%</span></div>`;
    document.getElementById('history').innerHTML = html + document.getElementById('history').innerHTML;

    if (data.win) alert("NYERTÉL!");
}

async function askForHint() {
    const hintBox = document.getElementById('hintBox');
    hintBox.innerText = "Gondolkodik...";
    try {
        const res = await fetch('http://127.0.0.1:5000/hint');
        const data = await res.json();
        if (data.error) {
            hintBox.innerText = "Hiba: " + (data.details || data.error);
        } else {
            hintBox.innerText = data.hint;
        }
    } catch (err) {
        hintBox.innerText = "Szerver nem elérhető.";
    }
}