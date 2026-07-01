/**
 * Modal showing full detail for a single inspection — annotated image
 * and per-defect breakdown. Fetches the image as a blob lazily.
 */
import { useEffect, useState } from "react";
import { X } from "lucide-react";
import axiosClient from "../../api/axiosClient";
import Loader from "../common/Loader";

export default function InspectionDetailModal({ inspection, onClose }) {
  const [imageUrl, setImageUrl] = useState(null);
  const [loadingImage, setLoadingImage] = useState(true);

  useEffect(() => {
    let objectUrl;
    axiosClient
      .get(`/detect/result/${inspection.id}/image`, { responseType: "blob" })
      .then((res) => {
        objectUrl = URL.createObjectURL(res.data);
        setImageUrl(objectUrl);
      })
      .catch(() => setImageUrl(null))
      .finally(() => setLoadingImage(false));

    return () => objectUrl && URL.revokeObjectURL(objectUrl);
  }, [inspection.id]);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[85vh] overflow-y-auto">
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="font-semibold">Inspection #{inspection.id}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={20} />
          </button>
        </div>

        <div className="p-5 space-y-4">
          {loadingImage ? (
            <Loader />
          ) : imageUrl ? (
            <img src={imageUrl} alt="Inspection result" className="w-full rounded-lg" />
          ) : (
            <p className="text-sm text-gray-400">Image unavailable</p>
          )}

          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-gray-500 dark:text-gray-400">Source</p>
              <p className="font-medium capitalize">{inspection.source_type}</p>
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400">Date</p>
              <p className="font-medium">{new Date(inspection.created_at).toLocaleString()}</p>
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400">Status</p>
              <p className={`font-medium ${inspection.is_defective ? "text-danger-500" : "text-success-500"}`}>
                {inspection.is_defective ? "Defective" : "Pass"}
              </p>
            </div>
            <div>
              <p className="text-gray-500 dark:text-gray-400">Avg Confidence</p>
              <p className="font-medium">{(inspection.avg_confidence * 100).toFixed(1)}%</p>
            </div>
          </div>

          {inspection.detections.length > 0 && (
            <div>
              <p className="text-sm font-medium mb-2">Detected Defects</p>
              <div className="space-y-1.5">
                {inspection.detections.map((d, i) => (
                  <div key={i} className="flex justify-between text-sm bg-gray-50 dark:bg-gray-700/50 px-3 py-2 rounded-lg">
                    <span className="capitalize">{d.class_name}</span>
                    <span className="text-gray-500">{(d.confidence * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
