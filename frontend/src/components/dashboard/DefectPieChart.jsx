/**
 * Pie chart of defect frequency by class, fed by
 * /api/analytics/defect-frequency.
 */
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";

const COLORS = ["#3b6fed", "#ef4444", "#f59e0b", "#22c55e", "#8b5cf6", "#06b6d4"];

export default function DefectPieChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-center h-[320px]">
        <p className="text-gray-400 text-sm">No defect data yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <h3 className="font-semibold mb-4">Defect Frequency by Type</h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="count"
            nameKey="class_name"
            cx="50%"
            cy="50%"
            outerRadius={90}
            label={({ class_name, count }) => `${class_name}: ${count}`}
          >
            {data.map((_, idx) => (
              <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
