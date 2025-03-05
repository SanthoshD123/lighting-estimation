class LightingEstimator {
  constructor() {
    this.webcamElement = document.getElementById("webcam");
    this.canvasElement = document.getElementById("output");
    this.statusElement = document.getElementById("lighting-status");
    this.context = this.canvasElement.getContext("2d");
  }

  async setupWebcam() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      this.webcamElement.srcObject = stream;
      return new Promise((resolve) => {
        this.webcamElement.onloadedmetadata = () => {
          resolve(this.webcamElement);
        };
      });
    } catch (err) {
      console.error("Webcam Error:", err);
      this.updateStatus("Webcam Access Denied", "red");
    }
  }

  calculateLightingMetrics(imageData) {
    const data = imageData.data;
    let totalBrightness = 0;
    let brightPixels = 0;
    let darkPixels = 0;
    let varianceSum = 0;

    // Sample every pixel
    for (let i = 0; i < data.length; i += 4) {
      // Calculate pixel brightness
      const pixelBrightness = (data[i] + data[i + 1] + data[i + 2]) / 3;

      totalBrightness += pixelBrightness;

      // Count bright and dark pixels
      if (pixelBrightness > 200) brightPixels++;
      if (pixelBrightness < 50) darkPixels++;
    }

    const pixelCount = data.length / 4;
    const averageBrightness = totalBrightness / pixelCount;
    const brightnessRatio = brightPixels / pixelCount;
    const darkRatio = darkPixels / pixelCount;

    return {
      averageBrightness,
      brightnessRatio,
      darkRatio,
    };
  }

  classifyLighting(metrics) {
    const { averageBrightness, brightnessRatio, darkRatio } = metrics;

    // Comprehensive lighting classification
    if (averageBrightness < 50)
      return {
        condition: "Dark Environment",
        color: "#8B0000", // Dark Red
      };

    if (averageBrightness < 100)
      return {
        condition: "Low Ambient Light",
        color: "#FF4500", // Orange Red
      };

    if (darkRatio > 0.3)
      return {
        condition: "Uneven Lighting",
        color: "#FFA500", // Orange
      };

    if (brightnessRatio > 0.4)
      return {
        condition: "Bright Direct Light",
        color: "#00FF00", // Bright Green
      };

    if (averageBrightness > 150 && brightnessRatio < 0.2)
      return {
        condition: "Soft, Diffused Light",
        color: "#00CED1", // Dark Turquoise
      };

    return {
      condition: "Optimal Lighting",
      color: "#32CD32", // Lime Green
    };
  }

  updateStatus(message, color = "#333") {
    this.statusElement.innerHTML = message;
    this.statusElement.style.backgroundColor = color;
  }

  async startLightingEstimation() {
    // Hide canvas
    this.canvasElement.style.display = "none";

    try {
      await this.setupWebcam();

      const processFrame = () => {
        // Draw current frame to canvas
        this.context.drawImage(this.webcamElement, 0, 0, 640, 480);

        // Get image data
        const imageData = this.context.getImageData(0, 0, 640, 480);

        // Calculate lighting metrics
        const metrics = this.calculateLightingMetrics(imageData);

        // Classify lighting
        const lightingResult = this.classifyLighting(metrics);

        // Update status
        this.updateStatus(
          `Lighting: ${lightingResult.condition}<br>` +
            `Brightness: ${metrics.averageBrightness.toFixed(2)}`,
          lightingResult.color
        );

        // Continue processing frames
        requestAnimationFrame(processFrame);
      };

      // Start processing
      processFrame();
    } catch (error) {
      console.error("Lighting Estimation Error:", error);
      this.updateStatus("Estimation Failed", "red");
    }
  }
}

// Initialize and start when page loads
window.addEventListener("load", () => {
  const lightingEstimator = new LightingEstimator();
  lightingEstimator.startLightingEstimation();
});
