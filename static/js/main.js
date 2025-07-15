$(document).ready(function() {
    loadArticles();

    function loadArticles() {
        $.get("/articles", function(data) {
            let html = '';
            data.forEach(article => {
                html += `
            <li class="list-group-item">
                <h5>${article.title}</h5>
                <p>${article.content}</p>
                <button class="btn btn-sm btn-warning edit-btn" data-id="${article.id}" data-title="${article.title}" data-content="${article.content}">Edit</button>
                <button class="btn btn-sm btn-danger delete-btn" data-id="${article.id}">Delete</button>
            </li>`;
            });
            $("#articleList").html(html);
        });
    }
    // 🟢 Submit Article Form
    $("#articleForm").submit(function(e) {
        e.preventDefault();
        const id = $("#article_id").val();
        const title = $("#title").val();
        const content = $("#content").val();

        const url = id ?
            `/articles/edit/${id}` // if id exists → Edit
            :
            "/articles/create"; // else → Create

        $.post(url, { title, content }, function() {
            $("#article_id").val('');
            $("#title").val('');
            $("#content").val('');
            loadArticles();
        }).fail(function(xhr) {
            alert("Save Error: " + xhr.responseJSON.message);
        });
    });
    // 🟡 Edit Article
    $(document).on("click", ".edit-btn", function() {
        const id = $(this).data("id");
        const title = $(this).data("title");
        const content = $(this).data("content");

        $("#article_id").val(id);
        $("#title").val(title);
        $("#content").val(content);
    });

    // 🔴 Delete Article
    $(document).on("click", ".delete-btn", function() {
        const id = $(this).data("id");

        $.post(`/articles/delete/${id}`, function() {
            loadArticles();
        }).fail(function(xhr) {
            alert("Delete Error: " + xhr.responseJSON.message);
        });
    });

});