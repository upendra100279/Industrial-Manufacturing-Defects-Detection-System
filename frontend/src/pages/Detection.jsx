/**
 * Detection page — tabbed interface: Image Upload vs Live Webcam.
 */
import { useState } from "react";
import toast from "react-hot-toast";
import { Image as ImageIcon, Video } from "lucide-react";
import axiosClient from "../api/axiosClient";
import UploadDropzone from "../components/detection/UploadDropzone";
import ResultCard from "../components/detection/ResultCard";
import WebcamFeed from "../components/detection/WebcamFeed";
import Loader from "../components/common/Loader";

export default function Detection() {
  const [activeTab, setActiveTab] = useState("image");
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [resultImageUrl, setResultImageUrl] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
    setResultImageUrl(null);
  };

  const handleDetect = async () => {
    if (!file) return;
    setSubmitting(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axiosClient.post("/detect/image", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);

      const imgRes = await axiosClient.get(`/detect/result/${res.data.id}/image`, {
        responseType: "blob",
      });
      setResultImageUrl(URL.createObjectURL(imgRes.data));
      toast.success(
        res.data.is_defective ? `${res.data.defect_count} defect(s) detected` : "No defects found"
      );
    } catch (err) {
      toast.error(err.response?.data?.detail || "Detection failed");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDownload = () => {
    if (!resultImageUrl) return;
    const a = document.createElement("a");
    a.href = resultImageUrl;
    a.download = `inspection_${result.id}.jpg`;
    a.click();
  };

  return (
    <div className="space-y-6">
      <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700">
        {[
          { key: "image", label: "Image Upload", icon: ImageIcon },
          { key: "webcam", label: "Live Webcam", icon: Video },
        ].map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 transition ${
              activeTab === key
                ? "border-primary-500 text-primary-600"
                : "border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
            }`}
          >
            <Icon size={16} /> {label}
          </button>
        ))}
      </div>

      {activeTab === "image" ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-4">
            <UploadDropzone onFileSelect={handleFileSelect} previewUrl={previewUrl} disabled={submitting} />
            <button
              onClick={handleDetect}
              disabled={!file || submitting}
              className="w-full bg-primary-500 hover:bg-primary-600 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition"
            >
              {submitting ? "Analyzing..." : "Run Defect Detection"}
            </button>
          </div>

          <div>
            {submitting ? (
              <Loader />
            ) : result ? (
              <ResultCard result={result} imageUrl={resultImageUrl} onDownload={handleDownload} />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400 text-sm border border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8">
                Upload an image and run detection to see results here
              </div>
            )}
          </div>
        </div>
      ) : (
        <WebcamFeed />
      )}
    </div>
  );
}
