import cv2
import numpy as np
import glob
import os


# Функция для чтения изображений из директории
def read_images_from_directory(directory_path):
    images = []
    image_paths = glob.glob(os.path.join(directory_path, '*.jpg'))
    for path in image_paths:
        img = cv2.imread(path)
        if img is not None:
            images.append(img)
    return images


# Функция для изменения размера изображений до одинаковых размеров
def resize_images(images, size=(256, 256)):
    resized_images = []
    for img in images:
        resized_img = cv2.resize(img, size)
        resized_images.append(resized_img)
    return resized_images


# Функция для нормализации яркости изображений
def normalize_brightness(images):
    normalized_images = []
    for img in images:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.equalizeHist(l)
        lab = cv2.merge((l, a, b))
        normalized_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        normalized_images.append(normalized_img)
    return normalized_images


# Функция для создания мозаики
def create_mosaic(images, rows, cols):
    if len(images) < rows * cols:
        raise ValueError("Недостаточно изображений для создания мозаики указанного размера (rows * cols)")

    image_height, image_width, _ = images[0].shape
    mosaic_height = rows * image_height
    mosaic_width = cols * image_width

    mosaic = np.zeros((mosaic_height, mosaic_width, 3), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            index = i * cols + j
            if index < len(images):
                start_row = i * image_height
                start_col = j * image_width
                mosaic[start_row:start_row + image_height, start_col:start_col + image_width] = images[index]

    return mosaic


# Функция для сохранения мозаики
def save_mosaic(mosaic, output_path):
    cv2.imwrite(output_path, mosaic)


# Функция для отображения мозаики
def display_mosaic(mosaic):
    cv2.imshow('Mosaic', mosaic)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Укажите путь к директории с изображениями
    directory_path = 'path/to/your/images'

    # Чтение изображений
    images = read_images_from_directory(directory_path)

    if len(images) == 0:
        print("Не удалось найти изображения в указанной директории.")
    else:
        # Изменение размера изображений
        resized_images = resize_images(images, size=(256, 256))

        # Нормализация яркости изображений
        normalized_images = normalize_brightness(resized_images)

        rows = int(input("Введите количество строк в мозаике: "))
        cols = int(input("Введите количество столбцов в мозаике: "))

        # Создание мозаики
        try:
            mosaic = create_mosaic(normalized_images, rows, cols)

            # Сохранение мозаики
            output_path = 'path/to/save/mosaic.jpg'
            save_mosaic(mosaic, output_path)

            # Отображение мозаики
            display_mosaic(mosaic)
        except ValueError as e:
            print(e)
