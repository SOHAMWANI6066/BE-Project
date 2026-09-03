import axios from "axios";

export const healthCheck = async (req, res) => {
  try {
    let mlStatus = "offline";

    try {
      const mlResponse = await axios.get(
        "http://127.0.0.1:8001/health",
        { timeout: 2000 }
      );

      if (mlResponse.status === 200) {
        mlStatus = "online";
      }
    } catch (mlError) {
      mlStatus = "offline";
    }

    return res.status(200).json({
      backend: "online",
      ml_server: mlStatus,
      timestamp: new Date().toISOString(),
    });

  } catch (error) {
    return res.status(500).json({
      backend: "offline",
      ml_server: "offline",
      timestamp: new Date().toISOString(),
    });
  }
};