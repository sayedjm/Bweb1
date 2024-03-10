$(document).ready(function () {
    let offset = 5;
    const fetchButton = $("#fetch-more-btn");

    function fetchArticles() {
        const maxResults = 5;
        const query = "Sarscov2";

        fetchButton.prop('disabled', true);
        fetchButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...');

        $.ajax({
            url: `/articles/?offset=${offset}&max_results=${maxResults}&query=${query}`,
            method: "GET",
            success: function (data) {
                updateUI(data);
            },
            error: function (error) {
                console.error("Error fetching articles:", error);
            },
            complete: function () {
                fetchButton.prop('disabled', false);
                fetchButton.text('Fetch More Articles');
            }
        });
    }

    function updateUI(articles) {
        const articlesContainer = $("#articles-container tbody");

        for (const key in articles) {
            const value = articles[key];
            const articleHtml = `
                <tr>
                    <td>${key}</td>
                    <td>${value.author}</td>
                    <td>${value.date_of_publication}</td>
                    <td>
                        <button type="button" class="btn btn-secondary btn-sm"
                                onclick="toggleAbstract('${key}')">Show Abstract
                        </button>
                    </td>
                    <td>
                        <button type="button" class="btn btn-secondary btn-sm">
                            <a href="${value.link}" target="_blank"
                               style="color: white; text-decoration: none;">View on PubMed</a>
                        </button>
                    </td>
                </tr>
                <tr>
                    <td colspan="5">
                        <div id="abstract_${key}" style="display: none;">
                            <strong>Abstract:</strong> ${value.abstract}
                        </div>
                    </td>
                </tr>
            `;

            articlesContainer.append(articleHtml);
        }

        offset += Object.keys(articles).length;
    }

    fetchButton.on("click", function () {
        fetchArticles();
    });

    fetchArticles();
});
