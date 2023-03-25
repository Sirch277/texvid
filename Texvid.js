const form = document.getElementById("text-form");
const textInput = document.getElementById("text-input");
const submitButton = document.getElementById("submit-button");
const videoContainer = document.getElementById("video-container");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = textInput.value;
  submitButton.disabled = true;
  submitButton.innerHTML = "Converting...";
  fetch("/text-to-video", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: new URLSearchParams({
      text: text
    })
  })
    .then(response => {
      submitButton.disabled = false;
      submitButton.innerHTML = "Convert to Video";
      if (response.ok) {
        return response.blob();
      } else {
        throw new Error("Conversion failed");
      }
    })
    .then(blob => {
      const video = document.createElement("video");
      video.src = URL.createObjectURL(blob);
      video.autoplay = true;
      video.controls = true;
      videoContainer.innerHTML = "";
      videoContainer.appendChild(video);
      videoContainer.style.display = "block";
    })
    .catch(error => {
      console.error(error);
      alert("Conversion failed");
      submitButton.disabled = false;
      submitButton.innerHTML = "Convert to Video";
    });
});