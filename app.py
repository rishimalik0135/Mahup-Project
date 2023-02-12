import streamlit as st
from youtube import Video
import os
import smtplib
from youtube_search import YoutubeSearch
from pytube import YouTube
from moviepy.editor import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(email, password, to, subject, body, file_path):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    with open(file_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', "attachment; filename= %s" % file_path)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, msg.as_string())
    server.quit()

def createmash(Singer,num,dur):
    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    for i in mp3_files:
        os.remove(i)

    results = YoutubeSearch(Singer, max_results=int(num)).to_dict()

    for i in results:
        video = YouTube('http://youtube.com/watch?v='+i['id']).streams.filter(only_audio=True).first().download()
        base, ext = os.path.splitext(video)
        new_file = base + '.mp3'
        os.rename(video, new_file)

    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    ad = AudioFileClip(mp3_files[0])
    merged_audio=ad.subclip(0,0)

    time=int(dur)
    for i in range(0,len(mp3_files)):
        audio = AudioFileClip(mp3_files[i])
        trimmed_audio = audio.subclip(10, time+10)
        merged_audio = concatenate_audioclips([merged_audio, trimmed_audio])

    merged_audio.write_audiofile("output.mp3")
    return os.getcwd()+"/output.mp3"


st.set_page_config(page_title="MashIT By Rishi Malik")
st.subheader("Mashup Maker")

st.write("Enter details: ")

with st.form("my_form"):
   Singer = st.text_input("Singer Name")
   num = st.text_input("Number of songs")
   dur = st.text_input("Audio duration")
   rec_email = st.text_input("Enter Email")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       output=createmash(Singer,num,dur)
       email = "rmalik_be20@thapar.edu"
       password = 'tzspoopoafwrrrwe'
       to = rec_email
       subject = "MashIT By Rishi Malik"
       body = "Enjoy Your Mashup..."
       file_path = os.getcwd()+"/output.mp3"
       send_email_with_attachment(email, password, to, subject, body, file_path)
       st.subheader("Check Your Mail.....")

