function setupImagePreview() {
  const fileInput = document.getElementById('image-input');
  const image = document.querySelector('#profile-image');

  if (fileInput && image) {
    fileInput.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file && file.type.includes('image')) {
        const url = URL.createObjectURL(file);
        image.src = url;
      }
    });
  }
}

setupImagePreview();

document.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target.id === "contact-create-form") {
    setupImagePreview();
  }
});