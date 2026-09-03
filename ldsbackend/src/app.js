import express from "express";
import cors from "cors";
import healthRoutes from "./routes/health.routes.js";
import uploadRoutes from "./routes/upload.routes.js";
import analyzeRoutes from "./routes/analyze.js";
import analyzePdfRoutes from "./routes/analyzePdf.js"
const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/upload", uploadRoutes);
app.use("/api/health", healthRoutes);
app.use("/api/analyze", analyzeRoutes);
app.use("/api/analyze/pdf", analyzePdfRoutes);
export default app;