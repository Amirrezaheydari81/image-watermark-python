from PIL import Image
import os

def process_images(input_folder, output_folder, square_watermark, rectangle_watermark):
    # اطمینان از وجود پوشه خروجی
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # پردازش تمامی تصاویر در پوشه ورودی
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
            image_path = os.path.join(input_folder, filename)

            # تبدیل فایل WEBP به JPG
            if filename.endswith(".webp"):
                img = Image.open(image_path).convert("RGB")
                new_filename = filename.replace(".webp", ".jpg")
                image_path = os.path.join(input_folder, new_filename)
                img.save(image_path, "JPEG")
                print(f"تصویر تبدیل شد: {new_filename}")

            # باز کردن تصویر
            img = Image.open(image_path).convert("RGBA")

            # بررسی نسبت ابعاد تصویر
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            if 0.9 <= aspect_ratio <= 1.1:  # نزدیک به مربع
                watermark_path = square_watermark
                target_size = min(img_width, img_height)  # مربع کراپ
                img = crop_to_square(img, target_size)
            else:  # نزدیک به مستطیل
                watermark_path = rectangle_watermark

            # اضافه کردن واترمارک
            watermark = Image.open(watermark_path).convert("RGBA")
            watermark = resize_watermark(watermark, img.size)
            img = add_watermark(img, watermark)

            # ذخیره تصویر نهایی
            output_path = os.path.join(output_folder, filename.replace(".webp", ".jpg"))
            img.convert("RGB").save(output_path, "JPEG")
            print(f"Save Photo: {output_path}")

def crop_to_square(img, target_size):
    """برش تصویر به مربع"""
    img_width, img_height = img.size
    left = (img_width - target_size) // 2
    top = (img_height - target_size) // 2
    right = left + target_size
    bottom = top + target_size
    return img.crop((left, top, right, bottom))

def resize_watermark(watermark, target_size):
    """تغییر اندازه واترمارک به اندازه بوم تصویر اصلی"""
    return watermark.resize(target_size, Image.Resampling.LANCZOS)

def add_watermark(img, watermark):
    """اضافه کردن واترمارک به تصویر"""
    img.paste(watermark, (0, 0), watermark)  # واترمارک در کل بوم
    return img

# مسیرها و پارامترها
input_folder = "./input_images"  # پوشه تصاویر ورودی
output_folder = "./output_images"  # پوشه تصاویر خروجی
square_watermark = "./watermark/1-1.png"  # مسیر واترمارک مربعی
rectangle_watermark = "./watermark/9-16.png"  # مسیر واترمارک مستطیلی

# اجرای تابع
process_images(input_folder, output_folder, square_watermark, rectangle_watermark)
