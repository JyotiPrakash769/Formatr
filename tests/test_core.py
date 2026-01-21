import unittest
import os
import shutil
from backend.core.image_processor import ImageProcessor
from backend.core.archive_processor import ArchiveProcessor

# Note: Testing PDF/AV/Doc requires external deps (FFmpeg, LibreOffice) which might not be present in this env.
# We will test what we can (Image, Archive).

class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a dummy image
        from PIL import Image
        self.img_path = os.path.join(self.test_dir, "test.png")
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(self.img_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_image_convert(self):
        output = ImageProcessor.convert_image(self.img_path, 'JPG', self.test_dir)
        self.assertTrue(os.path.exists(output))
        self.assertTrue(output.endswith(".jpg"))

    def test_image_resize(self):
        output = ImageProcessor.resize_image(self.img_path, width=50)
        from PIL import Image
        img = Image.open(output)
        self.assertEqual(img.size, (50, 50))

    def test_archive(self):
        zip_path = os.path.join(self.test_dir, "archive.zip")
        ArchiveProcessor.create_zip([self.img_path], zip_path)
        self.assertTrue(os.path.exists(zip_path))
        
        extract_dir = os.path.join(self.test_dir, "extracted")
        ArchiveProcessor.extract_zip(zip_path, extract_dir)
        self.assertTrue(os.path.exists(os.path.join(extract_dir, "test.png")))

if __name__ == '__main__':
    unittest.main()
