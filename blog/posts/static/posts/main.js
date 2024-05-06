$(document).ready(function() {
    loadLikedPosts();
    setupModal();
    setupModalApi();
    setupLikeButton();
    checkLikedPosts();
});

function updateFileName(input) {
    if (input.files && input.files[0]) {
        var fileName = input.files[0].name;
        document.getElementById('selectedFile').style.display = 'block'; // Показываем элемент
        document.getElementById('selectedFile').innerText = 'Выбрано: ' + fileName; // Обновляем текст
    } else {
        document.getElementById('selectedFile').style.display = 'none'; // Скрываем элемент
    }
}

function loadLikedPosts() {
    $.ajax({
        type: 'GET',
        url: 'posts/liked_posts/',
        success: function(response) {
            response.likedPosts.forEach(function(postId) {
                localStorage.setItem(`liked-${postId}`, 'true');
            });
            checkLikedPosts();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error: " + errorThrown);
        }
    });
}

function setupModal() {
    $('a[data-toggle="modal"]').on('click', function() {
        var target = $(this).attr('data-target');
        $(target).modal('show');
    });
}

function setupModalApi() {
    $('a[data-toggle="modalApi"]').on('click', function() {
        var target = $(this).attr('data-target');
        $(target).modal('show');

        // Добавляем обработчик события отправки формы
        $(target).find('#postForm').on('submit', function(event) {
            event.preventDefault();

            var topic = $(target).find('#postContent').val();

            // Получаем CSRF токен из метаданных страницы
            var csrftoken = $('[name=csrfmiddlewaretoken]').val();

            $.ajax({
                type: 'POST',
                url: '/api/generate_text/',
                data: {
                    topic: topic,
                    csrfmiddlewaretoken: csrftoken  // Добавляем CSRF токен в данные запроса
                },
                success: function(response) {
                    var generatedText = response.text;

                    // Показываем кнопку "Посмотреть пост"
                    $(target).find('#viewPostBtn').show();

                    // Передаем значение topic в модальное окно создания поста
                    var postModal = $('#postModal');
                    postModal.find('#title').val(topic);
                    postModal.find('#description').val(generatedText); // Передаем сгенерированный текст в поле "Описание"
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Failed to generate post:', errorThrown);
                }
            });
        });

        // Добавляем обработчик клика на кнопку "Посмотреть пост"
        $(target).find('#viewPostBtn').on('click', function() {
            var postModal = $('#postModal');
            postModal.modal('show');
            $(target).modal('hide'); // Закрываем модальное окно с формой для генерации текста
        });
    });
}




function setupLikeButton() {
    $('.like-btn').click(function() {
        var postId = $(this).data('post-id');
        var likeButton = $(this);
        $.ajax({
            type: 'POST',
            url: '/posts/like_post/' + postId + '/',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                $('#like-count-' + postId).text(response.likes_count);
                updateLikeButton(likeButton, response.message);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert("Error: " + errorThrown);
            }
        });
    });
}



function checkLikedPosts() {
    $('.like-btn').each(function() {
        var postId = $(this).data('post-id');
        var isLiked = localStorage.getItem(`liked-${postId}`) === 'true';
        var likeButton = $(this);
        updateLikeButton(likeButton, isLiked ? 'Liked' : 'Not Liked');
    });
}

function updateLikeButton(likeButton, status) {
    if (status === 'Liked') {
        likeButton.find('i').css('color', 'red');
        localStorage.setItem(`liked-${likeButton.data('post-id')}`, 'true');
    } else {
        likeButton.find('i').css('color', 'gray');
        localStorage.setItem(`liked-${likeButton.data('post-id')}`, 'false');
    }
}

function clearLocalStorage() {
    localStorage.clear();
}
