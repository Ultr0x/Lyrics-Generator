from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pytube
from urllib import request
import lyricsgenius as lg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import simple_image_download.simple_image_download as simp
import ssl
import urllib.request
import re
import cv2
import glob
from moviepy.editor import *
import os, random
#https solver
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
genius = lg.Genius('44iEjPByRCpaPtRNjGKU-BaRmLZhKnUzys77j7I-j7kic-BvRaHWY2k86-1aoVhT',  # Client access token from Genius Client API page
                             skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
                             remove_section_headers=True)



#GRABBED FROM https://towardsdatascience.com/song-lyrics-genius-api-dcc2819c29
def get_lyrics(name, k):  # Write lyrics of k songs by each artist in arr
    c = 0  # Counter
    global title
    try:
        songs = (genius.search_artist(name, max_songs=k, sort='popularity')).songs
        s = [song.lyrics for song in songs]
        file.write("\n \n".join(s))  # Deliminator
        c += 1
        print(f"Songs grabbed:{len(s)}")

    except:
        print(f"some exception at {name}: {c}")
        sys.exit("Error message")
    h= s[0]
    print(type(h))
    title, sep, tail = h.partition('Lyrics')
    title = ''.join(title.split())
    chars = """%&{}\<>*?/$!"'’,:@+`|=."""
    for char in chars:
        title = title.replace(char, "")

    print(title)
    title = title+"-"+x
    file.close()
    #get_lyrics.n = 5

#Creating Directories
def create_dir(dir1,dir2):
    try:
        os.mkdir(dir1+dir2+"/")
    except OSError:
        print ("Creation of the directory %s failed" % dir2+"/")
    else:
        print ("Successfully created the directory %s " % dir2+"/")


#Downloading Images
def download_photos(name,myline):
    global line_save
    my_downloader = simp.Downloader()
    # Change Direcotory
    my_downloader.directory = 'Photos/'
    # Change File extension type
    my_downloader.extensions = '.jpg'
    print(my_downloader.extensions)
    try:
        my_downloader.download(myline, limit=8, verbose=True)
    except:
        img = Image.new('RGB', (1000, 1000), color='white')
        img.save('Photos/'+myline+"/"+myline+'.jpg')
        print("Connection refused")
        pass

#download_photos(x)

#Photo Adjusting

def photo_adjusting(dir_name):
    openimage=random.choice(os.listdir(dir_name))
    print(openimage)
    #code from https://github.com/RiddlerQ/simple_image_download/blob/master/Example/sample.py
    w1, h1 = 1000,1000
    # creating new Image object
    im=Image.open(dir_name+"/"+openimage)
    im = im.convert('RGB')
    im1 = im.crop()
    newsize=(w1,h1)
    im1 = im1.resize(newsize)
    im1 = im1.filter(ImageFilter.GaussianBlur(3))
    im1.save('PhotosSquare/'+ x +"/" +x+ str(n)+".jpg")
    print("edited photo saved!")

#photo_adjusting(photos)

#adding text

def adding_text():
    global n
    n = 0
    #getting words for which images already downloaded
    text_file = open("database.txt", "r")
    list_words = text_file.read()
    text_file.close()
    print(list_words)
    lyrics = open(x + '.txt', encoding='utf-8')
    for line in lyrics:
        for word in line.split():
            n=n+1
            word = ''.join(word.split())
            chars = """%&{}\<>*?/$!"'’()_-,:@+Ι`è|=."""
            for char in chars:
                word = word.replace(char, "")
            photos = "Photos/" + word + "/"
            print("word is-", word,"-")
            word_check = "-"+word+"-"
            if word_check in list_words:
                print(word+" already in database")
                pass
            else:
                #adding word to the database and downloading its image
                print(word + " not in database")
                f = open('database.txt', 'a')
                f.write("-"+ word + "-")
                f.close()
                download_photos(x, word)
            photo_adjusting(photos)
            if len(os.listdir("Photos/" + word + "/")) == 0:
                img = Image.new('RGB', (1000, 1000), color='white')
                img.save('Photos/' + word + "/" + word + '.jpg')
            img = Image.open('PhotosSquare/'+ x +"/" +x+ str(n)+".jpg")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('comic-sans-ms.ttf', 100)
            draw.text((500, 500), word, fill=(255), anchor="mm", font=font, stroke_width=2, stroke_fill=(0))
            img.save('PhotosWithText/'+ x +"/" +x+ str(n)+".jpg")



#Download video

def download_video(name):
    search_keyword=name
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    link = "https://www.youtube.com/watch?v=" + video_ids[0]
    yt = pytube.YouTube(link)
    stream = yt.streams.filter(res="720p").first().download()
    os.rename(stream, name+'audio.mp4')


#Create Movie from Images

def generate_movie(title,name):
    img_array = []
    dir_name = 'PhotosWithText/'+ name +'/*.jpg'
    # Get list of all files only in the given directory
    list_of_files = filter(os.path.isfile,
                           glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files,
                           key=os.path.getmtime)
    for file in list_of_files:
        img = cv2.imread(file)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(title+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 24/frame_length, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

# adding audio to the video clip
def add_audio(name):
    audioclip = AudioFileClip(name+"audio.mp4")
    videoclip = VideoFileClip(name+".mp4")

    videoclip2 = videoclip.set_audio(audioclip)
    videoclip2.write_videofile(name+"Final.mp4")

#count words and frames and for how many frames one image should be displayed
def count(filename):
    video = cv2.VideoCapture(filename)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    file = open(x+".txt", "r")
    # Gets each line till end of file is reached
    count=0
    for line in file:
        # Splits each line into words
        words = line.split(" ");
        # Counts each word
        count = count + len(words);

    print("Number of words present in given file: " + str(count));
    print("frames count: ", frame_count)
    global frame_length
    frame_length = int(frame_count/count)
    print("length of a frame is: ",frame_length)
    file.close();

#delete certain files if needed
def delete_files(folder,name):
    files = glob.glob(folder +"/"+ name +'/*.jpg')
    for f in files:
        os.remove(f)
    print("deleted")

#---------------END OF METHOD DECLARATIONS--------------------

#Type Artist
x = input("Type a name of an artist: ")
x = ''.join(x.split())
file = open(x+".txt", "w", encoding='utf-8') # write to the file
get_lyrics(x, 1)

#Opening Textfile and deleteing some words
string_to_delete = ['Lyrics', 'Embed']
with open(x+".txt", "r",encoding='utf-8') as input:
    with open("_.txt", "w",encoding='utf-8') as output:
        for line in input:
            for word in string_to_delete:
                line = line.replace(word, " ")
            output.write(line)

# replace file with original name
os.replace('_.txt', x+'.txt')

#create directories
create_dir("Photos/","")
create_dir("PhotosWithText/","")
create_dir("PhotosSquare/","")
create_dir("PhotosWithText/",x)
create_dir("PhotosSquare/",x)
download_video(title)
count(title+'audio.mp4')

adding_text()

generate_movie(title,x)

add_audio(title)

