import { useEffect, useState } from "react";
import { ClipboardList, AlertTriangle, CheckCircle2, Gauge } from "lucide-react";
import toast from "react-hot-toast";
import axiosClient from "../api/axiosClient";
import StatCard from "../components/dashboard/StatCard";
import TrendChart from "../components/dashboard/TrendChart";
import DefectPieChart from "../components/dashboard/DefectPieChart";
import Loader from "../components/common/Loader";

const DEFAULT_STATS = {
  total_inspections: 0,
  defective_count: 0,
  non_defective_count: 0,
  accuracy_rate: 0,
  avg_confidence: 0,
};

export default function Dashboard() {
  const [stats, setStats] = useState(DEFAULT_STATS);
  const [trend, setTrend] = useState([]);
  const [defectFreq, setDefectFreq] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        // Fetch each independently so one failure doesn't break the whole page
        const statsRes = await axiosClient.get("/analytics/dashboard").catch(() => null);
        const trendRes = await axiosClient.get("/analytics/trend?days=14").catch(() => null);
        const freqRes  = await axiosClient.get("/analytics/defect-frequency").catch(() => null);

        if (statsRes) setStats(statsRes.data);
        if (trendRes) setTrend(trendRes.data);
        if (freqRes)  setDefectFreq(freqRes.data);

        if (!statsRes && !trendRes && !freqRes) {
          toast.error("Failed to load dashboard data");
        }
      } catch (err) {
        toast.error("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  if (loading) return <Loader fullScreen />;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={ClipboardList}
          label="Total Inspections"
          value={stats.total_inspections}
          accent="primary"
        />
        <StatCard
          icon={AlertTriangle}
          label="Defective Products"
          value={stats.defective_count}
          accent="danger"
        />
        <StatCard
          icon={CheckCircle2}
          label="Non-Defective Products"
          value={stats.non_defective_count}
          accent="success"
        />
        <StatCard
          icon={Gauge}
          label="Quality Rate"
          value={`${stats.accuracy_rate}%`}
          accent="primary"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TrendChart data={trend} />
        <DefectPieChart data={defectFreq} />
      </div>
    </div>
  );
}