import cv2
import numpy as np
from typing import List, Tuple
from PIL import Image

# 클래스 한글 매핑 (영어 -> 한글)
class_mapping = {
    'damaged door': '손상된 문짝',
    'damaged window': '손상된 창문',
    'damaged headlight': '손상된 헤드라이트',
    'damaged mirror': '손상된 사이드 미러',
    'dent': '덴트',
    'damaged hood': '손상된 후드',
    'damaged bumper': '손상된 범퍼',
    'damaged wind shield': '손상된 윈드쉴드'
}

# Detection 클래스 정의 (FastAPI 서버 없이 직접 실행)
class Detection:
    def __init__(self, model_path: str, classes: List[str]):
        self.model_path = model_path
        self.classes = classes
        self.model = self.__load_model()

    def __load_model(self) -> cv2.dnn_Net:
        net = cv2.dnn.readNet(self.model_path)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # CPU에서 실행
        return net

    def __extract_output(self, preds: np.ndarray, image_shape: Tuple[int, int], input_shape: Tuple[int, int],
                         score: float = 0.1, nms: float = 0.0, confidence: float = 0.0) -> dict:
        class_ids, confs, boxes = [], [], []

        image_height, image_width = image_shape
        input_height, input_width = input_shape
        x_factor = image_width / input_width
        y_factor = image_height / input_height

        rows = preds[0].shape[0]
        for i in range(rows):
            row = preds[0][i]
            conf = row[4]

            classes_score = row[4:]
            _, _, _, max_idx = cv2.minMaxLoc(classes_score)
            class_id = max_idx[1]

            if classes_score[class_id] > score:
                confs.append(conf)
                label = self.classes[int(class_id)]
                class_ids.append(label)

                # Extract boxes
                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

        r_class_ids, r_confs, r_boxes = [], [], []
        indexes = cv2.dnn.NMSBoxes(boxes, confs, confidence, nms)
        for i in indexes:
            r_class_ids.append(class_ids[i])
            r_confs.append(confs[i] * 100)
            r_boxes.append(boxes[i].tolist())

        return {'boxes': r_boxes, 'confidences': r_confs, 'classes': r_class_ids}

    def __call__(self, image: np.ndarray, width: int = 640, height: int = 640, score: float = 0.1,
                 nms: float = 0.0, confidence: float = 0.0) -> dict:
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (width, height), swapRB=True, crop=False)
        self.model.setInput(blob)
        preds = self.model.forward()
        preds = preds.transpose((0, 2, 1))

        results = self.__extract_output(preds=preds, image_shape=image.shape[:2], input_shape=(height, width),
                                        score=score, nms=nms, confidence=confidence)
        return results

# 모델 경로 및 클래스 정의 (영문)
detection = Detection(
    model_path='Resources/best.onnx',
    classes=['damaged door', 'damaged window', 'damaged headlight', 'damaged mirror', 'dent', 'damaged hood', 'damaged bumper', 'damaged wind shield']
)

def get_image_input(uploaded_file):
    # PIL로 이미지 불러오기
    image = Image.open(uploaded_file)
    image = np.array(image)

    # 객체 감지 수행
    results = detection(image)

    # 결과를 변수에 저장 (바운딩 박스, 레이블, 신뢰도 점수)
    boxes = results['boxes']
    labels = results['classes']
    confidences = results['confidences']

    # 이미지 크기 기준으로 영역 나누기 (좌측 상단, 우측 상단, 좌측 하단, 우측 하단)
    image_height, image_width = image.shape[:2]
    mid_width = image_width // 2
    mid_height = image_height // 2

    # 결과 텍스트를 저장할 리스트
    detection_results = []

    # 이미지에 감지 결과 그리기
    for box, label, confidence in zip(boxes, labels, confidences):
        x, y, w, h = box
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"{label} ({100-confidence:.2f}%)"
        cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 바운딩 박스 중심점 계산
        center_x = x + w // 2
        center_y = y + h // 2

        # 객체가 어느 영역에 속하는지 확인
        if center_x < mid_width and center_y < mid_height:
            position = "좌측 상단"
        elif center_x >= mid_width and center_y < mid_height:
            position = "우측 상단"
        elif center_x < mid_width and center_y >= mid_height:
            position = "좌측 하단"
        else:
            position = "우측 하단"

        # 영문 레이블을 한글로 변환
        korean_label = class_mapping.get(label, label)

        # 결과를 리스트에 저장
        result_text = f"{position}: {korean_label} - 신뢰도: {100-confidence:.2f}%"
        detection_results.append(result_text)


    # LLM 모델에 전달할 결과를 텍스트로 결합
    detection_text = "\n".join(detection_results)
    
    # 이제 detection_text를 LLM 모델에 전달
    # 예시: response = llm_model(detection_text)
    return detection_text,image

