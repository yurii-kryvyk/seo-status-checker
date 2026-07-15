const textarea = document.getElementById("urls");

const checkButton = document.getElementById("check-button");
const clearButton = document.getElementById("clear-button");

const searchInput = document.getElementById("search");

const tableBody = document.getElementById("results-body");

const totalCount = document.getElementById("total-count");
const successCount = document.getElementById("success-count");
const redirectCount = document.getElementById("redirect-count");
const clientErrorCount = document.getElementById("client-error-count");
const serverErrorCount = document.getElementById("server-error-count");

const sortableHeaders = document.querySelectorAll(".sortable");

let currentResults = [];

let currentSort = "url";
let sortAscending = true;


checkButton.addEventListener("click", checkUrls);
clearButton.addEventListener("click", clearPage);

searchInput.addEventListener("input", updateView);


sortableHeaders.forEach(header => {

    header.addEventListener("click", () => {

        const field = header.dataset.sort;

        if (currentSort === field) {
            sortAscending = !sortAscending;
        } else {
            currentSort = field;
            sortAscending = true;
        }

        updateView();

    });

});


async function checkUrls() {

    const urls = textarea.value
        .split("\n")
        .map(url => url.trim())
        .filter(url => url !== "");

    if (urls.length === 0) {
        alert("Enter at least one URL.");
        return;
    }

    try {

        checkButton.disabled = true;
        checkButton.textContent = "Checking...";

        const response = await fetch("/check", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                urls: urls
            })

        });

        if (!response.ok) {
            throw new Error("Server Error");
        }

        currentResults = await response.json();

        updateCounters(currentResults);

        updateView();

    } catch (error) {

        console.error(error);

        alert("Failed to check URLs.");

    } finally {

        checkButton.disabled = false;
        checkButton.textContent = "Check";

    }

}


function updateView() {

    let results = [...currentResults];

    const search = searchInput.value
        .trim()
        .toLowerCase();

    if (search !== "") {

        results = results.filter(result =>
            result.url.toLowerCase().includes(search)
        );

    }

    switch (currentSort) {

        case "url":

            results.sort((a, b) =>
                a.url.localeCompare(b.url)
            );

            break;

        case "status":

            results.sort((a, b) =>
                (a.status_code ?? 999) -
                (b.status_code ?? 999)
            );

            break;

        case "time":

            results.sort((a, b) =>
                (a.response_time ?? Number.MAX_VALUE) -
                (b.response_time ?? Number.MAX_VALUE)
            );

            break;

    }

    if (!sortAscending) {
        results.reverse();
    }

    renderTable(results);

    updateSortIcons();

}


function renderTable(results) {

    tableBody.innerHTML = "";

    for (const result of results) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${result.url}</td>
            <td>${result.status_code ?? "-"}</td>
            <td class="${getStatusClass(result.category)}">
                ${result.status}
            </td>
            <td>${result.response_time ?? "-"} ms</td>
        `;

        tableBody.appendChild(row);

    }

}


function updateCounters(results) {

    totalCount.textContent = results.length;

    let success = 0;
    let redirect = 0;
    let client = 0;
    let server = 0;

    for (const result of results) {

        switch (result.category) {

            case "success":
                success++;
                break;

            case "redirect":
                redirect++;
                break;

            case "client_error":
                client++;
                break;

            case "server_error":
                server++;
                break;

        }

    }

    successCount.textContent = success;
    redirectCount.textContent = redirect;
    clientErrorCount.textContent = client;
    serverErrorCount.textContent = server;

}


function clearPage() {

    textarea.value = "";

    searchInput.value = "";

    currentResults = [];

    currentSort = "url";
    sortAscending = true;

    tableBody.innerHTML = "";

    totalCount.textContent = 0;
    successCount.textContent = 0;
    redirectCount.textContent = 0;
    clientErrorCount.textContent = 0;
    serverErrorCount.textContent = 0;

    updateSortIcons();

}


function updateSortIcons() {

    sortableHeaders.forEach(header => {

        const icon = header.querySelector(".sort-icon");

        if (!icon) {
            return;
        }

        if (header.dataset.sort !== currentSort) {

            icon.textContent = "⇅";

            return;

        }

        icon.textContent = sortAscending ? "↑" : "↓";

    });

}


function getStatusClass(category) {

    switch (category) {

        case "success":
            return "status-success";

        case "redirect":
            return "status-redirect";

        case "client_error":
            return "status-client-error";

        case "server_error":
            return "status-server-error";

        case "timeout":
            return "status-timeout";

        default:
            return "status-error";

    }

}


updateSortIcons();
