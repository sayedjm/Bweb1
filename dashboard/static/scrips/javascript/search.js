function searchTable() {
    const input = document.getElementById("search-box");
    const table = document.getElementById("corona-table");
    const filter = input.value.toUpperCase();
    const rows = table.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
        const td = rows[i].getElementsByTagName("td");
        for (let j = 0; j < td.length; j++) {
            const cell = td[j];
            if (cell) {
                const text = cell.textContent || cell.innerText;
                if (text.toUpperCase().indexOf(filter) > -1) {
                    rows[i].style.display = "";
                    break;
                } else {
                    rows[i].style.display = "none";
                }
            }
        }
    }
}