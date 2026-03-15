// Lấy các phần tử cần sử dụng cho cả hai khu vực (Left và Right)
const imageInputLeft = document.getElementById('imageInputLeft');
const imageContainerLeft = document.getElementById('imageContainerLeft');
const previewImageLeft = document.getElementById('previewImageLeft');
const placeholderTextLeft = imageContainerLeft ? imageContainerLeft.querySelector('span') : null;

const imageInputRight = document.getElementById('imageInputRight');
const imageContainerRight = document.getElementById('imageContainerRight');
const previewImageRight = document.getElementById('previewImageRight');
const placeholderTextRight = imageContainerRight ? imageContainerRight.querySelector('span') : null;

// Xử lý sự kiện khi người dùng chọn ảnh cho Left
imageInputLeft.addEventListener('change', async (event) => {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            previewImageLeft.src = e.target.result;
            previewImageLeft.style.display = 'block';
            placeholderTextLeft.style.display = 'none';

            // Gửi ảnh lên server để nhận diện biển số xe
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/process-image', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                // Hiển thị ảnh đã xử lý ở bên phải
                previewImageRight.src = data.processed_image_url; // Đường dẫn ảnh sau khi xử lý
                previewImageRight.style.display = 'block';
                placeholderTextRight.style.display = 'none';
                
            } else {
                alert('Error processing the image.');
            }
        };

        reader.readAsDataURL(file);
    }
});

