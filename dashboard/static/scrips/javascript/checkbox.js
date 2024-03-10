function enableCheckboxRangeSelection() {
    let table = document.getElementById('corona-table');
    let checkboxes = table.querySelectorAll('input[type="checkbox"]');
    let lastChecked;

    function handleCheckbox(e) {
        let inBetween = false;

        if (e.shiftKey && this.checked) {
            checkboxes.forEach(checkbox => {
                if (checkbox === this || checkbox === lastChecked) {
                    inBetween = !inBetween;
                }

                if (inBetween) {
                    checkbox.checked = true;
                }
            });
        }

        lastChecked = this;
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', handleCheckbox);
    });
}

function check() {
    document.addEventListener('DOMContentLoaded', function () {
        let table = document.getElementById('corona-table');
        let checkboxes = table.querySelectorAll('input[type="checkbox"]');

        let lastChecked;

        function handleCheckbox(e) {
            let inBetween = false;

            if (e.shiftKey && this.checked) {
                checkboxes.forEach(checkbox => {
                    if (checkbox === this || checkbox === lastChecked) {
                        inBetween = !inBetween;
                    }

                    if (inBetween) {
                        checkbox.checked = true;
                    }
                });
            }

            lastChecked = this;
        }

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('click', handleCheckbox);
        });
    });
}


