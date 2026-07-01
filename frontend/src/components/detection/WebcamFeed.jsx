/**
 * Live webcam defect detection.
 * Captures a frame from <video> via canvas every INTERVAL_MS, posts it
 * to /api/video/webcam-frame, and renders the annotated JPEG returned
 * by the backend directly into an <img> — giving a near real-time
 * "live detection" feel without WebSockets.
 */
import { useRef, useState, useEffect, useCallback } from "react";
import { Camera, Square, Play } from "lucide-react";
import toast from "react-hot-toast";
import axiosClient from "../../api/axiosClient";

const INTERVAL_MS = 800;

export default function WebcamFeed() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const intervalRef = useRef(null);

  const [isActive, setIsActive] = useState(false);
  const [annotatedFrameUrl, setAnnotatedFrameUrl] = useState(null);
  const [processing, setProcessing] = useState(false);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setIsActive(true);
    } catch (err) {
      toast.error("Could not access webcam — check browser permissions");
    }
  };

  const stopWebcam = useCallback(() => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setIsActive(false);
    setAnnotatedFrameUrl(null);
  }, []);

  const captureAndDetect = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current || processing) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      async (blob) => {
        if (!blob) return;
        setProcessing(true);
        const formData = new FormData();
        formData.append("file", blob, "frame.jpg");

        try {
          const res = await axiosClient.post("/video/webcam-frame", formData, {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob",
          });
          setAnnotatedFrameUrl((prev) => {
            if (prev) URL.revokeObjectURL(prev);
            return URL.createObjectURL(res.data);
          });
        } catch (err) {
          // Silently skip a failed frame — next interval will retry
        } finally {
          setProcessing(false);
        }
      },
      "image/jpeg",
      0.85
    );
  }, [processing]);

  useEffect(() => {
    if (isActive) {
      intervalRef.current = setInterval(captureAndDetect, INTERVAL_MS);
    }
    return () => clearInterval(intervalRef.current);
  }, [isActive, captureAndDetect]);

  useEffect(() => () => stopWebcam(), [stopWebcam]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Live Webcam Detection</h3>
        <button
          onClick={isActive ? stopWebcam : startWebcam}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
            isActive
              ? "bg-danger-500 hover:bg-danger-600 text-white"
              : "bg-primary-500 hover:bg-primary-600 text-white"
          }`}
        >
          {isActive ? <Square size={16} /> : <Play size={16} />}
          {isActive ? "Stop" : "Start"}
        </button>
      </div>

      <div className="relative rounded-lg overflow-hidden bg-black aspect-video">
        <video ref={videoRef} className={`w-full h-full object-cover ${annotatedFrameUrl ? "hidden" : ""}`} muted playsInline />
        {annotatedFrameUrl && (
          <img src={annotatedFrameUrl} alt="Live detection" className="w-full h-full object-cover" />
        )}
        <canvas ref={canvasRef} className="hidden" />

        {!isActive && (
          <div className="absolute inset-0 flex items-center justify-center text-gray-400">
            <Camera size={40} />
          </div>
        )}
      </div>

      <p className="text-xs text-gray-400 mt-2">
        Frames are analyzed live and not saved to history. Use "Capture & Save" on the image tab to log an inspection.
      </p>
    </div>
  );
}
