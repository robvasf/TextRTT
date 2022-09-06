import cv2 as cv
import numpy as np
from scipy.ndimage import interpolation as inter


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist_v = np.sum(data, axis=1)
    hist_h = np.sum(data, axis=0)
    score_v = np.sum((hist_v[1:] - hist_v[:-1]) ** 2)
    return score_v, hist_v, hist_h


def rotated(img, real_img):
    delta, limit = 0.5, 60
    angles = np.arange(-limit, limit + delta, delta)
    ht, wd = img.shape[:2]
    ht1, wd1 = real_img.shape[:2]
    pix = np.array(img)
    bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)
    
    scores = []
    h_hists = []
    v_hists = []
    for angle in angles:
        score = find_score(bin_img, angle)
        scores.append(score[0])
        h_hists.append(score[1])
        v_hists.append(score[2])
    
    score_index = scores.index(max(scores))
    h_hist_list = h_hists[score_index].tolist()
    v_hist_list = v_hists[score_index].tolist()
    
    # Hor
    for i in range(len(h_hist_list)-1):
        h_dif = abs(h_hist_list[i+1]-h_hist_list[i])
        if 0.6 < h_dif:
            h_ri = (i+1)*10
            break
    
    h_hist_list_reversed = list(reversed(h_hist_list))
    for i in range(len(h_hist_list_reversed)-1):
        h_dif_reversed = abs(h_hist_list_reversed[i+1]-h_hist_list_reversed[i])
        if 0.6 < h_dif_reversed:
            h_rf = (len(h_hist_list)-i+1)*10
            break
    
    # Ver
    for i in range(len(v_hist_list)-1):
        h_dif = abs(v_hist_list[i+1]-v_hist_list[i])
        if 0.6 < h_dif:
            v_ri = (i+1)*10
            break
    
    v_hist_list_reversed = list(reversed(v_hist_list))
    for i in range(len(v_hist_list_reversed)-1):
        v_dif_reversed = abs(v_hist_list_reversed[i+1]-v_hist_list_reversed[i])
        if 0.6 < v_dif_reversed:
            v_rf = (len(v_hist_list)-i+1)*10
            break

    best_angle = angles[scores.index(max(scores))]
    img_matrix = cv.getRotationMatrix2D((wd1/2, ht1/2), best_angle, 1)
    img_skewed = cv.warpAffine(real_img, img_matrix, (wd1, ht1), borderMode=cv.BORDER_TRANSPARENT)

    return img_skewed, h_ri, h_rf, v_ri, v_rf
