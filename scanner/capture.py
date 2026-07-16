import cv2
import os


class DocumentCapture:

    def __init__(self):
        self.output_folder = "documents"

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def capture_from_camera(self):
        def __init__(self):
        self.output_folder = "documents"

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    # First method
    def capture_from_camera(self):

        camera = cv2.VideoCapture(0)

        print("Press 'S' to capture.")
        print("Press 'Q' to quit.")

        while True:

            success, frame = camera.read()

            if not success:
                break

            cv2.imshow("AI Document Scanner", frame)

            key = cv2.waitKey(1)

            if key == ord('s'):

                image_path = os.path.join(
                    self.output_folder,
                    "captured_document.jpg"
                )

                cv2.imwrite(image_path, frame)

                camera.release()
                cv2.destroyAllWindows()

                return image_path

            elif key == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()

        return None

    # Second method (write it BELOW the first one)
    def select_image(self):

        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        root = Tk()
        root.withdraw()

        file_path = askopenfilename(
            title="Select Document",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        return file_path

        camera = cv2.VideoCapture(0)

        print("Press 'S' to capture the document.")
        print("Press 'Q' to quit.")

        while True:

            success, frame = camera.read()

            if not success:
                print("Camera not found.")
                break

            cv2.imshow("AI Document Scanner", frame)

            key = cv2.waitKey(1)

            if key == ord('s'):

                image_path = os.path.join(
                    self.output_folder,
                    "captured_document.jpg"
                )

                cv2.imwrite(image_path, frame)

                print(f"Document saved to {image_path}")

                camera.release()
                cv2.destroyAllWindows()

                return image_path

            elif key == ord('q'):

                break

        camera.release()
        cv2.destroyAllWindows()

        return None