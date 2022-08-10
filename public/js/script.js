console.log("hello");
//send spotify id to backend
//get recommendations based on genre
//display results and recommendations

//you are likely to enjoy this genre and these songs

const genreAPI = async (songId) => {
    const response = await fetch('http://localhost:5000/api/genre?id=' + songId);
    let genreJSON = await response.json();
    genre = genreJSON['genre'];
    console.log(genre);
    document.getElementById("genre-results").innerHTML = `
            <div class="card is-pinker">
            <div class="card-content">
            <div class="content source-font has-text-centered">
                <p>🎵You are likely to enjoy the following genre:</p>
                <strong>✨${genre}<strong>
            </div>
            </div>
        </div>
    `;

    const response2 = await fetch('http://127.0.0.1:5000/api/rec?id=' + songId + "&genre=" + genre);
    let recJSON = await response2.json();
    rec = recJSON.rec;
    console.log(rec);
    document.getElementById("rec-results").innerHTML = `
        <div class="card is-pinker">
            <div class="card-content">
            <div class="content source-font has-text-centered">
            <p>🎵You should give this song a try:</p>
                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/${rec}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
            </div>
            </div>
        </div>
    `;
}
document.getElementById('button').addEventListener('click', () => {
    const input = document.getElementById('input').value;
    if (input.substring(0,31) == "https://open.spotify.com/track/"){
        const songId = input.substring(31,53);
        console.log(songId);
        genreAPI(songId);
    } else {
        alert("That's not a valid spotify link 🤨");
        return;
    }
});