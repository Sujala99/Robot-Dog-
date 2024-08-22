import numpy as np
import cv2

def sigmoid(x):
    return 1. / (1 + np.exp(-x))

def tanh(x):
    return 2. / (1 + np.exp(-2 * x)) - 1

def preprocess(src_img, size):
    output = cv2.resize(src_img, (size[0], size[1]), interpolation=cv2.INTER_AREA)
    output = output.transpose(2, 0, 1)
    output = output.reshape((1, 3, size[1], size[0])) / 255
    return output.astype('float32')

def nms(dets, thresh=0.45):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]
    output = []
    for i in keep:
        output.append(dets[i].tolist())
    return output

def detect_objects(session, img, input_width=352, input_height=352, thresh=0.65):
    try:
        pred = []
        H, W, _ = img.shape
        data = preprocess(img, [input_width, input_height])
        input_name = session.get_inputs()[0].name
        feature_map = session.run([], {input_name: data})[0][0]
        feature_map = feature_map.transpose(1, 2, 0)
        feature_map_height = feature_map.shape[0]
        feature_map_width = feature_map.shape[1]
        for h in range(feature_map_height):
            for w in range(feature_map_width):
                data = feature_map[h][w]
                obj_score, cls_score = data[0], data[5:].max()
                score = (obj_score ** 0.6) * (cls_score ** 0.4)
                if score > thresh:
                    cls_index = np.argmax(data[5:])
                    x_offset, y_offset = tanh(data[1]), tanh(data[2])
                    box_width, box_height = sigmoid(data[3]), sigmoid(data[4])
                    box_cx = (w + x_offset) / feature_map_width
                    box_cy = (h + y_offset) / feature_map_height
                    x1, y1 = box_cx - 0.5 * box_width, box_cy - 0.5 * box_height
                    x2, y2 = box_cx + 0.5 * box_width, box_cy + 0.5 * box_height
                    x1, y1, x2, y2 = int(x1 * W), int(y1 * H), int(x2 * W), int(y2 * H)
                    pred.append([x1, y1, x2, y2, score, cls_index])
        return nms(np.array(pred))
    except:
        return None
