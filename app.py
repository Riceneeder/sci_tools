from server.LogHandlers import ServerLogHandler, WebSocketLogHandler, fmt
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
from openai import OpenAI
from server.mods.markdown_translator import MarkdownTranslator
from server.mods.sci_pdf_to_markdown import PDFToMarkdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging
import os
import server.api_list as api_list
import atexit

app = Flask(__name__, static_url_path='/', static_folder='web', template_folder='web')
app.config['UPLOAD_FOLDER_PDFs'] = 'server/pdfs'
app.config['UPLOAD_FOLDER_MD'] = 'server/markdown'
app.config['PUBLIC_FOLDER'] = 'server/public'
app.config['OPENAI_API_KEY'] = 'sk-pUq0JojCpuvvVdP0Bb21F6766e3441B5B744D7Ea299bD5Cd'
app.config['OPENAI_API_BASE'] = 'https://free.v36.cm/v1/'
app.config['DEFAULT_HEADERS'] = {"x-foo": "true"}
openai_client = OpenAI(api_key=app.config['OPENAI_API_KEY'], base_url=app.config['OPENAI_API_BASE'], default_headers=app.config['DEFAULT_HEADERS'])
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
clients = []

server_log_handler = ServerLogHandler()
server_log_handler.setLevel(logging.INFO)
server_log_handler.setFormatter(fmt)

ws_log_handler = WebSocketLogHandler(socketio, clients)
ws_log_handler.setLevel(logging.INFO)
ws_log_handler.setFormatter(fmt)

server_logger = logging.getLogger('server')
server_logger.addHandler(server_log_handler)
server_logger.setLevel(logging.INFO)

ws_logger = logging.getLogger('ws')
ws_logger.addHandler(ws_log_handler)
ws_logger.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api', methods=['GET'])
def api():
    return api_list.api_list


@app.route('/api/upload/<string:type>', methods=['POST'])
def upload_file_pdfs(type):
    try:
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                return {"status": "error", "message": "No file selected"}
            if file:
                if type == 'pdf':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_PDFs'], file.filename))
                elif type == 'md':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER_MD'], file.filename))
        return {"status": "success", "message": "files uploaded successfully"}
    except Exception as e:
        server_logger.error(f"Error uploading files: {e}")
        ws_logger.error(f"Error uploading files: {e}")
        return {"status": "error", "message": f"Error uploading files: {e}"}


@app.route('/api/mdtranslate/<string:source>/<string:target>', methods=['POST'])
def mdtranslate(source, target):
    target_lang = target
    source_lang = source
    server_logger.info(f"Translating Markdown files from {source_lang} to {target_lang}")
    if os.path.exists(app.config['UPLOAD_FOLDER_MD']):
        try:
            for file in os.listdir(app.config['UPLOAD_FOLDER_MD']):
                markdown_translator = MarkdownTranslator(openai_client, ws_logger, output_path=app.config['PUBLIC_FOLDER'])
                file_path = os.path.join(app.config['UPLOAD_FOLDER_MD'], file)

                markdown_content = markdown_translator.read_markdown(file_path)

                translated_content = markdown_translator.process_markdown_content(markdown_content, source_lang, target_lang)

                translated_file_path = os.path.join(app.config['PUBLIC_FOLDER'], f'{file}_{target_lang}.md')
                markdown_translator.write_markdown(translated_file_path, translated_content)

                server_logger.info(f"Markdown file {file} translated successfully")
                ws_logger.info(f"Markdown file {file} translated successfully")

                os.remove(file_path)
            return {"status": "success", "message": f"Markdown file translated successfully"}
        except Exception as e:
            server_logger.error(f"Error translating Markdown file: {e}")
            ws_logger.error(f"Error translating Markdown file: {e}")
            return {"status": "error", "message": f"Error translating Markdown file: {e}"}


