async function startRecording() {
    const resultDiv = document.getElementById('result');
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    let audioChunks = [];

    mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recording.wav');

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        resultDiv.innerHTML = `😊 Emotion: <b>${data.label}</b> <br> 🔥 Confidence: ${data.score}`;
        audioChunks = [];
    };

    resultDiv.innerHTML = "🎙 Recording... Speak now!";
    mediaRecorder.start();

    setTimeout(() => {
        mediaRecorder.stop();
    }, 3000); // Record for 3 seconds
}
