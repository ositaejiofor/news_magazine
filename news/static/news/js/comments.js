document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Clear previous error messages
            const oldError = this.querySelector('.form-error');
            if (oldError) oldError.remove();

            const formData = new FormData(this);
            const url = this.dataset.url;

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                const parent_id = formData.get('parent_id');
                const newComment = document.createElement('div');
                newComment.className = parent_id ? 'ms-4 mt-2 border-start ps-3' : 'mb-3';
                newComment.innerHTML = `
                    <div>
                        <strong>${data.username}</strong>
                        <small class="text-muted ms-2">${data.created_at}</small>
                        <p class="mb-1">${data.content}</p>
                        <a class="btn btn-sm btn-link p-0 text-decoration-none"
                           data-bs-toggle="collapse" href="#replyToReplyForm${data.comment_id}" role="button">
                            Reply
                        </a>
                    </div>
                    <div class="collapse mt-2" id="replyToReplyForm${data.comment_id}">
                        <form method="post" class="ms-3" data-url="${url}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${formData.get('csrfmiddlewaretoken')}">
                            <input type="hidden" name="parent_id" value="${data.comment_id}">
                            <textarea name="content" class="form-control mb-2" required></textarea>
                            <button type="submit" class="btn btn-sm btn-primary">Submit Reply</button>
                        </form>
                    </div>
                `;

                // Insert new comment or reply
                if (parent_id) {
                    const parentDiv = document.querySelector(`#replyForm${parent_id}`) || document.querySelector(`#replyToReplyForm${parent_id}`);
                    parentDiv?.parentElement?.appendChild(newComment);
                } else {
                    document.querySelector('.ps-2').prepend(newComment);
                }

                // Reset form and collapse
                this.reset();
                if (this.closest('.collapse')) {
                    const collapse = bootstrap.Collapse.getInstance(this.closest('.collapse'));
                    collapse.hide();
                }
            } else {
                // Show error message below the textarea
                let errorMessage = "An error occurred.";
                if (data.errors && data.errors.content) {
                    errorMessage = data.errors.content.join(', ');
                } else if (data.error) {
                    errorMessage = data.error;
                }

                const errorElement = document.createElement('div');
                errorElement.className = 'form-error text-danger small mt-1';
                errorElement.innerText = errorMessage;

                // Insert error just after textarea
                const textarea = this.querySelector('textarea[name="content"]');
                textarea.parentNode.insertBefore(errorElement, textarea.nextSibling);
            }
        });
    });
});
