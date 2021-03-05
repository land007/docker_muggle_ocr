# coding: utf-8
import tornado.ioloop
import tornado.web
import shutil
import os
import json
import base64

import time
# STEP 1
import muggle_ocr
import os
# STEP 2
#sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
root_dir = r"./imgs"
for i in os.listdir(root_dir):
    n = os.path.join(root_dir, i)
    with open(n, "rb") as f:
        b = f.read()
    st = time.time()
    # STEP 3
    text = sdk.predict(image_bytes=b)
    print(i, text, time.time() - st)

class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='/file' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')

    def post(self):
        ret = {'result': 'OK'}
        upload_path = os.path.join(os.path.dirname(__file__), 'imgs')  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret
        str = ""
        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])
                # OR do other thing

            with open(file_path, "rb") as file:
                data = file.read()
            text = sdk.predict(image_bytes=data)
            str += text
        
        ret['result'] = str
        self.write(json.dumps(ret))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='/' enctype="application/x-www-form-urlencoded" method='post'>
    <input type='text' name='image64' value='base64'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')
    
    def post(self):
        ret = {'result': 'OK'}
        upload_path = os.path.join(os.path.dirname(__file__), 'imgs')  # 文件的暂存路径
        post_data = self.request.body_arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = simplejson.loads(post_data)
#         print(post_data["image64"])
        imgdata=base64.b64decode(post_data["image64"])
#         file_path = os.path.join(upload_path, '1.jpg')
#         with open(file_path, 'wb') as file:
#             file.write(imgdata)
#         with open(file_path, "rb") as file:
#             data = file.read()
#         text = sdk.predict(image_bytes=data)
        text = sdk.predict(image_bytes=imgdata)
        print(text)
        ret['result'] = text
        self.write(json.dumps(ret))

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/file', FileUploadHandler),
])

if __name__ == '__main__':
    app.listen(8080)
    print('start 8080')
    tornado.ioloop.IOLoop.instance().start()
