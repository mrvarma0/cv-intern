import streamlit as st
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import io
from PIL import Image
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def object_detection_app():
    st.title("Product Recognition Filter")
    url = st.text_input("Enter Image URL:")
    if url:
        image = Image.open(requests.get(url, stream=True).raw)
        processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(image)

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            class_name = model.config.id2label[label.item()]
            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(box[0], box[1], f'{class_name} {round(score.item(), 3)}', bbox=dict(facecolor='white', alpha=0.5))

        ax.axis('off')
        st.pyplot(fig)

def text_to_image_app():
    st.title("Generative AI for Visuals")
    input_text = st.text_input("Enter a description for the image")
    if st.button("Generate Image"):
        if input_text:
            image_bytes = query({"inputs": input_text})
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please enter a description for the image")

def classify_items():
    st.title("Exclusion of Non-Relevant Images")
    url = st.text_input("Enter Image URL:")
    if url:
        image = Image.open(requests.get(url, stream=True).raw)
        processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(image)

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            class_name = model.config.id2label[label.item()]
            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(box[0], box[1], f'{class_name} {round(score.item(), 3)}', bbox=dict(facecolor='white', alpha=0.5))

        ax.axis('off')
        st.pyplot(fig)

        relevant_labels = ["Shoe", "Sneaker", "Bottle", "Cup", "Sandal", "Perfume", "Toy", "Sunglasses", "Car",
                           "Water Bottle", "Chair", "Office Chair", "Can", "Cap", "Hat", "Couch", "Wristwatch",
                           "Glass", "Bag", "Handbag", "Baggage", "Suitcase", "Headphones", "Jar", "Vase"]

        # Check if any relevant label is detected
        relevant_detection = False
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            class_name = model.config.id2label[label.item()].lower()
            if class_name in [label.lower() for label in relevant_labels]:
                relevant_detection = True
                print(relevant_detection)
                break

        # Display the classification result
        if relevant_detection:
            st.write("Image contains relevant objects.")
        else:
            st.write("Image does not contain relevant objects.")
        
# def classify_items():
#     st.title("Exclusion of Non-Relevant Images")
#     url = st.text_input("Enter Image URL:")
#     if url:
#         image = Image.open(requests.get(url, stream=True).raw)
#         processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
#         model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
#         inputs = processor(images=image, return_tensors="pt")
#         outputs = model(**inputs)
#         target_sizes = torch.tensor([image.size[::-1]])
#         results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

#         fig, ax = plt.subplots(figsize=(10, 10))
#         ax.imshow(image)

#         for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
#             box = [round(i, 2) for i in box.tolist()]
#             class_name = model.config.id2label[label.item()]
#             rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
#                                      linewidth=1, edgecolor='r', facecolor='none')
#             ax.add_patch(rect)
#             ax.text(box[0], box[1], f'{class_name} {round(score.item(), 3)}', bbox=dict(facecolor='white', alpha=0.5))

#         ax.axis('off')
#         st.pyplot(fig)

#         relevant_labels = ["Shoe", "Sneaker", "Bottle", "Cup", "Sandal", "Perfume", "Toy", "Sunglasses", "Car",
#                        "Water Bottle", "Chair", "Office Chair", "Can", "Cap", "Hat", "Couch", "Wristwatch",
#                        "Glass", "Bag", "Handbag", "Baggage", "Suitcase", "Headphones", "Jar", "Vase"]

#     # Check if any relevant label is detected
#         relevant_detection = False
#         for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
#             class_name = model.config.id2label[label.item()].lower()
#             if class_name in [label.lower() for label in relevant_labels]:
#                 relevant_detection = True
#                 print(relevant_detection)
#                 break

#     # Display the classification result
#     if relevant_detection:
#         st.write("Image contains relevant objects.")
#     else:
#         st.write("Image does not contain relevant objects.")


            # Sidebar
app_selection = st.sidebar.radio("Select App", ("Object Detection", "Text to Image Generation","non relevant images"))

# Main app logic based on selected app
if app_selection == "Object Detection":
    object_detection_app()
elif app_selection == "Text to Image Generation":
    text_to_image_app()
elif app_selection == "non relevant images":
    classify_items()