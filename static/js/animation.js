
window.speechSynthesis.onvoiceschanged = () => {};


let voiceEnabled = true;
let recognition = null;
let recognitionStarted = false;
let userInteracted = false;
let pendingUpload = null; // "image" | "video"


document.addEventListener(
  "click",
  () => {
    userInteracted = true;
  },
  { once: true }
);


function speak(text) {
  if (!voiceEnabled || !userInteracted) return;
  if (!("speechSynthesis" in window)) return;

  speechSynthesis.cancel();

  const msg = new SpeechSynthesisUtterance(text);

  
  msg.rate = 0.85;   
  msg.pitch = 0.7;   // deep robotic tone
  msg.volume = 1.0;

  // Prefer high-quality system voices
  const voices = speechSynthesis.getVoices();
  const roboticVoice = voices.find(v =>
    v.name.includes("Google") ||
    v.name.includes("Microsoft") ||
    v.name.includes("Neural")
  );
  if (roboticVoice) msg.voice = roboticVoice;

  speechSynthesis.speak(msg);
}


/* =====================================================
   PROCESSING VISUAL + AI START SOUND
===================================================== */
function showProcessing() {
  const loader = document.getElementById("ai-loading");
  const startSound = document.getElementById("aiStartSound");

  if (loader) loader.style.display = "flex";

  if (startSound && userInteracted) {
    startSound.pause();
    startSound.currentTime = 0;
    startSound.loop = true;
    startSound.volume = 0.45;
    startSound.play().catch(() => {});
  }
}

function hideProcessing() {
  const loader = document.getElementById("ai-loading");
  const startSound = document.getElementById("aiStartSound");

  if (loader) loader.style.display = "none";

  if (startSound) {
    startSound.pause();
    startSound.currentTime = 0;
    startSound.loop = false;
  }
}


/* =====================================================
   GREETING (ONCE PER SESSION – ROBOTIC)
===================================================== */
window.addEventListener("load", () => {
  if (!sessionStorage.getItem("greeted")) {
    setTimeout(() => {
      speak(
        "Welcome Siddharth. Neural network initialized. Ready for detection."
      );
    }, 1200);
    sessionStorage.setItem("greeted", "true");
  }
});


/* =====================================================
   FORM SUBMIT HANDLER (IMAGE / VIDEO)
===================================================== */
document.querySelectorAll("form").forEach(form => {
  form.addEventListener("submit", () => {
    const fileInput = form.querySelector("input[type='file']");
    if (!fileInput || !fileInput.files.length) return;

    showProcessing();
    speak("Neural network is processing.");
  });
});


/* =====================================================
   RESULT PAGE HANDLER (VIDEO COMPLETE)
===================================================== */
window.addEventListener("load", () => {
  if (document.querySelector("video")) {
    hideProcessing();

    const doneSound = document.getElementById("aiDoneSound");
    if (doneSound && userInteracted) {
      doneSound.volume = 0.6;
      doneSound.play().catch(() => {});
    }

    speak("Processing completed successfully.");
  }
});


function openImagePicker() {
  const input = document.getElementById("imageInput");
  if (input) input.click();
}

function openVideoPicker() {
  const input = document.getElementById("videoInput");
  if (input) input.click();
}


function startVoiceCommands() {
  if (!("webkitSpeechRecognition" in window) || !userInteracted) return;

  recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onstart = () => {
    recognitionStarted = true;
    speak("Voice commands activated.");
    console.log("🎙 Voice recognition ON");
  };

  recognition.onerror = e => {
    console.warn("Voice error:", e.error);
  };

  recognition.onend = () => {
    recognitionStarted = false;
    if (document.visibilityState === "visible") {
      setTimeout(startVoiceCommands, 1000);
    }
  };

  recognition.onresult = e => {
    const cmd =
      e.results[e.results.length - 1][0]
        .transcript.toLowerCase().trim();

    console.log("🎙 Command:", cmd);

    const video = document.querySelector("video");

    /* ---------- IMAGE UPLOAD ---------- */
    if (cmd.includes("upload image")) {
      pendingUpload = "image";
      speak("Image upload ready. Say confirm upload or click choose image.");
      document.getElementById("imageCard")?.classList.add("highlight");
    }

    /* ---------- VIDEO UPLOAD ---------- */
    else if (cmd.includes("upload video")) {
      pendingUpload = "video";
      speak("Video upload ready. Say confirm upload or click choose video.");
      document.getElementById("videoCard")?.classList.add("highlight");
    }

    /* ---------- CONFIRM UPLOAD ---------- */
    else if (cmd.includes("confirm upload")) {
      if (pendingUpload === "image") openImagePicker();
      if (pendingUpload === "video") openVideoPicker();
      speak("Opening file manager.");
      pendingUpload = null;
    }

    /* ---------- VIDEO CONTROL ---------- */
    else if (cmd.includes("play video")) {
      if (video) {
        video.play();
        speak("Playing video.");
      }
    }

    else if (cmd.includes("stop video")) {
      if (video) {
        video.pause();
        speak("Video stopped.");
      }
    }

    
    else if (cmd.includes("start webcam")) {
      speak("Starting webcam detection.");
      window.location.href = "/webcam";
    }

    else if (cmd.includes("stop detection")) {
      speak("Stopping detection.");
      window.location.href = "/dashboard";
    }

  
    else if (cmd.includes("mute voice")) {
      voiceEnabled = false;
      speechSynthesis.cancel();
      console.log("🔇 Voice muted");
    }

    else if (cmd.includes("unmute voice")) {
      voiceEnabled = true;
      speak("Voice enabled.");
    }
  };

  recognition.start();
}


document.addEventListener(
  "click",
  () => {
    if (!recognitionStarted) startVoiceCommands();
  },
  { once: true }
);


function captureFrame() {
  const img = document.getElementById("liveCam");
  const canvas = document.getElementById("canvas");
  const fileInput = document.getElementById("capturedFile");
  const form = document.getElementById("captureForm");

  if (!img || !canvas || !fileInput || !form) {
    alert("Webcam not ready.");
    return;
  }

  if (!img.complete || img.naturalWidth === 0) {
    alert("Webcam feed not ready yet.");
    return;
  }

  showProcessing();

  const ctx = canvas.getContext("2d");
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  ctx.drawImage(img, 0, 0);

  canvas.toBlob(blob => {
    if (!blob) {
      hideProcessing();
      alert("Capture failed.");
      return;
    }

    const file = new File([blob], "webcam.jpg", { type: "image/jpeg" });
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    form.submit();
  }, "image/jpeg", 0.95);
}

