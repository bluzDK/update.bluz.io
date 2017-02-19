from unittest import TestCase

import sys
sys.path.append("..")
from update_api import *


class APITestCase(TestCase):
    """
    Test cases for the API and helper functions
    """

    def test_create_dir(self):
        dir = create_dir()
        self.assertTrue(os.path.exists(dir))

        os.rmdir(dir)

    def test_filename_from_url(self):
        urls = ["http://console.bluz.io/firmware/latest/bluz_dk/system-part1.bin", "http://console.bluz.io/firmware/latest/bluz_dk/tinker.bin",
                "http://console.bluz.io/tinker.bin", "https://console.bluz.io/wreck_it_ralph.bin"]
        names = ["system-part1.bin", "tinker.bin", "tinker.bin", "wreck_it_ralph.bin"]

        for url, name in zip(urls, names):
            self.assertEqual(name, filename_from_url(url))






