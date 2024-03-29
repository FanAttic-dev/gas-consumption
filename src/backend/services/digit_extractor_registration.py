from pathlib import Path
import numpy as np
from skimage.morphology import *
import cv2
from matplotlib import pyplot as plt
from PIL import Image

from services.digit_extractor import DigitExtractor


class DigitExtractorRegistration(DigitExtractor):
    TEMPLATE_PATH = Path("dataset/template/template.jpg")

    def __init__(self, csv_name: str):
        super().__init__(csv_name)
        self.img_template = DigitExtractor.img_read(
            DigitExtractorRegistration.TEMPLATE_PATH)

    def align_with_template_SIFT(self, img, debug: bool = False):
        img_template = self.img_template

        img = (img * 255).astype(np.uint8)
        img_template = (img_template * 255).astype(np.uint8)

        orb = cv2.SIFT_create()
        img_kps, img_descs = orb.detectAndCompute(img, None)
        template_kps, template_descs = orb.detectAndCompute(
            img_template, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(img_descs, template_descs, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.5 * n.distance:
                good.append([m])

        if debug:
            matched_vis = cv2.drawMatchesKnn(
                img, img_kps, img_template, template_kps, good, None,
                # flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
            )
            h, w, _ = matched_vis.shape
            matched_vis = cv2.resize(matched_vis, (1000, int(h * 1000 / w)))
            cv2.imshow("Matched keypoints", matched_vis)
            cv2.waitKey(0)

        pts_img = np.zeros((len(good), 2), dtype=np.float32)
        pts_template = np.zeros((len(good), 2), dtype=np.float32)
        for (i, m) in enumerate(good):
            m = m[0]
            pts_img[i] = img_kps[m.queryIdx].pt
            pts_template[i] = template_kps[m.queryIdx].pt

        H, mask = cv2.findHomography(
            pts_img, pts_template, method=cv2.RANSAC)
        h, w = img_template.shape[:2]
        img_aligned = cv2.warpPerspective(img, H, (w, h))

        plt.imshow(img_aligned, cmap="gray")
        plt.show()

        return img_aligned

    def align_with_template_ORB(self, img, max_features: int = 500, keep_percent: int = 20, debug: bool = False):
        img_template = self.img_template

        img = (img * 255).astype(np.uint8)
        img_template = (img_template * 255).astype(np.uint8)

        orb = cv2.ORB_create(max_features, scoreType=cv2.ORB_HARRIS_SCORE)
        img_kps, img_descs = orb.detectAndCompute(img, None)
        template_kps, template_descs = orb.detectAndCompute(
            img_template, None)

        method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
        matcher = cv2.DescriptorMatcher_create(method)
        matches = matcher.match(img_descs, template_descs, None)

        matches = sorted(matches, key=lambda x: x.distance)
        keep = int(len(matches) * keep_percent / 100)
        matches = matches[:keep]

        if debug:
            matched_vis = cv2.drawMatches(
                img, img_kps, img_template, template_kps, matches, None)
            h, w, _ = matched_vis.shape
            matched_vis = cv2.resize(matched_vis, (1000, int(h * 1000 / w)))
            cv2.imshow("Matched keypoints", matched_vis)
            cv2.waitKey(0)

        pts_img = np.zeros((len(matches), 2), dtype=np.float32)
        pts_template = np.zeros((len(matches), 2), dtype=np.float32)
        for (i, m) in enumerate(matches):
            pts_img[i] = img_kps[m.queryIdx].pt
            pts_template[i] = template_kps[m.queryIdx].pt

        H, mask = cv2.findHomography(
            pts_img, pts_template, method=cv2.RANSAC)
        h, w = img_template.shape[:2]
        img_aligned = cv2.warpPerspective(img, H, (w, h))

        plt.imshow(img_aligned, cmap="gray")
        plt.show()

        return img_aligned

    def img_preprocess(self, img_orig, show: bool):
        img = img_orig

        # self.align_with_template_ORB(img, debug=True)
        try:
            img = self.align_with_template_SIFT(img, debug=True)
        except Exception as e:
            print(e)
            img = img_orig

        return Image.fromarray(img).convert('RGB')
