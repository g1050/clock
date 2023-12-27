import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, input_image_path, output_text_file, target_size=(240, 240)):
        self.input_image_path = input_image_path
        self.output_text_file = output_text_file
        self.target_size = target_size

    def resize_and_save(self):
        # 读取原始图像
        im = cv2.imread(self.input_image_path, cv2.IMREAD_COLOR)

        # 获取原始图像的尺寸
        rows, cols, _ = im.shape

        # 计算缩放比例
        scale_factor = min(self.target_size[0] / rows, self.target_size[1] / cols)

        # 计算 resize 后的新尺寸
        new_rows = int(rows * scale_factor)
        new_cols = int(cols * scale_factor)

        # 使用 OpenCV 进行 resize
        im_resized = cv2.resize(im, (new_cols, new_rows))

        # 创建一个黑色的背景
        black_background = np.zeros((self.target_size[0], self.target_size[1], 3), dtype=np.uint8)

        # 计算填充位置
        start_row = (self.target_size[0] - new_rows) // 2
        start_col = (self.target_size[1] - new_cols) // 2

        # 将 resize 后的图像放入黑色背景的中央位置
        black_background[start_row:start_row + new_rows, start_col:start_col + new_cols] = im_resized

        # 将图像数据处理为 RGB565 格式
        imgout = self.process_image(black_background)

        # 将结果写入文件
        with open(self.output_text_file, "w") as f:
            for i in range(self.target_size[0]):
                for j in range(self.target_size[1]):
                    f.write(hex(imgout[i, j]) + ',')

    @staticmethod
    def process_image(image):
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

    @staticmethod
    def visualize_image_from_file(file_path):
        # 读取文本文件中的数据
        with open(file_path, "r") as file:
            data = file.read().split(',')[:-1]  # 最后一个元素为空字符串，所以去掉

        # 将十六进制字符串转换为整数数组
        data = [int(value, 16) for value in data]

        # 将一维数组转换为二维数组
        w = int(np.sqrt(len(data)))
        imgout = np.array(data).reshape((w, w))

        # 将 RGB565 格式还原为 8 位灰度图像
        imgout = imgout.astype(np.uint16)
        r = ((imgout >> 11) & 0x1F) << 3
        g = ((imgout >> 5) & 0x3F) << 2
        b = (imgout & 0x1F) << 3
        imgout = np.stack((b, g, r), axis=-1).astype(np.uint8)

        # 使用 OpenCV 的 imshow 展示图像
        cv2.imshow('Visualized Image', imgout)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# 使用示例

# processor = ImageProcessor(input_image_path='img/cat.jpg', output_text_file='img/file.txt', target_size=(240, 240))
# processor.resize_and_save()

# 可视化图像
ImageProcessor.visualize_image_from_file(file_path='img/file.txt')
