// main.js
$(document).ready(function() {
    loadLikedPosts();
    setupModal();
    setupLikeButton();
    checkLikedPosts();
});

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
