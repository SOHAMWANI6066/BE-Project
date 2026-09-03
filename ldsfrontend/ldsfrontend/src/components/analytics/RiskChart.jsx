import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

// Dark-theme aligned risk colors
const COLORS = [
  "#EF4444",  // High - controlled red
  "#F59E0B",  // Medium - amber
  "#10B981",  // Low - emerald
];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900/95 border border-white/10 p-3 rounded-xl shadow-2xl backdrop-blur-md">
        <p className="text-white text-xs font-semibold tracking-wide">
          {payload[0].name} Risk
        </p>
        <p className="text-indigo-400 text-lg font-bold">
          {payload[0].value} Clauses
        </p>
      </div>
    );
  }
  return null;
};

const RiskChart = ({ riskSummary }) => {
  if (!riskSummary) return null;

  const data = [
    { name: "High", value: riskSummary.high_risk_clauses },
    { name: "Medium", value: riskSummary.medium_risk_clauses },
    { name: "Low", value: riskSummary.low_risk_clauses },
  ];

  const total = data.reduce((a, b) => a + b.value, 0);

  return (
    <div className="bg-slate-900/60 border border-white/5 rounded-2xl p-6 h-[340px] flex flex-col backdrop-blur-xl shadow-[0_0_40px_rgba(99,102,241,0.05)]">
      <h3 className="text-white font-semibold tracking-tight mb-4">
        Risk Distribution
      </h3>

      <div className="flex-1 w-full relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              innerRadius={70}
              outerRadius={105}
              paddingAngle={6}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index]}
                  className="transition-all duration-300 hover:opacity-90"
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>

        {/* Center Text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-slate-500 text-xs uppercase tracking-widest">
            Total Clauses
          </span>
          <span className="text-white text-3xl font-bold">
            {total}
          </span>
        </div>
      </div>
    </div>
  );
};

export default RiskChart;