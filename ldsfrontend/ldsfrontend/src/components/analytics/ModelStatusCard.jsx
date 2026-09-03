import React, { useEffect, useState } from "react";
import {
    FiActivity,
    FiCpu,
    FiLayers,
    FiCheckCircle,
    FiZap,
} from "react-icons/fi";
import { getHealthStatus } from "../../services/api";

const StatusItem = ({ label, status, icon: Icon }) => {
    const isOnline =
        status === "online" || status === "active" || status.includes("v1.1");
    const isNeutral = status === "checking";

    return (
        <div className="flex items-center justify-between py-5 border-b border-white/[0.03] last:border-none group/item">
            <div className="flex items-center gap-4">
                <div
                    className={`p-2.5 rounded-xl bg-white/[0.03] border border-white/5 transition-colors duration-300 group-hover/item:border-indigo-500/30 group-hover/item:bg-indigo-500/5`}
                >
                    {Icon && (
                        <Icon
                            className="text-slate-500 group-hover/item:text-indigo-400"
                            size={18}
                        />
                    )}
                </div>
                <span className="text-slate-300 text-sm font-semibold tracking-tight group-hover/item:text-white transition-colors">
                    {label}
                </span>
            </div>

            <span
                className={`px-3 py-1 text-[9px] uppercase tracking-[0.15em] font-black rounded-full border transition-all duration-500 ${
                    isOnline
                        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.1)]"
                        : isNeutral
                          ? "bg-slate-800 text-slate-400 border-slate-700"
                          : "bg-red-500/10 text-red-400 border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]"
                }`}
            >
                {status}
            </span>
        </div>
    );
};

const ModelStatusCard = () => {
    const [backendStatus, setBackendStatus] = useState("checking");
    const [mlStatus, setMlStatus] = useState("checking");
    const [latency, setLatency] = useState(null);

    const checkHealth = async () => {
        const start = performance.now();
        try {
            const data = await getHealthStatus();
            const end = performance.now();
            setBackendStatus(data.backend || "offline");
            setMlStatus(data.ml_server || "offline");
            setLatency(((end - start) / 1000).toFixed(2));
        } catch (err) {
            setBackendStatus("offline");
            setMlStatus("offline");
            setLatency(null);
        }
    };

    useEffect(() => {
        checkHealth();
        const interval = setInterval(checkHealth, 5000);
        return () => clearInterval(interval);
    }, []);

    const isSystemLive = backendStatus === "online" && mlStatus === "online";

    return (
        <div className="w-full h-full group">
            <div className="relative h-full bg-[#0B0F1A]/80 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-10 overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex flex-col">
                {/* Visual Glow Layer */}
                <div
                    className={`absolute -bottom-24 -left-24 w-64 h-64 blur-[100px] rounded-full transition-all duration-1000 ${isSystemLive ? "bg-emerald-500/5 group-hover:bg-emerald-500/10" : "bg-red-500/5"}`}
                />

                <div className="relative z-10">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-10">
                        <div className="space-y-1">
                            <div className="flex items-center gap-2 text-indigo-500 font-black text-[10px] uppercase tracking-[0.3em] mb-1">
                                <FiZap size={12} />
                                Core Infrastructure
                            </div>
                            <h2 className="text-3xl font-black text-white tracking-tight">
                                System Status
                            </h2>
                        </div>

                        <div
                            className={`flex items-center gap-2 px-4 py-2 rounded-2xl border font-black text-[10px] uppercase tracking-widest transition-all duration-500 ${
                                isSystemLive
                                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_20px_rgba(16,185,129,0.2)]"
                                    : "bg-red-500/10 text-red-400 border-red-500/20"
                            }`}
                        >
                            <span
                                className={`w-2 h-2 rounded-full ${isSystemLive ? "bg-emerald-500 animate-pulse shadow-[0_0_8px_#10b981]" : "bg-red-500"}`}
                            />
                            {isSystemLive ? "Engine Live" : "Offline"}
                        </div>
                    </div>

                    {/* Infrastructure Items */}
                    <div className="space-y-1 mb-10">
                        <StatusItem
                            label="Backend API"
                            status={backendStatus}
                            icon={FiLayers}
                        />
                        <StatusItem
                            label="Classification Model"
                            status={mlStatus}
                            icon={FiCpu}
                        />
                        <StatusItem
                            label="Hybrid Controller"
                            status={isSystemLive ? "active" : "offline"}
                            icon={FiActivity}
                        />
                        <StatusItem
                            label="CUAD Dataset"
                            status="v1.1 (33 Labels)"
                            icon={FiCheckCircle}
                        />
                    </div>
                </div>

                {/* Metrics Section - Pushed to the bottom */}
                <div className="mt-auto relative z-10">
                    <div className="p-6 rounded-[2rem] bg-white/[0.02] border border-white/5 ring-1 ring-inset ring-white/5">
                        <p className="text-[10px] text-slate-500 mb-5 uppercase tracking-[0.3em] font-black">
                            Telemetry Metrics
                        </p>

                        <div className="grid grid-cols-2 gap-8">
                            <div className="space-y-1">
                                <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">
                                    Response Latency
                                </p>
                                <p className="text-3xl font-black text-indigo-400 tracking-tighter">
                                    {latency ? `~${latency}s` : "--"}
                                </p>
                            </div>

                            <div className="border-l border-white/5 pl-8 space-y-1">
                                <p className="text-[10px] text-slate-400 uppercase font-bold tracking-widest">
                                    Build Version
                                </p>
                                <p className="text-3xl font-black text-white tracking-tighter">
                                    v1.0.4
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModelStatusCard;
