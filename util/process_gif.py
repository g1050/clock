from PIL import Image
import numpy as np
import cv2

class ImageProcessor:
    def __init__(self, input_image_path, output_folder, target_size=(240, 240)):
        self.input_image_path = input_image_path
        self.output_folder = output_folder
        self.target_size = target_size

    def process_gif(self):
        image = Image.open(self.input_image_path)
        
        try:
            while True:
                current_frame_number = image.tell()
                frame_data = np.array(image.convert("RGB"))

                self.save_frame_to_txt(current_frame_number, frame_data)

                image.seek(current_frame_number + 1)
        except EOFError:
            pass

    def save_frame_to_txt(self, frame_number, frame_data):
        file_path = f"{self.output_folder}/frame_{frame_number}.txt"
        imgout = self.process_image(frame_data)

        with open(file_path, "w") as f:
            for i in range(self.target_size[0]):
                for j in range(self.target_size[1]):
                    f.write(hex(imgout[i, j]) + ',')

    def process_image(self, image):
        rows, cols, _ = image.shape

        scale_factor = min(self.target_size[0] / rows, self.target_size[1] / cols)

        new_rows = int(rows * scale_factor)
        new_cols = int(cols * scale_factor)

        im_resized = cv2.resize(image, (new_cols, new_rows))

        black_background = np.zeros((self.target_size[0], self.target_size[1], 3), dtype=np.uint8)

        start_row = (self.target_size[0] - new_rows) // 2
        start_col = (self.target_size[1] - new_cols) // 2

        black_background[start_row:start_row + new_rows, start_col:start_col + new_cols] = im_resized

        imgout = self.rgb565_conversion(black_background)

        return imgout

    @staticmethod
    def rgb565_conversion(image):
        b = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint32)
        g = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint32)
        r = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint32)
        imgout = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint32)

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                b[i, j] = image[i, j, 0]
                g[i, j] = image[i, j, 1]
                r[i, j] = image[i, j, 2]

        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                red = np.right_shift(r[i, j], 3)
                red = np.left_shift(red, 11)
                green = np.right_shift(g[i, j], 2)
                green = np.left_shift(green, 5)
                blue = np.right_shift(b[i, j], 3)
                imgout[i, j] = red + green + blue

        return imgout

# 使用示例
if __name__ == "__main__":
    input_gif_path = './img/loopy.gif'  # 请替换为你的 GIF 文件路径
    output_folder = './txt'  # 请替换为你想要保存帧的文件夹路径
    target_size = (240, 240)

    processor = ImageProcessor(input_image_path=input_gif_path, output_folder=output_folder)
    processor = ImageProcessor(input_image_path=input_gif_path, output_folder=output_folder, target_size=target_size)
    processor.process_gif()
