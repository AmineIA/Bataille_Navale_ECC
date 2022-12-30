window.onload = function () {
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get("game-id");
    const playerName = urlParams.get("player-name");
    document.getElementById("game-id").value = gameId;
    document.getElementById("player-name").value = playerName;
}
async function getPlayer(gameId, playerName) {
    const resource_url = host + "/get-player?game_id=" + gameId + "&player_name=" +
        playerName;
    const response = await getData(resource_url);
    if (!response.ok) {
        return { player_name: playerName, battle_field: { vessels: [] } };
    } else {
        return response.json();
    }
}

<script src="scripts/create-game.js"></script>
window.onload = function () {
    const urlParams = new URLSearchParams(window.location.search);
    const gameId = urlParams.get("game-id");
    const playerName = urlParams.get("player-name");
    document.getElementById("game-id").value = gameId;
    document.getElementById("player-name").value = playerName;
}
// Constante o� on stock le host du serveur contenant l'api (http://localhost:5000)
const host = window.location.protocol + "//" + window.location.host;
// url compl�te de l'api create-game
const url = host + "/create-game";
// Au chargement de la page, on ajoute un listener au formulaire create-game-form,
// � la soumission la fonction create_game(event) sera appel�e
window.onload = function () {
    const createGameForm = document.getElementById("create-game-form");
    if (createGameForm != null) {
        createGameForm.addEventListener("submit", create_game);
    }
};
async function create_game(event) {
    event.preventDefault();
    console.log("start request")
    // R�cup�rer l'objet qui repr�sente le fomulaire concern�
    const form = event.currentTarget;
    const formData = new FormData(form);
    // R�cup�rer l'objet contenant les donn�es de notre formulaire
    // notez que les attributs name des elements html du formulaire doivent
    // contenir les m�mes noms attendus par l�api
    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);
    // Appel de l'API create-game qui se fait en asynchrone
    // le await pour stocker le r�sultat dans response quand il sera re�u
    const response = await postData(url, formDataJsonString)
    // R�cup�rer l'element html identifi� par "create-game-result"
    // afin de mettre le message de retour de l'api
    const resultCreateGame = document.getElementById("create-game-result");
    let h1 = document.createElement('H1');
    resultCreateGame.appendChild(h1)
    if (!response.ok) {
        // le await est ajout� ici parceque response est un objet qu'on recevra plutard en
        asynchrone
        const error = await response.json();
        console.log(error)
        h1.innerHTML = "Erreur: " + error.message;
        h1.className = "error";
    } else {
        const gameId = await response.json();
        h1.innerHTML = "Partie cr��e avec l'id : " + gameId + "<br>";
        // Dans l'element html qui contient le r�sultat on ajoute un lien
        // pour diriger l'utilisateur vers la page de gestion de cr�ation des vaisseaux
        // avec l'id de la partie cr��e :
        // http://localhost:5000/views/manage_fleet.html?game-id=4&player-name=Tatanor
        let linkToVessels = document.createElement("a");
        const playerName = document.getElementById("player-name").value;
        linkToVessels.href = "manage_fleet.html?game-id=" + gameId + "&player-name=" +
            playerName;
        linkToVessels.text = "Cr�er votre flotte !"
        h1.appendChild(linkToVessels);
        h1.className = "success";
    }
    // on r�cup�re l'objet repr�sentant le formulaire et le masquer
    // on aurait pu utiliser l'objet form r�cup�r� plus haut avec : const form =
    event.currentTarget;
    const createGameForm = document.getElementById("create-game-form");
    createGameForm.style.visibility = "hidden";
    // On affiche la balise r�sultat
    resultCreateGame.style.visibility = "visible";
}
// Fonction pour appeler l'api en POST avec les donn�es data
// les appels api sont toujours en asynchrone en javascript
// afin de ne pas bloquer le navigateur dans l'attente de la r�ponse
async function postData(url = '', data) {
    const fetchOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: data,
    };
    return fetch(url, fetchOptions);
}