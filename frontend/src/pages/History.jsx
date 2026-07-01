/**
 * Paginated inspection history with defective-only filter,
 * detail modal, and delete functionality.
 */
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { Eye, Trash2, Filter } from "lucide-react";
import axiosClient from "../api/axiosClient";
import Loader from "../components/common/Loader";
import InspectionDetailModal from "../components/history/InspectionDetailModal";

const PAGE_SIZE = 10;

export default function History() {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [defectiveOnly, setDefectiveOnly] = useState(false);
  const [selected, setSelected] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await axiosClient.get("/history/", {
        params: { skip: page * PAGE_SIZE, limit: PAGE_SIZE, defective_only: defectiveOnly },
      });
      setInspections(res.data);
    } catch (err) {
      toast.error("Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [page, defectiveOnly]);

  const handleDelete = async (id) => {
    try {
      await axiosClient.delete(`/history/${id}`);
      toast.success("Inspection deleted");
      fetchHistory();
    } catch (err) {
      toast.error("Failed to delete inspection");
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-lg">Inspection History</h3>
        <button
          onClick={() => { setPage(0); setDefectiveOnly((d) => !d); }}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium border transition ${
            defectiveOnly
              ? "bg-danger-500 text-white border-danger-500"
              : "border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300"
          }`}
        >
          <Filter size={14} /> Defective Only
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
        {loading ? (
          <Loader />
        ) : inspections.length === 0 ? (
          <p className="text-center text-gray-400 text-sm py-12">No inspections found</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="bg-gray-50 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400">
              <tr>
                <th className="text-left px-5 py-3 font-medium">ID</th>
                <th className="text-left px-5 py-3 font-medium">Source</th>
                <th className="text-left px-5 py-3 font-medium">Status</th>
                <th className="text-left px-5 py-3 font-medium">Defects</th>
                <th className="text-left px-5 py-3 font-medium">Confidence</th>
                <th className="text-left px-5 py-3 font-medium">Date</th>
                <th className="text-right px-5 py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {inspections.map((insp) => (
                <tr key={insp.id} className="border-t border-gray-100 dark:border-gray-700">
                  <td className="px-5 py-3">#{insp.id}</td>
                  <td className="px-5 py-3 capitalize">{insp.source_type}</td>
                  <td className="px-5 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      insp.is_defective
                        ? "bg-red-50 text-danger-600 dark:bg-red-900/20"
                        : "bg-green-50 text-success-600 dark:bg-green-900/20"
                    }`}>
                      {insp.is_defective ? "Defective" : "Pass"}
                    </span>
                  </td>
                  <td className="px-5 py-3">{insp.defect_count}</td>
                  <td className="px-5 py-3">{(insp.avg_confidence * 100).toFixed(1)}%</td>
                  <td className="px-5 py-3 text-gray-500">{new Date(insp.created_at).toLocaleDateString()}</td>
                  <td className="px-5 py-3 text-right space-x-2">
                    <button onClick={() => setSelected(insp)} className="text-primary-600 hover:text-primary-700">
                      <Eye size={16} />
                    </button>
                    <button onClick={() => handleDelete(insp.id)} className="text-danger-500 hover:text-danger-600">
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="flex justify-end gap-2">
        <button
          disabled={page === 0}
          onClick={() => setPage((p) => p - 1)}
          className="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-40"
        >
          Previous
        </button>
        <button
          disabled={inspections.length < PAGE_SIZE}
          onClick={() => setPage((p) => p + 1)}
          className="px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 disabled:opacity-40"
        >
          Next
        </button>
      </div>

      {selected && <InspectionDetailModal inspection={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
