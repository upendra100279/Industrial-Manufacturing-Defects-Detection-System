/**
 * Reusable stat card for the dashboard's top row of metrics.
 */
export default function StatCard({ icon: Icon, label, value, accent = "primary" }) {
  const accentClasses = {
    primary: "bg-primary-50 text-primary-600 dark:bg-primary-700/20 dark:text-primary-400",
    danger: "bg-red-50 text-danger-600 dark:bg-red-900/20 dark:text-danger-500",
    success: "bg-green-50 text-success-600 dark:bg-green-900/20 dark:text-success-500",
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${accentClasses[accent]}`}>
          <Icon size={22} />
        </div>
      </div>
    </div>
  );
}
