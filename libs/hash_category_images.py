import os
import hashlib
import time

def hashed_upload_path(instance, filename):
    # استخراج پسوند فایل (jpg, png و غیره)
    extension = os.path.splitext(filename)[1]
    
    # تولید هش از زمان فعلی و عنوان دسته بندی
    hash_input = f"{instance.title}-{time.time()}"
    hashed_filename = hashlib.sha256(hash_input.encode()).hexdigest()
    
    # بازگرداندن مسیر ذخیره فایل با نام هش‌شده
    return f'category_images/{hashed_filename}{extension}'