@app.route('/api/sci_pdf2md', methods=['POST'])
def sci_pdf2md():
    pdf2md = PDFToMarkdown(input_path=app.config['UPLOAD_FOLDER_PDFs'], output_path=app.config['PUBLIC_FOLDER'], logger=ws_logger)
    try:
        output = pdf2md.process()
        server_logger.info("PDF files converted to Markdown successfully")
        ws_logger.info("PDF files converted to Markdown successfully")
        # 删除路径下所有pdf文件
        for file in os.listdir(app.config['UPLOAD_FOLDER_PDFs']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER_PDFs'], file)
            os.remove(file_path)
        return {"status": "success", "message": "PDF files converted to Markdown successfully"}
    except Exception as e:
        server_logger.error(f"Error converting PDF files to Markdown: {e}")
        ws_logger.error(f"Error converting PDF files to Markdown: {e}")
        return {"status": "error", "message": f"Error converting PDF files to Markdown: {e}"}


@app.route('/api/get/public/list', methods=['GET'])
def get_public_list():
    return os.listdir(app.config['PUBLIC_FOLDER'])


@app.route('/api/get/pdf/list', methods=['GET'])
def get_pdf_list():
    return os.listdir(app.config['UPLOAD_FOLDER_PDFs'])


@app.route('/api/get/md/list', methods=['GET'])
def get_md_list():
    return os.listdir(app.config['UPLOAD_FOLDER_MD'])


@app.route('/api/download/public/<string:file>', methods=['GET'])
def download_public_file(file):
    ws_logger.info(f"Downloading file {os.path.join(app.config['PUBLIC_FOLDER'], file)}")
    return send_file(os.path.join(app.config['PUBLIC_FOLDER'], file))


@app.route('/api/delete/public/<string:file>', methods=['DELETE'])
def delete_public_file(file):
    try:
        os.remove(os.path.join(app.config['PUBLIC_FOLDER'], file))
        return {"status": "success", "message": f"File {file} deleted successfully"}
    except Exception as e:
        server_logger.error(f"Error deleting file {file}: {e}")
        ws_logger.error(f"Error deleting file {file}: {e}")
        return {"status": "error", "message": f"Error deleting file {file}: {e}"}


@app.route('/api/delete/pdf/<string:file>', methods=['DELETE'])
def delete_pdf_file(file):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_PDFs'], file))
        return {"status": "success", "message": f"File {file} deleted successfully"}
    except Exception as e:
        server_logger.error(f"Error deleting file {file}: {e}")
        ws_logger.error(f"Error deleting file {file}: {e}")
        return {"status": "error", "message": f"Error deleting file {file}: {e}"}


@app.route('/api/delete/md/<string:file>', methods=['DELETE'])
def delete_md_file(file):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_MD'], file))
        return {"status": "success", "message": f"File {file} deleted successfully"}
    except Exception as e:
        server_logger.error(f"Error deleting file {file}: {e}")
        ws_logger.error(f"Error deleting file {file}: {e}")
        return {"status": "error", "message": f"Error deleting file {file}: {e}"}


@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    server_logger.info(f"Client {request.sid} connected")


@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    server_logger.info(f"Client {request.sid} disconnected")


# 监视public、pdfs、markdown文件的变化
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, folder, event_name):
        self.folder = folder
        self.event_name = event_name

    def on_modified(self, event):
        if not event.is_directory:
            socketio.emit(self.event_name, {'file': event.src_path})
            server_logger.info(f"File {event.src_path} modified in {self.folder}")
            ws_logger.info(f"File {event.src_path} modified in {self.folder}")

    def on_created(self, event):
        if not event.is_directory:
            socketio.emit(self.event_name, {'file': event.src_path})
            server_logger.info(f"File {event.src_path} created in {self.folder}")
            ws_logger.info(f"File {event.src_path} created in {self.folder}")

    def on_deleted(self, event):
        if not event.is_directory:
            socketio.emit(self.event_name, {'file': event.src_path})
            server_logger.info(f"File {event.src_path} deleted in {self.folder}")
            ws_logger.info(f"File {event.src_path} deleted in {self.folder}")


def start_watching(folder, event_name):
    event_handler = FileChangeHandler(folder, event_name)
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    return observer


public_observer = start_watching(app.config['PUBLIC_FOLDER'], 'public_change')
pdfs_observer = start_watching(app.config['UPLOAD_FOLDER_PDFs'], 'pdf_change')
md_observer = start_watching(app.config['UPLOAD_FOLDER_MD'], 'md_change')

# Ensure observers are stopped and joined when the application exits
atexit.register(lambda: (public_observer.stop(), public_observer.join()))
atexit.register(lambda: (pdfs_observer.stop(), pdfs_observer.join()))
atexit.register(lambda: (md_observer.stop(), md_observer.join()))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)