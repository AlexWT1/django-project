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
        document.getElementById('selectedFile').style.display = 'block';
        document.getElementById('selectedFile').innerText = 'Выбрано: ' + fileName;
    } else {
        document.getElementById('selectedFile').style.display = 'none';
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

        $(target).find('#postForm').on('submit', function(event) {
            event.preventDefault();

            var topic = $(target).find('#postContent').val();

            var csrftoken = $('[name=csrfmiddlewaretoken]').val();

            $.ajax({
                type: 'POST',
                url: '/api/generate_text/',
                data: {
                    topic: topic,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(response) {
                    var generatedText = response.text;

                    $(target).find('#viewPostBtn').show();

                    var postModal = $('#postModal');
                    postModal.find('#title').val(topic);
                    postModal.find('#description').val(generatedText);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error('Failed to generate post:', errorThrown);
                }
            });
        });

        $(target).find('#viewPostBtn').on('click', function() {
            var postModal = $('#postModal');
            postModal.modal('show');
            $(target).modal('hide');
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
