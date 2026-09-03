import React from "react";

const RiskSummary = ({ riskSummary }) => {
  if (!riskSummary) return null;

  const {
    high_risk_clauses,
    medium_risk_clauses,
    low_risk_clauses,
    total_risk_score,
    document_risk_level,
  } = riskSummary;

  const stats = [
    {
      label: "High Risk",
      value: high_risk_clauses,
      color: "text-red-400",
      bg: "bg-red-500/10",
      border: "border-red-500/20",
    },
    {
      label: "Medium Risk",
      value: medium_risk_clauses,
      color: "text-amber-400",
      bg: "bg-amber-500/10",
      border: "border-amber-500/20",
    },
    {
      label: "Low Risk",
      value: low_risk_clauses,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10",
      border: "border-emerald-500/20",
    },
  ];

  return (
    <div className="bg-slate-900/60 border border-white/5 rounded-2xl p-6 backdrop-blur-xl shadow-[0_0_40px_rgba(99,102,241,0.05)]">

      <div className="flex justify-between items-center mb-8">
        <h3 className="text-white font-semibold tracking-tight">
          Document Risk Analysis
        </h3>

        <div className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20">
          <span className="text-xs text-indigo-400 font-semibold tracking-wide uppercase">
            Live Score
          </span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className={`${stat.bg} ${stat.border} border rounded-xl p-5 transition-all duration-300 hover:scale-[1.03]`}
          >
            <p className={`text-3xl font-bold ${stat.color}`}>
              {stat.value}
            </p>
            <p className="text-xs font-semibold text-slate-500 uppercase mt-2 tracking-wider">
              {stat.label}
            </p>
          </div>
        ))}
      </div>

      <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-between">
        <div>
          <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">
            Total Risk Score
          </p>
          <p className="text-2xl font-bold text-white">
            {total_risk_score}
          </p>
        </div>

        <div
          className={`px-4 py-2 rounded-lg font-semibold text-xs uppercase tracking-wide border ${
            document_risk_level === "High"
              ? "bg-red-500/15 text-red-400 border-red-500/25"
              : document_risk_level === "Medium"
              ? "bg-amber-500/15 text-amber-400 border-amber-500/25"
              : "bg-emerald-500/15 text-emerald-400 border-emerald-500/25"
          }`}
        >
          {document_risk_level} Risk
        </div>
      </div>
    </div>
  );
};

export default RiskSummary;