import io
import base64
from zipfile import ZipFile
from utils import get_dataset_names, get_preview_images, total_image_count, save_images_to_dataset
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def home():
    dataset_list = get_dataset_names()
    resp = app.make_response(render_template('home.html', dataset_names=dataset_list))
    return resp


@app.route('/explore_dataset/<dataset_name>/<page_no>')
def explore_dataset(dataset_name, page_no):
    if dataset_name:
        has_prev = has_next = True
        image_per_page = 10
        if page_no:
            page_no = int(page_no)
            total_images = total_image_count(dataset_name)
            total_pages = total_images // image_per_page
            total_pages = total_pages if total_pages % image_per_page == 0 else total_pages+1
            images = get_preview_images(dataset_name, count=image_per_page, idx=page_no - 1, max_count=total_images)
        else:
            page_no = 1
            total_images = total_image_count(dataset_name)
            total_pages = total_images // image_per_page
            total_pages = total_pages if total_pages % image_per_page == 0 else total_pages+1
            images = get_preview_images(dataset_name, count=image_per_page, idx=page_no - 1, max_count=total_images)
        image_strs = []
        for image_info in images:
            encoded_string = base64.b64encode(image_info['image']).decode('utf-8')
            image_strs.append({'image': 'data:image/jpeg;base64,' + encoded_string, 'caption': image_info['filename']})

        total_pages_current = ((page_no // 3)+1)*3 if ((page_no // 3)+1)*3 < total_pages else total_pages
        min_pages_current = (page_no // 3) * 3 if page_no >= 3 else 1
        if page_no < 3:
            has_prev = False
        if total_pages_current == total_pages:
            has_next = False
        resp = app.make_response(render_template('image-gallery.html', images=image_strs,
                                                 total_pages=total_pages_current, min_pages=min_pages_current,
                                                 dataset_name=dataset_name, page_no=page_no, has_prev = has_prev,
                                                 has_next=has_next))
    else:
        dataset_list = get_dataset_names()
        resp = app.make_response(render_template('home.html', dataset_names=dataset_list))
    return resp


@app.route('/file_upload')
def file_upload():
    resp = app.make_response(render_template('file-upload.html'))
    return resp


@app.route('/add_dataset', methods=['GET', 'POST'])
def add_dataset():
    dataset_list = get_dataset_names()
    if request.method == 'POST':
        dataset_name = request.form['datasetName']
        if dataset_name in dataset_list:
            flash("Dataset name already exists", category="error")
            return redirect(url_for('file_upload'))
        dataset_file = request.files['file']
        if dataset_file.filename != '':
            z = ZipFile(io.BytesIO(dataset_file.stream.read()))
            file_list = z.infolist()
            images = []
            for i in file_list:
                images.append({"image": z.read(i), "dataset_name": dataset_name, "filename": i.filename})
            save_images_to_dataset(images)
            flash("Dataset saved successfully", category="message")
        else:
            flash("Upload unsuccessful", category="error")
            return redirect(url_for('file_upload'))
    elif request.method == 'GET':
        return redirect(url_for('file_upload'))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
