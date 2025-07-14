from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(word="Hellooo!!", letter="o", api_name="/predict")
print(result)
