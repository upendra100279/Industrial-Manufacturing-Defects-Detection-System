/**
 * Drag-and-drop image uploader using react-dropzone.
 */
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { UploadCloud, ImageIcon } from "lucide-react";

export default function UploadDropzone({ onFileSelect, previewUrl, disabled }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) onFileSelect(acceptedFiles[0]);
    },
    [onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/jpeg": [], "image/png": [] },
    maxFiles: 1,
    disabled,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition
        ${isDragActive ? "border-primary-500 bg-primary-50 dark:bg-primary-700/10" : "border-gray-300 dark:border-gray-600"}
        ${disabled ? "opacity-60 cursor-not-allowed" : "hover:border-primary-400"}`}
    >
      <input {...getInputProps()} />
      {previewUrl ? (
        <img src={previewUrl} alt="preview" className="max-h-64 mx-auto rounded-lg" />
      ) : (
        <div className="flex flex-col items-center gap-2 text-gray-500 dark:text-gray-400">
          {isDragActive ? <ImageIcon size={36} /> : <UploadCloud size={36} />}
          <p className="font-medium">
            {isDragActive ? "Drop the image here" : "Drag & drop a product image, or click to browse"}
          </p>
          <p className="text-xs">JPEG or PNG, up to 10MB</p>
        </div>
      )}
    </div>
  );
}
