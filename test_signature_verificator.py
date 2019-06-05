"""
    Test package
"""

import unittest
import cv2
from signature_verificator import SignatureVerificator


class TestSignatureVerificator(unittest.TestCase):
    """
        Test of SignatureVerificator class
    """

    @classmethod
    def setUpClass(cls):
        cls.s = SignatureVerificator()

    def test_tp(self):
        """
            True Positive test
        """
        H_0_IMG = cv2.imread("test_images/H_0.png", 0)
        H_1_IMG = cv2.imread("test_images/H_1.png", 0)
        I_0_IMG = cv2.imread("test_images/I_0.png", 0)
        self.assertTrue(self.s.verify(H_0_IMG, H_0_IMG) > 0.8)
        self.assertTrue(self.s.verify(H_1_IMG, H_1_IMG) > 0.8)
        self.assertTrue(self.s.verify(H_0_IMG, H_1_IMG) > 0.8)
        self.assertTrue(self.s.verify(I_0_IMG, I_0_IMG) > 0.8)

    def test_tn(self):
        """
            True Negative test
        """
        H_0_IMG = cv2.imread("test_images/H_0.png", 0)
        H_1_IMG = cv2.imread("test_images/H_1.png", 0)
        I_0_IMG = cv2.imread("test_images/I_0.png", 0)
        self.assertTrue(self.s.verify(H_0_IMG, I_0_IMG) < 0.2)
        self.assertTrue(self.s.verify(H_1_IMG, I_0_IMG) < 0.2)

    def test_preprocess(self):
        """
            Preprocess test
        """
        C_0_IMG = cv2.imread("test_images/C_0.png", 0)
        C_1_IMG = cv2.imread("test_images/C_1.png", 0)
        self.assertTrue(self.s.verify(C_0_IMG, C_1_IMG) > 0.8)
