import tempfile
import io

import streamlit as st
from PIL import Image

import pretty_midi
import music21
import note_seq
from scipy.io import wavfile

import numpy as np

st.title('Music Demo')
st.markdown('This example need a .xml music file as input and show partiture, piano roll and a simply wav. You can generate it from MuseScore or similar software.')

# example_1 = st.button('Test Example')

uploaded_file = st.file_uploader("Choose a .xml music file", type='xml')

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(suffix=".xml") as f:
        f.write(uploaded_file.getbuffer())
        file_path = f.name

        # Show partiture with music21
        music = music21.converter.parse(file_path)
        streaming_partiture = str(music.write('/tmp/lily.png'))
        image = Image.open(streaming_partiture)
        st.text('Partiture')
        st.image(image)

        # save to mid
        midi_path = file_path + '.mid'
        music.write('midi', fp=midi_path)

        # plot piano rol
        unconditional_ns = note_seq.midi_file_to_note_sequence(midi_path)
        piano_roll = note_seq.plot_sequence(unconditional_ns, show_figure=False)
        st.text('Piano Roll')
        st.bokeh_chart(piano_roll, use_container_width=True)

        # generate wav
        with st.spinner(f"Sinthezizing to wav"):
            midi_data = pretty_midi.PrettyMIDI(midi_path)
            audio_data = midi_data.synthesize()
            audio_data = np.int16(
                audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
            )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py
            virtualfile = io.BytesIO()
            wavfile.write(virtualfile, 44100, audio_data)

        st.audio(virtualfile)
        st.markdown("Download the audio by right-clicking on the media player")
