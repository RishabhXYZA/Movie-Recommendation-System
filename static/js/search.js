const input = document.getElementById("search-input");
const suggestionsBox = document.getElementById("suggestions");

input.addEventListener("input", async () => {
    const query = input.value.trim();

    if (query.length < 2) {
        suggestionsBox.innerHTML = "";
        return;
    }

    const response = await fetch(`/autocomplete?q=${query}`);
    const movies = await response.json();

    suggestionsBox.innerHTML = "";

    movies.forEach(movie => {
        const div = document.createElement("div");
        div.className = "suggestion-item";
        div.innerText = movie.title;

        div.onclick = () => {
            window.location.href = `/movie/${movie.id}`;
        };

        suggestionsBox.appendChild(div);
    });
});
