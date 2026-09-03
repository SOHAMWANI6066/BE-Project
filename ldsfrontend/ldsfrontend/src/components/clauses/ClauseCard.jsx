import React, { useState } from "react";
import {
    FiChevronDown,
    FiShield,
    FiAlertOctagon,
    FiInfo,
    FiExternalLink,
    FiTerminal,
} from "react-icons/fi";

const ClauseCard = ({ clause }) => {
    const [expanded, setExpanded] = useState(false);

    const getRiskConfig = (risk) => {
        switch (risk) {
            case "High":
                return {
                    icon: <FiAlertOctagon size={16} />,
                    label: "High Risk",
                    badge: "bg-red-500/10 text-red-400 border-red-500/20",
                    accent: "border-l-red-500",
                };
            case "Medium":
                return {
                    icon: <FiInfo size={16} />,
                    label: "Medium Risk",
                    badge: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
                    accent: "border-l-yellow-400",
                };
            default:
                return {
                    icon: <FiShield size={16} />,
                    label: "Low Risk",
                    badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
                    accent: "border-l-emerald-400",
                };
        }
    };

    const config = getRiskConfig(clause.risk_level);

    return (
        <div className="relative group">
            {/* Hover Soft Glow */}
            <div className="absolute inset-0 rounded-3xl bg-indigo-500/0 group-hover:bg-indigo-500/5 blur-2xl transition duration-500" />

            <div
                className={`relative bg-slate-900/60 backdrop-blur-xl border border-white/5 rounded-3xl p-7 transition-all duration-400
        hover:border-white/10 hover:shadow-[0_10px_40px_rgba(0,0,0,0.35)]
        border-l-4 ${config.accent}`}
            >
                {/* Header */}
                <div className="flex justify-between items-start mb-6">
                    <div className="flex items-center gap-4">
                        <div className="p-3 rounded-xl bg-white/[0.04] border border-white/5 text-slate-300">
                            {config.icon}
                        </div>

                        <div>
                            <p className="text-[10px] uppercase tracking-[0.3em] text-slate-500 font-semibold">
                                Clause #{clause.clause_number}
                            </p>
                            <h4 className="text-white font-semibold text-base tracking-tight mt-1">
                                {clause.clause_type}
                            </h4>
                        </div>
                    </div>

                    <div
                        className={`px-3 py-1.5 rounded-full border text-[10px] font-bold uppercase tracking-wider transition-all duration-300 ${config.badge}`}
                    >
                        {config.label}
                    </div>
                </div>

                {/* Simplified Clause */}
                <div className="bg-white/[0.03] border border-white/5 rounded-xl p-5 transition-colors duration-300 group-hover:bg-white/[0.05]">
                    <p className="text-slate-200 text-sm leading-relaxed">
                        {clause.simplified_text}
                    </p>
                </div>

                {/* Footer */}
                <div className="mt-7 flex items-center justify-between">
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className="flex items-center gap-2 text-xs font-semibold text-indigo-400 hover:text-white transition-colors"
                    >
                        {expanded ? "Hide Original" : "View Original"}
                        <FiChevronDown
                            className={`transition-transform duration-300 ${
                                expanded ? "rotate-180" : ""
                            }`}
                        />
                    </button>

                    <button className="flex items-center gap-2 text-xs text-slate-500 hover:text-indigo-400 transition-colors">
                        Share
                        <FiExternalLink size={14} />
                    </button>
                </div>

                {/* Accordion */}
                <div
                    className={`transition-all duration-500 ease-in-out overflow-hidden ${
                        expanded
                            ? "max-h-[500px] opacity-100 mt-6"
                            : "max-h-0 opacity-0"
                    }`}
                >
                    <div className="p-6 rounded-xl bg-black/60 border border-white/5 font-mono text-xs text-slate-400 leading-relaxed shadow-inner">
                        <div className="flex items-center gap-2 mb-4 text-indigo-400/80 border-b border-white/5 pb-2">
                            <FiTerminal size={13} />
                            <span className="font-semibold uppercase tracking-widest text-[10px]">
                                Legal Verbatim Text
                            </span>
                        </div>

                        <p className="text-slate-400 whitespace-pre-line">
                            {clause.original}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ClauseCard;
