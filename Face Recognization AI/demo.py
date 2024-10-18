import gradio as gr
import requests
import datadog_api_client
from PIL import Image

def compare_face(frame1, frame2):
    url = "http://127.0.0.1:8080/compare_face"
    files = {'file1': open(frame1, 'rb'), 'file2': open(frame2, 'rb')}

    r = requests.post(url=url, files=files)

    html = None
    faces = None

    compare_result = r.json().get('compare_result')
    compare_similarity = r.json().get('compare_similarity')

    html = ("<table>"
                "<tr>"
                    "<th>Compare Result</th>"
                    "<th>Value</th>"
                "</tr>"
                "<tr>"
                    "<td>Result</td>"
                    "<td>{compare_result}</td>"
                "</tr>"
                "<tr>"
                    "<td>Similarity</td>"
                    "<td>{compare_similarity}</td>"
                "</tr>"
                "</table>".format(compare_result=compare_result, compare_similarity=compare_similarity))

    try:
        image1 = Image.open(frame1)
        image2 = Image.open(frame2)

        face1 = None
        face2 = None

        if r.json().get('face1') is not None:
            face = r.json().get('face1')
            x1 = face.get('x1')
            y1 = face.get('y1')
            x2 = face.get('x2')
            y2 = face.get('y2')

            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 >= image1.width:
                x2 = image1.width - 1
            if y2 >= image1.height:
                y2 = image1.height - 1

            face1 = image1.crop((x1, y1, x2, y2))
            face_image_ratio = face1.width / float(face1.height)
            resized_w = int(face_image_ratio * 150)
            resized_h = 150

            face1 = face1.resize((int(resized_w), int(resized_h)))

        if r.json().get('face2') is not None:
            face = r.json().get('face2')
            x1 = face.get('x1')
            y1 = face.get('y1')
            x2 = face.get('x2')
            y2 = face.get('y2')

            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 >= image2.width:
                x2 = image2.width - 1
            if y2 >= image2.height:
                y2 = image2.height - 1

            face2 = image2.crop((x1, y1, x2, y2))
            face_image_ratio = face2.width / float(face2.height)
            resized_w = int(face_image_ratio * 150)
            resized_h = 150

            face2 = face2.resize((int(resized_w), int(resized_h)))

        if face1 is not None and face2 is not None:
            new_image = Image.new('RGB',(face1.width + face2.width + 10, 150), (80,80,80))

            new_image.paste(face1,(0,0))
            new_image.paste(face2,(face1.width + 10, 0))
            faces = new_image.copy()
        elif face1 is not None and face2 is None:
            new_image = Image.new('RGB',(face1.width + face1.width + 10, 150), (80,80,80))

            new_image.paste(face1,(0,0))
            faces = new_image.copy()
        elif face1 is None and face2 is not None:
            new_image = Image.new('RGB',(face2.width + face2.width + 10, 150), (80,80,80))

            new_image.paste(face2,(face2.width + 10, 0))
            faces = new_image.copy()

    except:
        pass

    return [faces, html]

with gr.Blocks() as demo:
    gr.Markdown(
        """
    # Face Recognition
    A demo face Recognition Neural Network
    """
    )
    with gr.TabItem("Face Recognition"):
        gr.Markdown(
            """
        """
        )
        with gr.Row():
            with gr.Column():
                compare_face_input1 = gr.Image(type='filepath')
                gr.Examples(['face_examples/1.jpg', 'face_examples/3.jpg', 'face_examples/5.jpg', 'face_examples/7.jpg', 'face_examples/9.jpg'], 
                            inputs=compare_face_input1)
                compare_face_button = gr.Button("Compare Face")
            with gr.Column():
                compare_face_input2 = gr.Image(type='filepath')
                gr.Examples(['face_examples/2.jpg', 'face_examples/4.jpg', 'face_examples/6.jpg', 'face_examples/8.jpg', 'face_examples/10.jpg'], 
                            inputs=compare_face_input2)
            with gr.Column():
                compare_face_output = gr.Image(type="pil").style(height=150)
                compare_result_output = gr.HTML(label='Result')

        compare_face_button.click(compare_face, inputs=[compare_face_input1, compare_face_input2], outputs=[compare_face_output, compare_result_output])
    gr.HTML('<a href="https://visitorbadge.io/status?path=https%3A%2F%2Fhuggingface.co%2Fspaces%2Fkby-ai%2FFaceRecognition"><img src="https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fhuggingface.co%2Fspaces%2Fkby-ai%2FFaceRecognition&countColor=%23263759" /></a>')

demo.launch(server_name="0.0.0.0", server_port=7860)