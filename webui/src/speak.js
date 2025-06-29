import * as sdk from 'microsoft-cognitiveservices-speech-sdk';

export const speakText = (text) => {
  const speechConfig = sdk.SpeechConfig.fromSubscription(
    process.env.REACT_APP_AZURE_SPEECH_KEY,
    process.env.REACT_APP_AZURE_REGION
  );

  speechConfig.speechSynthesisVoiceName = "en-US-AvaMultilingualNeural";

  const audioConfig = sdk.AudioConfig.fromDefaultSpeakerOutput();
  const synthesizer = new sdk.SpeechSynthesizer(speechConfig, audioConfig);

  synthesizer.speakTextAsync(
    text,
    (result) => {
      if (result.reason === sdk.ResultReason.SynthesizingAudioCompleted) {
        console.log("✅ Speech synthesized successfully.");
      } else {
        console.error("❌ Synthesis failed:", result.errorDetails);
      }
      synthesizer.close();
    },
    (err) => {
      console.error("❌ TTS error:", err);
      synthesizer.close();
    }
  );
};
