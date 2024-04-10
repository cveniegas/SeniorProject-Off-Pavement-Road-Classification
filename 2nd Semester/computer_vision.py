import argparse
import os
from typing import Dict, Iterable, List, Set, Tuple
from PySide2.QtCore import Qt ,Signal,QThread
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
import cv2
import numpy as np
from inference.models.utils import get_roboflow_model
from tqdm import tqdm
import supervision as sv
from inference import InferencePipeline
from inference.core.interfaces.camera.entities import VideoFrame
from ui_Project3 import Ui_MainWindow

COLORS = sv.ColorPalette.from_hex(["#b619e6", "#19e6d8", "#2ee619", "#e69419"])

classes = ["Bicyclist",
            "Bus",
            "Car",
            "Commercial-Vehicle", "Emergency-Vehicle",
            "Pedestrian",
            "Pickup-Truck", "Semi-Truck",
            "Trailer"
            ]


ZONE_IN_POLYGONS = [
    np.array([
    [496, 238],[621, 225],[613, 100],[496, 109]
    ]),np.array([
    [1268, 271],[1138, 282],[1032, 261],[878, 269],[865, 179],[1270, 171]
    ]),np.array([
    [333, 713],[629, 709],[658, 417],[392, 421]
    ]),np.array([
    [129, 449],[258, 311],[4, 311],[0, 441]
    ])
]

ZONE_OUT_POLYGONS = [
    np.array([
    [629, 225],[746, 225],[708, 92],[621, 96]
    ]),np.array([
    [963, 296],[1042, 388],[1275, 363],[1271, 284]
    ]),np.array([
    [142, 438],[354, 434],[308, 704],[50, 704]
    ]),np.array([
    [0, 313],[76, 307],[161, 286],[236, 213],[3, 225]
    ])
]

class DetectionsManager:
    def __init__(self) -> None:
        self.tracker_id_to_zone_id: Dict[int, int] = {}
        self.counts: Dict[int, Dict[int, Set[int]]] = {}

    def update(
        self,
        detections_all: sv.Detections,
        detections_in_zones: List[sv.Detections],
        detections_out_zones: List[sv.Detections],
    ) -> sv.Detections:
        for zone_in_id, detections_in_zone in enumerate(detections_in_zones):
            for tracker_id in detections_in_zone.tracker_id:
                self.tracker_id_to_zone_id.setdefault(tracker_id, zone_in_id)

        for zone_out_id, detections_out_zone in enumerate(detections_out_zones):
            for tracker_id in detections_out_zone.tracker_id:
                if tracker_id in self.tracker_id_to_zone_id:
                    zone_in_id = self.tracker_id_to_zone_id[tracker_id]
                    self.counts.setdefault(zone_out_id, {})
                    self.counts[zone_out_id].setdefault(zone_in_id, set())
                    self.counts[zone_out_id][zone_in_id].add(tracker_id)
        if len(detections_all) > 0:
            detections_all.class_id = np.vectorize(
                lambda x: self.tracker_id_to_zone_id.get(x, -1)
            )(detections_all.tracker_id)
        else:
            detections_all.class_id = np.array([], dtype=int)
        return detections_all[detections_all.class_id != -1]


def initiate_polygon_zones(
    polygons: List[np.ndarray],
    frame_resolution_wh: Tuple[int, int],
    triggering_anchors: Iterable[sv.Position] = [sv.Position.CENTER],
) -> List[sv.PolygonZone]:
    return [
        sv.PolygonZone(
            polygon=polygon,
            frame_resolution_wh=frame_resolution_wh,
            triggering_anchors=triggering_anchors,
        )
        for polygon in polygons
    ]


