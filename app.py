import os
import io

import streamlit as st
from PIL import Image

import pretty_midi
import music21
from scipy.io import wavfile

import numpy as np

st.title('Music Demo')
st.markdown('This example need a .xml music file as input. You can generate it from MuseScore or similar software.')

uploaded_file = st.file_uploader("Choose a xml music file")

if uploaded_file is not None:
    # save file
    with open(os.path.join(os.getcwd(), uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_path = os.path.join(os.getcwd(), uploaded_file.name)

    # Show partiture with music21
    music = music21.converter.parse(file_path)
    streaming_partiture = str(music.write('lily.png'))
    image = Image.open(streaming_partiture)
    st.image(image, caption='Musical sheet')

    # save to mid
    midi_path = file_path + '.mid'
    music.write('midi', fp=midi_path)

    # generate wav
    with st.spinner(f"Transcribing to FluidSynth"):
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        audio_data = midi_data.synthesize()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py
        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)

    st.audio(virtualfile)
    st.markdown("Download the audio by right-clicking on the media player")
