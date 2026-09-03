import app from "./app.js";
import { PORT } from "./config/env.js";
import cors from "cors"

app.use(cors())
app.listen(PORT, () => {
  console.log(`🚀 Backend running on http://localhost:${PORT}`);
});