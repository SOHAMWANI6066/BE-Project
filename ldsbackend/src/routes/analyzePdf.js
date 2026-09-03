import express from "express";
import { analyzePdfFile } from "../../services/pdfService.js";

const router = express.Router();

router.post("/", async (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({
        error: "No PDF files uploaded"
      });
    }

    const documents = [];

    for (const file of req.files) {
      const result = await analyzePdfFile(file.path);

      documents.push({
        filename: file.originalname,
        analysis: result
      });
    }

    res.json({
      success: true,
      documents
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.toString()
    });
  }
});

export default router;