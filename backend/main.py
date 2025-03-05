import cv2
import numpy as np


class AdvancedLightingEstimator:
    def __init__(self):
        # More comprehensive lighting evaluation
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def estimate_lighting(self, frame):
        """
        Advanced lighting estimation with multiple analysis techniques
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        # If no face detected, analyze overall frame
        if len(faces) == 0:
            return self._analyze_overall_lighting(frame)

        # Analyze face region
        return self._analyze_face_lighting(frame, faces)

    def _analyze_overall_lighting(self, frame):
        """
        Analyze overall frame lighting when no face is detected
        """
        # Convert to LAB color space for better light analysis
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Calculate various brightness metrics
        mean_brightness = np.mean(l)
        std_brightness = np.std(l)

        # Determine lighting condition based on multiple factors
        if mean_brightness < 50:
            return "Dark", mean_brightness
        elif mean_brightness < 100:
            return "Low Light", mean_brightness
        elif mean_brightness < 150:
            return "Moderate", mean_brightness
        else:
            return "Bright", mean_brightness

    def _analyze_face_lighting(self, frame, faces):
        """
        Detailed lighting analysis for face region
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Get the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face

        # Extract face region
        face_l = l[y:y + h, x:x + w]

        # Calculate face region metrics
        mean_face_brightness = np.mean(face_l)
        std_face_brightness = np.std(face_l)

        # Advanced lighting classification
        if mean_face_brightness < 50:
            return "Poorly Lit Face", mean_face_brightness
        elif mean_face_brightness < 100:
            return "Soft Lighting", mean_face_brightness
        elif mean_face_brightness < 150:
            return "Well Lit", mean_face_brightness
        else:
            return "Bright Direct Light", mean_face_brightness

    def visualize_lighting(self, frame, lighting_condition, brightness):
        """
        Create visual feedback for lighting condition
        """
        height, width = frame.shape[:2]

        # Color mapping for different lighting conditions
        color_map = {
            "Dark": (0, 0, 100),  # Dark blue
            "Low Light": (0, 100, 200),  # Orange
            "Moderate": (0, 200, 200),  # Yellow
            "Poorly Lit Face": (0, 0, 255),  # Red
            "Soft Lighting": (100, 200, 0),  # Light green
            "Well Lit": (0, 255, 0),  # Bright green
            "Bright": (255, 0, 0),  # Blue
            "Bright Direct Light": (255, 255, 0)  # Cyan
        }

        # Lighting progress bar
        lighting_progress = min(brightness / 255.0, 1.0)
        bar_color = color_map.get(lighting_condition, (128, 128, 128))

        # Draw progress bar
        cv2.rectangle(frame, (50, height - 100),
                      (50 + int(lighting_progress * 200), height - 80),
                      bar_color, -1)

        # Add text
        cv2.putText(frame,
                    f"Lighting: {lighting_condition} ({brightness:.2f})",
                    (50, height - 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)

        return frame

    def run_estimation(self):
        """
        Main estimation and visualization loop
        """
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Estimate lighting
            lighting_condition, brightness = self.estimate_lighting(frame)

            # Visualize lighting
            frame = self.visualize_lighting(frame, lighting_condition, brightness)

            # Display frame
            cv2.imshow("Advanced Lighting Estimation", frame)

            # Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def main():
    estimator = AdvancedLightingEstimator()
    estimator.run_estimation()


if __name__ == "__main__":
    main()