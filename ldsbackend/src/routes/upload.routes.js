import express from "express";
import { uploadPDFs } from "../middleware/upload.middleware.js";
import { analyzeUploadedPDFs } from "../controllers/upload.controller.js";

const router = express.Router();

/*
   POST /api/upload/analyze
   Accepts multiple PDFs
*/
router.post("/analyze", uploadPDFs, analyzeUploadedPDFs);

export default router;