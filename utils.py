import time

import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def calculate_angle(a, b, c):
    """Calculate the angle between three points."""
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle


def get_joint_coordinates(mediapipe_result, joints_to_get):
    """Get the coordinates for all joints from the mediapipe result."""
    landmarks = mediapipe_result.pose_landmarks.landmark

    def get_joint_tuple(joint_name):
        """Get the tuple for a joint."""
        return [landmarks[mp_pose.PoseLandmark[joint_name].value].x,
                landmarks[mp_pose.PoseLandmark[joint_name].value].y]

    joints_coordinates = {}
    for joint in joints_to_get:
        joints_coordinates[joint] = get_joint_tuple(joint)

    return joints_coordinates


def set_session_states():
    """Set the session states for the Analysis carousal"""
    if 'arm_index' not in st.session_state:
        st.session_state.arm_index = -1

    if 'head_index' not in st.session_state:
        st.session_state.head_index = -1

    if 'leg_index' not in st.session_state:
        st.session_state.leg_index = -1


@st.cache(persist=True, suppress_st_warning=True, allow_output_mutation=True)
def init_model():
    """Initialize the pose estimation model"""

    return mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=2,
                        static_image_mode=False)


def process_main_feed(frame, model):
    """Processes the main feed and returns predictions"""
    img = frame.to_ndarray(format="bgr24")
    # load img with cv2:
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img.flags.writeable = False
    results = model.process(img)
    img.flags.writeable = True
    return results, img


def postprocess_main_feed(image, results):
    """Postprocess the main feed by drawing detected points"""
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    # flip image horizontally:
    image = cv2.flip(image, 1)

    # add today's date and time on bottom right in red:
    cv2.putText(image, time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()),
                (image.shape[1] - 200, image.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return image
