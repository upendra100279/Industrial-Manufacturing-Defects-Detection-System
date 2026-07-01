export default function Loader({ fullScreen = false }) {
  const wrapperClass = fullScreen
    ? "h-screen w-full flex items-center justify-center"
    : "flex items-center justify-center py-8";

  return (
    <div className={wrapperClass}>
      <div className="h-8 w-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
