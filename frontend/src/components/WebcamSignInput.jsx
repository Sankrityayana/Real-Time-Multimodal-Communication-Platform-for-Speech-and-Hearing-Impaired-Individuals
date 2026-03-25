import { useEffect, useRef, useState } from 'react';
import { aiApi } from '../services/api';

export default function WebcamSignInput({ onDetectedText }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [active, setActive] = useState(false);

  useEffect(() => {
    let stream;

    const init = async () => {
      if (!active) return;
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    };

    init();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [active]);

  const captureAndDetect = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg');
    const response = await aiApi.detectSign({ image_base64: dataUrl });

    if (response.data.detected_text) {
      onDetectedText(response.data.detected_text);
    }
  };

  return (
    <section className="rounded-2xl bg-white/90 p-4 shadow-xl">
      <h2 className="font-heading text-xl font-bold text-slate-900">Sign Detection</h2>
      <div className="mt-3 flex flex-wrap gap-3">
        <button
          className="rounded-lg bg-amber px-5 py-3 text-lg font-semibold text-white"
          onClick={() => setActive((prev) => !prev)}
        >
          {active ? 'Stop Webcam' : 'Start Webcam'}
        </button>
        <button
          className="rounded-lg bg-slate-800 px-5 py-3 text-lg font-semibold text-white disabled:opacity-40"
          disabled={!active}
          onClick={captureAndDetect}
        >
          Detect Gesture
        </button>
      </div>
      <div className="mt-4 overflow-hidden rounded-xl border border-slate-300 bg-black/90">
        <video ref={videoRef} autoPlay playsInline className="h-56 w-full object-cover" />
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </section>
  );
}
