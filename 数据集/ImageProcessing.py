# python ImageProcessing.py --input_dir /path/to/input --output_dir /path/to/output
import os
import cv2
import numpy as np
import argparse

def extract_person(image_path, mask_path, output_path):
    try:
        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        # 确保掩码是二维的，并且扩展到与图像相同的通道数
        if len(mask.shape) == 2:
            mask = mask[:, :, np.newaxis]
            mask = np.repeat(mask, 3, axis=2)

        # 使用 np.where 来应用掩码
        result = np.where(mask != 0, image, np.zeros_like(image))

        cv2.imwrite(output_path, result)
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def process_person(person_folder, images_lr_folder, fmask_lr_folder, output_folder):
    person_name = os.path.basename(person_folder)
    person_output_folder = os.path.join(output_folder, person_name)
    os.makedirs(person_output_folder, exist_ok=True)

    # 用于存储每个时刻的所有图片路径
    moment_images = {}

    # 遍历每个视角文件夹
    for camera_folder_name in os.listdir(images_lr_folder):
        camera_folder_path = os.path.join(images_lr_folder, camera_folder_name)
        if os.path.isdir(camera_folder_path):
            # 遍历视角文件夹中的图片
            for image_name in os.listdir(camera_folder_path):
                if image_name.endswith('.jpg') or image_name.endswith('.png'):
                    base_image_name = os.path.splitext(image_name)[0]
                    mask_name = f"{base_image_name}_fmask.png"  # 构造掩码名称

                    # 如果是第一次遇到这个基本名称，初始化列表
                    if base_image_name not in moment_images:
                        moment_images[base_image_name] = []

                    # 添加当前图片路径
                    moment_images[base_image_name].append((camera_folder_path, image_name, mask_name))

    # 为每个时刻创建新文件夹并处理图片
    folder_number = 1
    for base_image_name, images in moment_images.items():
        # 创建新的文件夹
        new_folder_name = f"{folder_number:04d}"
        new_folder_path = os.path.join(person_output_folder, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # 处理每个视角的图片
        for i, (camera_path, image_name, mask_name) in enumerate(images, start=1):
            image_path = os.path.join(camera_path, image_name)
            mask_path = os.path.join(fmask_lr_folder, os.path.relpath(camera_path, images_lr_folder), mask_name)

            # 检查掩码图像是否存在
            if not os.path.exists(mask_path):
                print(f"Mask not found for {image_path}, skipping.")
                continue

            new_image_name = f"{i}.jpg"
            output_path = os.path.join(new_folder_path, new_image_name)

            # 检查输出文件是否已存在
            if os.path.exists(output_path):
                print(f"Output file {output_path} already exists, skipping.")
                continue

            # 提取人像并保存
            extract_person(image_path, mask_path, output_path)

        folder_number += 1

        print(f"new_image_folder {new_folder_name} has finished!")

def main():
    parser = argparse.ArgumentParser(description='Process images using masks and delete originals')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing input images and masks')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output images')

    args = parser.parse_args()

    # 遍历每个人物文件夹
    for person_folder in os.listdir(args.input_dir):
        person_folder_path = os.path.join(args.input_dir, person_folder)
        images_lr_folder = os.path.join(person_folder_path, 'images_lr')
        fmask_lr_folder = os.path.join(person_folder_path, 'fmask_lr')
        if os.path.isdir(person_folder_path):
            process_person(person_folder_path, images_lr_folder, fmask_lr_folder, args.output_dir)

if __name__ == "__main__":
    main()