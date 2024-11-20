from flask import Flask, request, send_file
import dropbox

app = Flask(__name__)

# Initialize Dropbox
dbx = dropbox.Dropbox('sl.CBGdob8AJ3klr1uuSyGiAOwOwe827t4PWxvy7K3YRL5V3jwnNO97yX7Yr0gDhDhpQDQiWT9HhjONxG83dZJQK82xZbewiRBSuI_RGEBPpxCdIyw0zE_3x7JqYtKQJPTQEFfyWbx-HMrFh1BzFmCi774')
@app.route('/')
def home():
    return '''
    <h1>File Upload/Download with Dropbox</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>
    <form action="/download" method="post">
        <input type="text" name="filename" placeholder="Enter filename to download">
        <button type="submit">Download</button>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        dbx.files_upload(file.read(), f"/{file.filename}")
        return f"File {file.filename} uploaded successfully!"
    return "No file uploaded."

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    if filename:
        try:
            _, file_content = dbx.files_download(f'/{filename}')
            return send_file(
                file_content.raw, as_attachment=True, download_name=filename
            )
        except dropbox.exceptions.HttpError as err:
            return f"Error: {err}"
    return "Filename not provided."

if __name__ == '__main__':
    app.run(debug=True)
