import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900/95 border border-white/10 p-4 rounded-xl shadow-2xl backdrop-blur-md">
        <p className="text-slate-400 text-[10px] font-semibold uppercase tracking-widest mb-1">
          {label}
        </p>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-indigo-500" />
          <p className="text-white font-bold text-lg">
            {payload[0].value}
            <span className="text-sm font-normal text-slate-500 ml-1">
              Clauses
            </span>
          </p>
        </div>
      </div>
    );
  }
  return null;
};

const ClauseTypeChart = ({ clauses }) => {
  if (!clauses) return null;

  const counts = {};
  clauses.forEach((clause) => {
    counts[clause.clause_type] =
      (counts[clause.clause_type] || 0) + 1;
  });

  const data = Object.keys(counts)
    .map((key) => ({
      type: key,
      count: counts[key],
    }))
    .sort((a, b) => b.count - a.count);

  return (
    <div className="bg-slate-900/60 border border-white/5 rounded-2xl p-6 h-[420px] backdrop-blur-xl shadow-[0_0_40px_rgba(99,102,241,0.05)] relative overflow-hidden">

      {/* Soft indigo glow */}
      <div className="absolute -top-20 -right-20 w-72 h-72 bg-indigo-500/5 blur-[120px] rounded-full" />

      {/* Header */}
      <div className="flex items-center justify-between mb-6 relative z-10">
        <div>
          <h3 className="text-white font-semibold tracking-tight">
            Clause Type Distribution
          </h3>
          <p className="text-slate-500 text-xs uppercase tracking-wider mt-1">
            Classification Breakdown
          </p>
        </div>

        <div className="h-9 w-9 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M3 3v18h18" />
            <path d="M18 17V9" />
            <path d="M13 17V5" />
            <path d="M8 17v-3" />
          </svg>
        </div>
      </div>

      <div className="h-[300px] relative z-10">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
          >
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#6366F1" stopOpacity={0.9} />
                <stop offset="100%" stopColor="#4F46E5" stopOpacity={0.6} />
              </linearGradient>
            </defs>

            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="rgba(255,255,255,0.02)"
            />

            <XAxis
              dataKey="type"
              axisLine={false}
              tickLine={false}
              tick={{
                fill: "#64748B",
                fontSize: 10,
                fontWeight: 500,
              }}
              interval={0}
              angle={-25}
              textAnchor="end"
              height={60}
            />

            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{
                fill: "#64748B",
                fontSize: 10,
              }}
            />

            <Tooltip
              cursor={{ fill: "rgba(99,102,241,0.05)" }}
              content={<CustomTooltip />}
            />
            <Bar
              dataKey="count"
              fill="url(#barGradient)"
              radius={[8, 8, 0, 0]}
              barSize={28}
              animationDuration={600}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ClauseTypeChart;