import express from "express";
import { analyzeBatchClauses } from "../../services/mlBridge.js";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    const { clause } = req.body;

    if (!clause) {
      return res.status(400).json({
        error: "Clause text is required",
      });
    }

    const result = await analyzeBatchClauses(clause);

    res.json({
      success: true,
      data: result,
    });

  } catch (error) {
    console.error("ML Error:", error);

    res.status(500).json({
      success: false,
      error: "ML processing failed",
    });
  }
});

export default router;