import { useState } from "react";
import { FiChevronDown } from "react-icons/fi";

/* --------------------------------------------------
   SECTION COMPONENT
-------------------------------------------------- */

const RiskSection = ({ title, color, clauses }) => {
    const [open, setOpen] = useState(true);

    if (!clauses.length) return null;

    return (
        <div className="space-y-6 relative">
            {/* Section Header */}
            <div
                onClick={() => setOpen(!open)}
                className={`group flex justify-between items-center cursor-pointer
        px-6 py-4 rounded-2xl bg-slate-900/60 border border-white/5
        transition-all duration-300 hover:bg-slate-900/80`}
            >
                <div className="flex items-center gap-4">
                    {/* Animated Indicator */}
                    <div
                        className={`w-2 h-8 rounded-full ${color.strip} transition-all duration-500 group-hover:scale-y-110`}
                    />

                    <div>
                        <h3 className="text-lg font-semibold text-white tracking-tight">
                            {title}
                        </h3>
                        <p className="text-xs text-slate-500 uppercase tracking-widest">
                            {clauses.length} Clauses Identified
                        </p>
                    </div>
                </div>

                <FiChevronDown
                    className={`text-slate-400 transition-transform duration-300 ${
                        open ? "rotate-180" : ""
                    }`}
                />
            </div>

            {/* Animated Grid */}
            <div
                className={`transition-all duration-500 ease-in-out overflow-hidden ${
                    open ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0"
                }`}
            >
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 pt-2">
                    {clauses.map((clause, index) => (
                        <div
                            key={clause.clause_number}
                            className="animate-fade-in"
                            style={{ animationDelay: `${index * 60}ms ` }}
                        >
                            <ClauseCard clause={clause} color={color} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

/* --------------------------------------------------
   CLAUSE CARD
-------------------------------------------------- */

const ClauseCard = ({ clause, color }) => {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className="relative group">
            {/* Soft Hover Aura */}
            <div
                className={`absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 blur-2xl transition duration-500 ${color.glow}`}
            />

            <div
                className={`relative bg-slate-900/70 backdrop-blur-xl
        border border-white/5 rounded-3xl p-7
        transition-all duration-300
        hover:border-white/10 hover:shadow-[0_15px_50px_rgba(0,0,0,0.4)]
        border-l-4 ${color.strip}`}
            >
                {/* Header */}
                <div className="flex justify-between items-start mb-5">
                    <div>
                        <p className="text-[10px] text-slate-500 uppercase tracking-[0.3em] font-semibold">
                            Clause #{clause.clause_number}
                        </p>
                        <h4 className="text-white font-semibold text-base mt-1">
                            {clause.clause_type}
                        </h4>
                    </div>

                    <span
                        className={`text-xs font-bold px-3 py-1.5 rounded-full border transition-all duration-300 ${color.badge}`}
                    >
                        {clause.risk_level}
                    </span>
                </div>

                {/* Simplified */}
                <div className="bg-white/[0.03] border border-white/5 rounded-xl p-5 transition-colors duration-300 group-hover:bg-white/[0.05]">
                    <p className="text-slate-200 text-sm leading-relaxed">
                        {clause.simplified_text}
                    </p>
                </div>

                {/* Expand Button */}
                <button
                    onClick={() => setExpanded(!expanded)}
                    className="mt-6 text-xs font-semibold text-indigo-400 hover:text-white transition-colors"
                >
                    {expanded ? "Hide Original Clause" : "View Original Clause"}
                </button>
                {/* Accordion */}
                <div
                    className={`transition-all duration-500 ease-in-out overflow-hidden ${
                        expanded
                            ? "max-h-[400px] opacity-100 mt-4"
                            : "max-h-0 opacity-0"
                    }`}
                >
                    <div className="text-xs text-slate-400 bg-black/60 border border-white/5 p-4 rounded-xl font-mono leading-relaxed shadow-inner">
                        {clause.original}
                    </div>
                </div>
            </div>
        </div>
    );
};

/* --------------------------------------------------
   MAIN LIST
-------------------------------------------------- */

const ClauseList = ({ clauses }) => {
    if (!clauses || clauses.length === 0) return null;

    const high = clauses.filter((c) => c.risk_level === "High");
    const medium = clauses.filter((c) => c.risk_level === "Medium");
    const low = clauses.filter((c) => c.risk_level === "Low");

    return (
        <div className="space-y-14">
            <div>
                <h2 className="text-2xl font-bold text-white tracking-tight">
                    Clause Risk Analysis
                </h2>
                <p className="text-sm text-slate-500 mt-2">
                    Detailed classification and simplified interpretation of
                    detected clauses.
                </p>
            </div>

            <RiskSection
                title="High Risk Clauses"
                clauses={high}
                color={{
                    strip: "border-l-red-500 bg-red-500",
                    badge: "bg-red-500/10 text-red-400 border-red-500/20",
                    glow: "bg-red-500/5",
                }}
            />

            <RiskSection
                title="Medium Risk Clauses"
                clauses={medium}
                color={{
                    strip: "border-l-amber-400",
                    badge: "bg-amber-400/10 text-amber-300 border border-amber-400/20",
                    glow: "bg-amber-400/10",
                }}
            />

            <RiskSection
                title="Low Risk Clauses"
                clauses={low}
                color={{
                    strip: "border-l-emerald-400 bg-emerald-400",
                    badge: "bg-emerald-400/10 text-emerald-400 border-emerald-400/20",
                    glow: "bg-emerald-400/5",
                }}
            />
        </div>
    );
};

export default ClauseList;
