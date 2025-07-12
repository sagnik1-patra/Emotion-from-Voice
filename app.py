from flask import Flask, render_template, request, jsonify
import torch
import soundfile as sf
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor, pipeline
import io

app = Flask(__name__)

# ✅ Load model and feature extractor
model_name = "superb/wav2vec2-base-superb-er"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
classifier = pipeline(
    "audio-classification",
    model=model,
    feature_extractor=feature_extractor,
    device=0 if torch.cuda.is_available() else -1
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No audio data'}), 400

    audio_file = request.files['audio_data']
    audio_bytes = audio_file.read()
    audio_array, samplerate = sf.read(io.BytesIO(audio_bytes))

    prediction = classifier(audio_array)[0]
    return jsonify({
        'label': prediction['label'],
        'score': round(prediction['score'], 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
