import multiprocessing
import os
import os.path as osp
import time
from glob import glob
from multiprocessing import Pool

import cv2
import image_processing
import numpy as np
from tqdm import tqdm


def random_crop(image, mask, crop_size=(224, 224)):
    """
    画像からrandom cropを作成する
    """
    h, w, _ = image.shape

    # 0~(400-224)の間で画像のtop, leftを決める
    top = np.random.randint(0, h - crop_size[0])
    left = np.random.randint(0, w - crop_size[1])

    # top, leftから画像のサイズである224を足して、bottomとrightを決める
    bottom = top + crop_size[0]
    right = left + crop_size[1]

    # 決めたtop, bottom, left, rightを使って画像を抜き出す
    image = image[top:bottom, left:right, :]
    mask = mask[top:bottom, left:right, :]

    return image, mask


def create_crop(num):
    ROOT_PATH = '/Volumes/GoogleDrive/マイドライブ/07_aoz_cloud/■会社別ファイル/'\
        'メ__メインマーク/3_研究開発/FootinBarDetection/data/'
    SAVE_PATH = '/Volumes/GoogleDrive/マイドライブ/07_aoz_cloud/■会社別ファイル/'\
        'メ__メインマーク/3_研究開発/FootinBarDetection/'\
        'crack_segmentation_dataset/crack_segmentation_dataset/'

    PHASE = 'train'

    RESIZE = 480

    IMG_ROOT = ROOT_PATH + 'img_' + PHASE + '/'
    MASK_ROOT = ROOT_PATH + 'mask_' + PHASE + '/'
    if not osp.exists(IMG_ROOT) and not osp.exists(MASK_ROOT):
        print('ROOT path no exist!!')

    # maskのの領域が5%以上を学習データとして採用する
    IMG_SAVE_PATH = SAVE_PATH + PHASE + '/images/'
    MASK_SAVE_PATH = SAVE_PATH + PHASE + '/masks/'
    if not osp.exists(IMG_SAVE_PATH) or osp.exists(MASK_SAVE_PATH):
        os.mkdir(IMG_SAVE_PATH)
        os.mkdir(MASK_SAVE_PATH)

    # img = cv2.imread(IMG_ROOT + num + '.png')
    # mask = cv2.imread(MASK_ROOT + num + '.png')

    # 元画像とマスク画像をリサイズする
    ip = image_processing.ImageProcessing(IMG_ROOT + num + '.png', RESIZE)
    img = ip.image_resize()
    print('\n', img.shape)

    ip = image_processing.ImageProcessing(MASK_ROOT + num + '.png', RESIZE)
    mask = ip.image_resize()

    print(num)
    if np.count_nonzero(mask == 255) != 0:
        count = 0
        while True:
            if count == 10:
                break
            else:
                img_crop, mask_crop = random_crop(
                    img, mask, crop_size=(RESIZE, RESIZE))
                per = np.round(np.count_nonzero(
                    mask_crop) / mask_crop.size * 100, 1)
                if 5.0 <= per:  # 大きいと無限ループ
                    count += 1
                    cv2.imwrite(IMG_SAVE_PATH + num + '_' +
                                str(count).zfill(2) + '.png', img_crop)
                    cv2.imwrite(MASK_SAVE_PATH + num + '_' +
                                str(count).zfill(2) + '.png', mask_crop)

        count = 0
        while True:
            if count == 2:
                break
            else:
                img_crop, mask_crop = random_crop(
                    img, mask, crop_size=(RESIZE, RESIZE))
                per = np.round(np.count_nonzero(
                    mask_crop) / mask_crop.size * 100, 1)
                if per <= 1.5:  # 小さいと無限ループ
                    count += 1
                    cv2.imwrite(IMG_SAVE_PATH + num + '_' +
                                str(count).zfill(2) + '_0.png', img_crop)
                    cv2.imwrite(MASK_SAVE_PATH + num + '_' +
                                str(count).zfill(2) + '_0.png', mask_crop)


if __name__ == '__main__':
    PHASE = 'train'

    TEST_FILE = glob('/Volumes/GoogleDrive/マイドライブ/07_aoz_cloud/■会社別ファイル/'
                     'メ__メインマーク/3_研究開発/FootinBarDetection/data/'
                     'img_' + PHASE + '/' + '*.png')
    TEST_ID = [osp.basename(path)[:5] for path in TEST_FILE]

    # 並列処理
    core = multiprocessing.cpu_count()
    with Pool(core - 1) as p:
        result = list(tqdm(p.imap(create_crop, TEST_ID), total=len(TEST_ID)))

