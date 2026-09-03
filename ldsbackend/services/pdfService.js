import fs from "fs";
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf.mjs";
import { analyzeBatchClauses } from "./mlBridge.js";

/* --------------------------------------------------
   GLOBAL ML QUEUE LOCK (CRITICAL FIX)
   Ensures ML requests never run in parallel
-------------------------------------------------- */

let mlProcessingLock = Promise.resolve();

/* --------------------------------------------------
   LEGAL KEYWORD FILTERING
-------------------------------------------------- */

const LEGAL_KEYWORDS = [
    "shall",
    "may",
    "must",
    "agree",
    "agrees",
    "liable",
    "indemnify",
    "terminate",
    "termination",
    "pay",
    "governed",
    "license",
    "rights",
    "obligation",
];

const isValidClause = (text) => {
    if (!text) return false;

    const words = text.trim().split(/\s+/);
    if (words.length < 6) return false;
    if (text === text.toUpperCase()) return false;

    const lower = text.toLowerCase();
    return LEGAL_KEYWORDS.some((keyword) => lower.includes(keyword));
};

/* --------------------------------------------------
   SAFE BATCHING CONFIG
-------------------------------------------------- */

const MAX_CLAUSES_PER_BATCH = 5;

/* --------------------------------------------------
   MAIN ANALYSIS FUNCTION
-------------------------------------------------- */

export const analyzePdfFile = async (filePath) => {
    try {
        const data = new Uint8Array(fs.readFileSync(filePath));
        const pdf = await pdfjsLib.getDocument({ data }).promise;

        let fullText = "";

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            const strings = content.items.map((item) => item.str);
            fullText += strings.join(" ") + " ";
        }

        if (!fullText || fullText.length === 0) {
            throw new Error("Empty PDF text");
        }

        /* --------------------------------------------------
       NORMALIZATION
    -------------------------------------------------- */

        const normalized = fullText
            .replace(/\r/g, " ")
            .replace(/\n/g, " ")
            .replace(/\s+/g, " ")
            .trim();

        /* --------------------------------------------------
       SMART CLAUSE SPLIT
    -------------------------------------------------- */

        let rawClauses = normalized.split(/(?=\d+\.)|(?<=\.)\s+(?=[A-Z])/);
        rawClauses = rawClauses.map((c) => c.trim());

        const clauses = rawClauses.filter(isValidClause);

        if (clauses.length === 0) {
            throw new Error("No valid legal clauses detected");
        }

        console.log("Total clauses detected:", clauses.length);

        /* --------------------------------------------------
       SAFE SERIAL ML PROCESSING (QUEUE PROTECTED)
    -------------------------------------------------- */

        let analyses = [];

        for (let i = 0; i < clauses.length; i += MAX_CLAUSES_PER_BATCH) {
            const chunk = clauses.slice(i, i + MAX_CLAUSES_PER_BATCH);

            console.log(
                `Processing ML chunk ${Math.floor(i / MAX_CLAUSES_PER_BATCH) + 1}`,
            );

            // 🔥 SERIALIZE ML CALLS
            mlProcessingLock = mlProcessingLock.then(() =>
                analyzeBatchClauses(chunk),
            );

            const batchResult = await mlProcessingLock;

            if (!Array.isArray(batchResult)) {
                throw new Error("Invalid ML batch response");
            }

            analyses = analyses.concat(batchResult);
        }

        if (analyses.length !== clauses.length) {
            throw new Error("Mismatch between clauses and ML results");
        }

        /* --------------------------------------------------
       RISK SCORING SYSTEM
    -------------------------------------------------- */

        let highCount = 0;
        let mediumCount = 0;
        let lowCount = 0;
        let totalScore = 0;

        const results = clauses.map((clause, index) => {
            const analysis = analyses[index];

            if (!analysis || analysis.error) {
                return {
                    clause_number: index + 1,
                    original: clause,
                    error: "ML processing failed",
                };
            }

            const risk = analysis.risk_level;
            let score = 1;

            if (risk === "High") {
                highCount++;
                score = 3;
            } else if (risk === "Medium") {
                mediumCount++;
                score = 2;
            } else {
                lowCount++;
                score = 1;
            }

            totalScore += score;

            return {
                clause_number: index + 1,
                original: clause,
                clause_type: analysis.clause_type,
                risk_level: risk,
                simplified_text: analysis.simplified_text,
            };
        });

        const totalClauses = results.length;
        const averageScore = totalScore / totalClauses;

        let documentRiskLevel = "Low";

        if (averageScore >= 2.5) {
            documentRiskLevel = "High";
        } else if (averageScore >= 1.75) {
            documentRiskLevel = "Medium";
        }

        /* --------------------------------------------------
       FINAL STRUCTURED OUTPUT
    -------------------------------------------------- */

        return {
            total_clauses: totalClauses,
            risk_summary: {
                high_risk_clauses: highCount,
                medium_risk_clauses: mediumCount,
                low_risk_clauses: lowCount,
                total_risk_score: totalScore,
                average_risk_score: Number(averageScore.toFixed(2)),
                document_risk_level: documentRiskLevel,
            },
            clauses: results,
        };
    } catch (error) {
        console.error("PDF analysis error:", error);
        throw error;
    }
};
