function sortTable(columnIndex) {
    const table = document.getElementById("corona-table");
    const rows = Array.from(table.rows).slice(1);
    const headerRow = table.rows[0];
    const clickedHeaderCell = headerRow.cells[columnIndex];
    const isAscending = clickedHeaderCell.classList.toggle("asc");

    for (let i = 0; i < headerRow.cells.length; i++) {
        if (i !== columnIndex) {
            headerRow.cells[i].classList.remove("asc");
            headerRow.cells[i].classList.remove("desc");
        }
    }

    if (isAscending) {
        clickedHeaderCell.classList.add("asc");
    } else {
        clickedHeaderCell.classList.add("desc");
    }

    const clickedHeaderCells = table.getElementsByClassName("clicked-header");
    while (clickedHeaderCells.length > 0) {
        clickedHeaderCells[0].classList.remove("clicked-header");
    }

    clickedHeaderCell.classList.add("clicked-header");

    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].innerText;
        const cellB = rowB.cells[columnIndex].innerText;

        if (isNaN(cellA) || isNaN(cellB)) {
            return cellA.localeCompare(cellB);
        } else {
            return parseFloat(cellA) - parseFloat(cellB);
        }
    });

    if (!isAscending) {
        rows.reverse();
    }

    for (let i = 0; i < rows.length; i++) {
        table.tBodies[0].appendChild(rows[i]);
    }
}