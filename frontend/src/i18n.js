import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      title: 'Real-Time Multimodal Communication Platform',
      subtitle: 'Accessible communication across speech, text, and sign language.',
      microphone: 'Microphone',
      startRecording: 'Start Recording',
      stopRecording: 'Stop Recording',
      transcribe: 'Transcribe',
      signDetection: 'Sign Detection',
      startWebcam: 'Start Webcam',
      stopWebcam: 'Stop Webcam',
      detectGesture: 'Detect Gesture',
      liveTranscript: 'Live Transcript',
      transcriptHint: 'Transcribed speech and detected signs appear here.',
      textToSpeech: 'Text to Speech',
      playLatest: 'Play Latest Message',
      typeMessage: 'Type Message',
      typePlaceholder: 'Type text to share...',
      send: 'Send',
      conversation: 'Conversation',
      noMessages: 'No messages yet. Start speaking, typing, or signing.'
    }
  },
  hi: {
    translation: {
      title: 'रीयल-टाइम मल्टीमोडल कम्युनिकेशन प्लेटफॉर्म',
      subtitle: 'बोलकर, लिखकर और सांकेतिक भाषा से सुलभ संवाद।',
      microphone: 'माइक्रोफोन',
      startRecording: 'रिकॉर्डिंग शुरू करें',
      stopRecording: 'रिकॉर्डिंग बंद करें',
      transcribe: 'ट्रांसक्राइब करें',
      signDetection: 'साइन डिटेक्शन',
      startWebcam: 'वेबकैम शुरू करें',
      stopWebcam: 'वेबकैम बंद करें',
      detectGesture: 'जेस्चर पहचानें',
      liveTranscript: 'लाइव ट्रांसक्रिप्ट',
      transcriptHint: 'ट्रांसक्राइब किया गया टेक्स्ट यहां दिखेगा।',
      textToSpeech: 'टेक्स्ट से आवाज',
      playLatest: 'नवीनतम संदेश चलाएं',
      typeMessage: 'संदेश लिखें',
      typePlaceholder: 'साझा करने के लिए टेक्स्ट लिखें...',
      send: 'भेजें',
      conversation: 'बातचीत',
      noMessages: 'अभी कोई संदेश नहीं। बोलकर, लिखकर, या साइन से शुरू करें।'
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false }
});

export default i18n;
