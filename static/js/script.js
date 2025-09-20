function toggleSelection(videoId) {
    fetch(`/select_video/${videoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update the button appearance
        const button = document.querySelector(`[data-video-id="${videoId}"]`);
        const videoCard = button.closest('.video-card');
        
        if (data.selected) {
            button.innerHTML = '<i class="fas fa-check-circle"></i> Selected';
            button.classList.remove('btn-unselected');
            button.classList.add('btn-selected');
            videoCard.classList.add('selected');
        } else {
            button.innerHTML = '<i class="fas fa-circle"></i> Select';
            button.classList.remove('btn-selected');
            button.classList.add('btn-unselected');
            videoCard.classList.remove('selected');
        }
        
        // Reload the page to update the selected videos list
        setTimeout(() => {
            location.reload();
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating selection');
    });
}

// File upload preview (optional enhancement)
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('video');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const files = this.files;
            if (files.length > 0) {
                alert(`Selected ${files.length} file(s) for upload`);
            }
        });
    }
    
    // Add smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

