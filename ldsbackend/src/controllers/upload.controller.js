import pLimit from "p-limit";
import { analyzePdfFile } from "../../services/pdfService.js";
import { successResponse, errorResponse } from "../utils/response.js";

const MAX_PARALLEL_PDFS = 1; // Safe concurrency limit

export const analyzeUploadedPDFs = async (req, res) => {
  const startTime = Date.now();

  try {
    // ✅ Proper validation
    if (!req.files || req.files.length === 0) {
      return errorResponse(
        res,
        "No PDF files uploaded",
        "NO_FILES",
        400
      );
    }

    const limit = pLimit(MAX_PARALLEL_PDFS);

    // 🚀 Controlled parallel execution
    const tasks = req.files.map((file) =>
      limit(async () => {
        try {
          const analysis = await analyzePdfFile(file.path);

          return {
            filename: file.originalname,
            analysis
          };

        } catch (err) {
          return {
            filename: file.originalname,
            error: err?.message || "PDF processing failed"
          };
        }
      })
    );

    const results = await Promise.all(tasks);

    const processingTime = Date.now() - startTime;

    return successResponse(res, results, {
      total_files: results.length,
      processing_time_ms: processingTime,
      parallel_limit: MAX_PARALLEL_PDFS
    });

  } catch (error) {
    console.error("Upload Controller Error:", error);

    return errorResponse(
      res,
      "Unexpected server error",
      "UPLOAD_FAILURE",
      500
    );
  }
};