import os
import subprocess
import numpy
import cv2
import time

from werkzeug.utils import secure_filename

GALLERY_FOLDER = './www/photo_gallery'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photo(photo_file):
    filename = secure_filename(photo_file.filename)
    output_path = os.path.join(GALLERY_FOLDER, filename)
    photo_file.save(output_path)
    make_portrait(output_path)
    return filename

def save_from_data(data):
    filename = 'uploaded_from_ios_{}.jpg'.format(int(time.time()))
    output_path = os.path.join(GALLERY_FOLDER, filename)
    nparr = numpy.fromstring(data, numpy.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite(output_path, img)
    make_portrait(output_path)
    return filename

def make_portrait(photo_path):
    subprocess.Popen(['./photo_frame/make_portrait.sh', photo_path], cwd=os.getcwd())

def random_photo():
    command = 'ls {} | sort -R | tail -n 1'.format(GALLERY_FOLDER)
    result = subprocess.run([command], shell=True, stdout=subprocess.PIPE)
    random_filename = result.stdout.decode('utf-8').rstrip()
    return random_filename
