/**
 * Deeper analytics view — reuses TrendChart/DefectPieChart with a
 * selectable date range, plus a defect-frequency bar chart.
 */
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import axiosClient from "../api/axiosClient";
import TrendChart from "../components/dashboard/TrendChart";
import Loader from "../components/common/Loader";

const RANGE_OPTIONS = [
  { label: "7 Days", value: 7 },
  { label: "14 Days", value: 14 },
  { label: "30 Days", value: 30 },
  { label: "90 Days", value: 90 },
];

export default function Analytics() {
  const [range, setRange] = useState(14);
  const [trend, setTrend] = useState([]);
  const [defectFreq, setDefectFreq] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [trendRes, freqRes] = await Promise.all([
          axiosClient.get(`/analytics/trend?days=${range}`),
          axiosClient.get("/analytics/defect-frequency"),
        ]);
        setTrend(trendRes.data);
        setDefectFreq(freqRes.data);
      } catch (err) {
        toast.error("Failed to load analytics");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [range]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-lg">Defect Analytics</h3>
        <div className="flex gap-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
          {RANGE_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setRange(opt.value)}
              className={`px-3 py-1.5 text-sm rounded-md transition ${
                range === opt.value
                  ? "bg-white dark:bg-gray-600 shadow-sm font-medium"
                  : "text-gray-500 dark:text-gray-400"
              }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <Loader />
      ) : (
        <div className="space-y-6">
          <TrendChart data={trend} />

          <div className="bg-white dark:bg-gray-800 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-gray-700">
            <h3 className="font-semibold mb-4">Defect Count by Type</h3>
            {defectFreq.length === 0 ? (
              <p className="text-gray-400 text-sm py-8 text-center">No defects recorded yet</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={defectFreq} layout="vertical" margin={{ left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis type="number" allowDecimals={false} />
                  <YAxis type="category" dataKey="class_name" width={100} tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b6fed" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
