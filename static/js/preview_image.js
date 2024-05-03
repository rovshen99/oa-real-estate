console.log("preview1")
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('.custom-file-input');
    console.log("preview2")
    console.log(inputs)
    inputs.forEach(input => {
        const id = input.id;
        const existingPreview = document.querySelector(`img[for="${id}"]`);
        input.addEventListener('change', function (event) {
            console.log("preview3")
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const src = e.target.result;
                    if (existingPreview) {
                        existingPreview.src = src;
                    } else {
                        const img = document.createElement('img');
                        img.src = src;
                        img.setAttribute('for', id);
                        img.style.width = '150px';
                        img.style.height = 'auto';
                        img.style.marginTop = '10px';
                        input.parentNode.parentNode.appendChild(img);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });
});
