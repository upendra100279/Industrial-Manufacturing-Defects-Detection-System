/**
 * Displays detection results: annotated image, defect badge,
 * per-defect confidence list, and a download button.
 */
import { AlertCircle, CheckCircle, Download } from "lucide-react";

export default function ResultCard({ result, imageUrl, onDownload }) {
  if (!result) return null;
  const { is_defective, defect_count, avg_confidence, detections } = result;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <div
          className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${
            is_defective
              ? "bg-red-50 text-danger-600 dark:bg-red-900/20"
              : "bg-green-50 text-success-600 dark:bg-green-900/20"
          }`}
        >
          {is_defective ? <AlertCircle size={16} /> : <CheckCircle size={16} />}
          {is_defective ? `${defect_count} Defect(s) Found` : "No Defects Detected"}
        </div>

        <button
          onClick={onDownload}
          className="flex items-center gap-1.5 text-sm font-medium text-primary-600 hover:text-primary-700"
        >
          <Download size={16} /> Download
        </button>
      </div>

      {imageUrl && (
        <img src={imageUrl} alt="Annotated result" className="w-full rounded-lg mb-4 border border-gray-100 dark:border-gray-700" />
      )}

      {detections && detections.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Average Confidence: {(avg_confidence * 100).toFixed(1)}%
          </p>
          {detections.map((d, i) => (
            <div
              key={i}
              className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-700/50 px-3 py-2 rounded-lg"
            >
              <span className="font-medium capitalize">{d.class_name}</span>
              <span className="text-gray-500 dark:text-gray-400">{(d.confidence * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
