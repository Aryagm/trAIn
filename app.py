import glob
import os
import time

import av
import cv2
import numpy as np
import streamlit as st
from playsound import playsound
from streamlit_webrtc import webrtc_streamer

import utils

# use wide mode for streamlit
st.set_page_config(layout="wide")

# Set the session states for the Analysis carousal:
utils.set_session_states()

# Set the title using logo image:
st.image("./assets/trAIn_logo.png", use_column_width=True)

# Sidebar for choosing Training mode or Analysis mode:
mode = st.sidebar.selectbox("Select mode", ["Train", "Analyze"])

if mode == "Train":

    utils.init_model()

    model = utils.init_model()

    # Create 2 columns for the main feed and the only pose feed:
    main_feed_col, pose_feed_col = st.columns(2)

    # Completely white image for start-up:
    main_feed_img = np.ones((256, 256, 3), dtype=np.uint8) * 255

    # Blank results for start-up:
    result = model.process_image(main_feed_img)

    last_mistake = time.time()


    def video_frame_callback(frame):
        result, image = utils.process_main_feed(frame, model)
        global result
        global main_feed_img
        main_feed_img = image.copy()
        image = utils.postprocess_main_feed(image, result)

        try:
            joints_to_get = ["LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST", "LEFT_HIP", "LEFT_KNEE", "LEFT_HEEL",
                             "LEFT_NOSE"]
            joints_coordinates = utils.get_joint_coordinates(result, joints_to_get)
            angle_arm = utils.calculate_angle(joints_coordinates["LEFT_SHOULDER"], joints_coordinates["LEFT_ELBOW"],
                                              joints_coordinates["LEFT_WRIST"])
            angle_neck = utils.calculate_angle(joints_coordinates["LEFT_HIP"], joints_coordinates["LEFT_SHOULDER"],
                                               joints_coordinates["LEFT_NOSE"])

            # Get mistake in arm:
            if angle_arm < 60 or angle_arm > 120 and time.time() - last_mistake > 10:
                # save image to ./images/arm/ with time in batches of 10 seconds:
                cv2.imwrite("./imag_data/arm/{}.jpg".format(int(time.time()) // 10), image)
                # Play sound when mistake occurs:
                playsound('./assets/audio/Arm.mp3', block=True)
                global last_mistake
                # Update the last_mistake variable:
                last_mistake = time.time()

            # get mistake in foot:
            elif joints_coordinates["LEFT_HEEL"][0] < joints_coordinates["NOSE"][0] and time.time() - last_mistake > 10:
                # save image to ./images/leg/ with time in batches of 10 seconds:
                cv2.imwrite("./imag_data/leg/{}.jpg".format(int(time.time()) // 10), image)
                # Play sound when mistake occurs:
                playsound('./assets/audio/leg.mp3', block=True)
                global last_mistake
                # Update the last_mistake variable:
                last_mistake = time.time()

            # get mistake in head:
            elif angle_neck < 120 and time.time() - last_mistake > 10:
                # save image to ./images/head/ with time in batches of 10 seconds:
                cv2.imwrite("./imag_data/head/{}.jpg".format(int(time.time()) // 10), image)
                # Play sound when mistake occurs:
                playsound('./assets/audio/head.mp3', block=True)
                global last_mistake
                # Update the last_mistake variable:
                last_mistake = time.time()

        except Exception as e:
            print(e)
            pass

        return av.VideoFrame.from_ndarray(image, format="bgr24")


    playing = st.checkbox("Playing")

    with main_feed_col:
        ctx = webrtc_streamer(key="sample", video_frame_callback=video_frame_callback, desired_playing_state=playing)

    # TODO: Add functions in utils.py to make Analyze section more concise. Unable to complete because of time
    #  constraints:
    if mode == "Analyze":
        # sort by time:
        images_arm = sorted(glob.glob("./images/arm/*.jpg"), key=os.path.getmtime, reverse=True)
        images_leg = sorted(glob.glob("./images/leg/*.jpg"), key=os.path.getmtime, reverse=True)
        images_head = sorted(glob.glob("./images/head/*.jpg"), key=os.path.getmtime, reverse=True)

        st.title("Arm")

        left_button, picture, right_button = st.columns(3)

        # make a slideshow of the images in the arm folder:
        with left_button:
            # add br tags:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            left_button_arm = st.button("<", key="left_arm")
        with right_button:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            right_button_arm = st.button(">", key="right_arm")
        with picture:
            st.image(images_arm[st.session_state.pic], use_column_width=True)
        if right_button_arm:
            st.session_state.pic -= 1
        if left_button_arm and st.session_state.pic < 0:
            st.session_state.pic += 1

        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        st.title("Leg")
        left_button_2, picture_2, right_button_2 = st.columns(3)
        # make a slideshow of the images in the leg folder:
        with left_button_2:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            left_button_leg = st.button("<", key="left_leg")
        with right_button_2:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            right_button_leg = st.button(">", key="right_leg")
        with picture_2:
            st.image(images_leg[st.session_state.pic_2], use_column_width=True)
        if right_button_leg:
            st.session_state.pic_2 -= 1
        if left_button_leg and st.session_state.pic_2 < 0:
            st.session_state.pic_2 += 1

        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)

        st.title("Head")
        left_button_3, picture_3, right_button_3 = st.columns(3)
        # make a slideshow of the images in the head folder:
        with left_button_3:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            left_button_head = st.button("<", key="left_head")
        with right_button_3:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            right_button_head = st.button(">", key="right_head")
        with picture_3:
            st.image(images_head[st.session_state.pic_3], use_column_width=True)
        if right_button_head:
            st.session_state.pic_3 -= 1
        if left_button_head and st.session_state.pic_3 < 0:
            st.session_state.pic_3 += 1
