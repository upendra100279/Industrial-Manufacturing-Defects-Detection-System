/**
 * Line chart of daily total vs. defective inspections, fed by
 * /api/analytics/trend. Uses Recharts.
 */
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";

export default function TrendChart({ data }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
      <h3 className="font-semibold mb-4">Inspection Trend (Last 14 Days)</h3>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="total" stroke="#3b6fed" strokeWidth={2} name="Total" />
          <Line type="monotone" dataKey="defective" stroke="#ef4444" strokeWidth={2} name="Defective" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
