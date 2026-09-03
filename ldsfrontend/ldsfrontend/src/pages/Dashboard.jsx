import { useState, useMemo } from "react";
import UploadCard from "../components/upload/UploadCard";
import ModelStatusCard from "../components/analytics/ModelStatusCard";
import RiskSummary from "../components/analytics/RiskSummary";
import RiskChart from "../components/analytics/RiskChart";
import ClauseTypeChart from "../components/analytics/ClauseTypeChart";
import ClauseList from "../components/clauses/ClauseList";

const Dashboard = () => {
    const [analysisData, setAnalysisData] = useState(null);

    // 🔥 Aggregate multiple PDFs into one unified view
    const aggregatedData = useMemo(() => {
        if (!analysisData?.data) return null;

        let totalHigh = 0;
        let totalMedium = 0;
        let totalLow = 0;
        let totalScore = 0;
        let totalClauses = 0;

        let allClauses = [];

        analysisData.data.forEach((file) => {
            const analysis = file.analysis;
            if (!analysis) return;

            const summary = analysis.risk_summary;

            totalHigh += summary.high_risk_clauses;
            totalMedium += summary.medium_risk_clauses;
            totalLow += summary.low_risk_clauses;
            totalScore += summary.total_risk_score;
            totalClauses += analysis.total_clauses;

            allClauses = [...allClauses, ...analysis.clauses];
        });

        if (totalClauses === 0) return null;

        const avgScore = totalScore / totalClauses;

        let documentRiskLevel = "Low";
        if (avgScore >= 2.5) {
            documentRiskLevel = "High";
        } else if (avgScore >= 1.75) {
            documentRiskLevel = "Medium";
        }

        return {
            riskSummary: {
                high_risk_clauses: totalHigh,
                medium_risk_clauses: totalMedium,
                low_risk_clauses: totalLow,
                total_risk_score: totalScore,
                average_risk_score: Number(avgScore.toFixed(2)),
                document_risk_level: documentRiskLevel,
            },
            clauses: allClauses,
        };
    }, [analysisData]);

    return (
        <div className="space-y-10">
            <h2 className="text-2xl font-bold text-white">System Overview</h2>

            {/* Upload + Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <UploadCard onAnalysisComplete={setAnalysisData} />
                <ModelStatusCard />
            </div>

            {/* Aggregated Analytics */}
            {aggregatedData && (
                <>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <RiskSummary riskSummary={aggregatedData.riskSummary} />
                        <RiskChart riskSummary={aggregatedData.riskSummary} />
                    </div>

                    <ClauseTypeChart clauses={aggregatedData.clauses} />

                    {/* 🔥 Clause Risk Breakdown Section */}
                    <ClauseList clauses={aggregatedData.clauses} />
                </>
            )}
        </div>
    );
};

export default Dashboard;
