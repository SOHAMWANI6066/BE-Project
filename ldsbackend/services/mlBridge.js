import fetch from "node-fetch";

/* --------------------------------------------------
   CONFIG
-------------------------------------------------- */

const ML_SERVER_URL = "http://127.0.0.1:8001/analyze/batch";
const REQUEST_TIMEOUT_MS = 60000; // 60 seconds
const MAX_RETRIES = 1;

/* --------------------------------------------------
   SAFE FETCH WITH TIMEOUT
-------------------------------------------------- */

const fetchWithTimeout = async (url, options, timeoutMs) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal,
        });
        return response;
    } finally {
        clearTimeout(timeout);
    }
};

/* --------------------------------------------------
   MAIN ML CALL
-------------------------------------------------- */

export const analyzeBatchClauses = async (clauses) => {
    let attempt = 0;

    while (attempt <= MAX_RETRIES) {
        try {
            console.log(`🚀 ML Batch Request (Attempt ${attempt + 1})`);

            const response = await fetchWithTimeout(
                ML_SERVER_URL,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ clauses }),
                },
                REQUEST_TIMEOUT_MS,
            );

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`ML Server Error: ${text}`);
            }

            const data = await response.json();

            if (!data || !Array.isArray(data.results)) {
                throw new Error("Invalid ML response structure");
            }

            return data.results;
        } catch (error) {
            console.error("ML Bridge Error:", error.message);

            if (attempt === MAX_RETRIES) {
                throw error;
            }

            console.log("Retrying ML request...");
            attempt++;
        }
    }
};
