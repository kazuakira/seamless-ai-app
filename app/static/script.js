async function sendImage() {
    const input = document.getElementById('imageInput');
    if (!input.files.length) return;
  
    const formData = new FormData();
    formData.append("file", input.files[0]);
  
    const response = await fetch("/process_image/", {
      method: "POST",
      body: formData
    });
  
    const blob = await response.blob();
    document.getElementById("resultImage").src = URL.createObjectURL(blob);
  }
  