class VideoProcessor():
    def __init__(
        self,
        roboflow_api_key: str,
        model_id: str,
        source_video_path: str,
        target_video_path: str = None,
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7,
    ) -> None:
        self.conf_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.source_video_path = source_video_path
        self.target_video_path = target_video_path
        self.model = get_roboflow_model(model_id=model_id, api_key=roboflow_api_key)
        self.tracker = sv.ByteTrack()
        self.stopped = False
        
        self.north_count = self.south_count = self.west_count = self.east_count = self.sum = 0
        self.video_info = sv.VideoInfo.from_video_path(source_video_path)
        self.zones_in = initiate_polygon_zones(
            ZONE_IN_POLYGONS, self.video_info.resolution_wh, [sv.Position.CENTER]
        )
        self.zones_out = initiate_polygon_zones(
            ZONE_OUT_POLYGONS, self.video_info.resolution_wh, [sv.Position.CENTER]
        )

        self.bounding_box_annotator = sv.BoundingBoxAnnotator(color=COLORS)
        self.label_annotator = sv.LabelAnnotator(
            color=COLORS, text_color=sv.Color.BLACK
        )
        self.trace_annotator = sv.TraceAnnotator(
            color=COLORS, position=sv.Position.CENTER, trace_length=100, thickness=2
        )
        self.detections_manager = DetectionsManager()

    def process_video(self):
        
        frame_generator = sv.get_video_frames_generator(
            source_path=self.source_video_path
        )
        if self.target_video_path:
            with sv.VideoSink(self.target_video_path, self.video_info) as sink:
                for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                    if self.stopped:  # Check if processing should stop
                        break
                    
                    annotated_frame = self.process_frame(frame)
                    sink.write_frame(annotated_frame)
        else:
            for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                annotated_frame = self.process_frame(frame)
                
                annotated_frame = self.process_frame(frame)
                cv2.imshow("Processed Video", annotated_frame)
                if self.stopped:  # Check if processing should stop
                        break
                if cv2.waitKey(1) & 0xFF == ord("q") :
                    break
            cv2.destroyAllWindows()
        
    def stop_video(self):
        self.stopped = True


    def annotate_frame(
        self, frame: np.ndarray, detections: sv.Detections
    ) -> np.ndarray:
        annotated_frame = frame.copy()
        for i, (zone_in, zone_out) in enumerate(zip(self.zones_in, self.zones_out)):
            annotated_frame = sv.draw_polygon(
                annotated_frame, zone_in.polygon, COLORS.colors[i]
            )
            annotated_frame = sv.draw_polygon(
                annotated_frame, zone_out.polygon, COLORS.colors[i]
            )

        labels = [f"{tracker_id}" for tracker_id in detections.tracker_id]

        annotated_frame = self.trace_annotator.annotate(annotated_frame, detections)
        annotated_frame = self.bounding_box_annotator.annotate(
            annotated_frame, detections
        )
        annotated_frame = self.label_annotator.annotate(
            annotated_frame, detections, labels
        )

        total_count_zone_out = 0
        frame_counter = 0
        
        text_output = ""

        for zone_out_id, zone_out in enumerate(self.zones_out):
            zone_center = sv.get_polygon_center(polygon=zone_out.polygon)
            if zone_out_id in self.detections_manager.counts:
                counts = self.detections_manager.counts[zone_out_id]
                total_count_zone_out = 0
                for i, zone_in_id in enumerate(counts):
                    count = len(self.detections_manager.counts[zone_out_id][zone_in_id])
                    text_anchor = sv.Point(x=zone_center.x, y=zone_center.y + 40 * i)
                    total_count_zone_out += count
                    annotated_frame = sv.draw_text(
                        scene=annotated_frame,
                        text=str(count),
                        text_anchor=text_anchor,
                        background_color=COLORS.colors[zone_in_id],
                    )
                    frame_counter += 1

                    if zone_out_id == 0:
                        self.north_count = total_count_zone_out
                    elif zone_out_id == 1:
                        self.west_count = total_count_zone_out
                    elif zone_out_id == 2:
                        self.south_count = total_count_zone_out
                    elif zone_out_id == 3:
                        self.east_count = total_count_zone_out

                    if frame_counter == 1:
                    # Print the total count for the current zone_out
                        self.sum = self.north_count+self.west_count+self.south_count+self.east_count
                        # print(f"Total count for the Zone {zone_out_id}: {total_count_zone_out}")
                        # print(f"The sum for the zones {sum}")
                        text_output += f"Total count for the North zone: {self.north_count}\n"
                        text_output += f"Total count for the West zone: {self.west_count}\n"
                        text_output += f"Total count for the South zone: {self.south_count}\n"
                        text_output += f"Total count for the East zone: {self.east_count}\n"
                        text_output += f"Total sum of counts for all zones: {self.sum}\n\n"
                        frame_counter = 0
                    
        with open('Traffic summary counts.txt', 'w') as file:
            file.write(text_output)
        return annotated_frame
    
    def get_north_count(self):
        return self.north_count

    def get_south_count(self):
        return self.south_count

    def get_east_count(self):
        return self.east_count

    def get_west_count(self):
        return self.west_count
    def get_sum_count(self):
        return self.sum
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        results = self.model.infer(
            frame, confidence=self.conf_threshold, iou_threshold=self.iou_threshold
        )[0]
        detections = sv.Detections.from_inference(results)

        detections.class_id = np.zeros(len(detections))
        detections = self.tracker.update_with_detections(detections)

        detections_in_zones = []
        detections_out_zones = []

        for zone_in, zone_out in zip(self.zones_in, self.zones_out):
            detections_in_zone = detections[zone_in.trigger(detections=detections)]
            detections_in_zones.append(detections_in_zone)
            detections_out_zone = detections[zone_out.trigger(detections=detections)]
            detections_out_zones.append(detections_out_zone)
            

        detections = self.detections_manager.update(
            detections, detections_in_zones, detections_out_zones
        )
        
        return self.annotate_frame(frame, detections)

from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes

on_prediction=render_boxes

pipeline = InferencePipeline.init(
    model_id="vehicle-detection-fjtcf/3",
    video_reference=r"C:\Users\chris\SeniorProject-Off-Pavement-Road-Classification-main\VIDEOS\test#2.mp4",
    on_prediction=render_boxes
)

if __name__ == "__main__":

    #pipeline.start()
    #pipeline.join()

    processor = VideoProcessor(
        roboflow_api_key="HOlvoPdcKkvJa5DvYZr0",
        model_id="vehicle-detection-fjtcf/3",
        source_video_path=r"C:\Users\chris\SeniorProject-Off-Pavement-Road-Classification-main\VIDEOS\test#4.mp4",
        confidence_threshold=0.3,
        iou_threshold=0.7,
    )
    processor.process_video()
#target_video_path=r"C:\Users\chris\SeniorProject-Off-Pavement-Road-Classification-main\video_out#3.mp4"