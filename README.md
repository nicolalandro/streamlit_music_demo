# Music Streamlit demo

This is a streamlit demo App for music application.

![demo](imgs/demo.png)

## Run

```
# ubuntu/debian based
sudo apt-get install -y lilypond 
# opensuse
sudo zypper in lilypond

python3.8 -m pip install -r requirements.txt
python3.8 -m streamlit run app.py
firefox http://localhost:8501
```

# Reference
Here I list the basic knowledge used to implement this project.
* python and pip
* [Sreamlit](https://streamlit.io/): GUI library
* [Music21](http://web.mit.edu/music21/): to read and plot .xml music
* [LillyPond](https://lilypond.org/): dependecy of Music21 to plot partiture
* [pretty_midi](http://craffel.github.io/pretty-midi/): to read mid and synthesize it into a wav
* numpy: for math operation