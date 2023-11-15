import cv2
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pytesseract

# Preprocess
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return image

# Extrac text
def extract_text(image):
    return pytesseract.image_to_string(image)

def text_to_features(texts):
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    return features, vectorizer

def train_classifier(features, labels):
    classifier = MultinomialNB()
    classifier.fit(features, labels)
    return classifier

def predict_label(classifier, image):
    image = preprocess_image(image)
    text = extract_text(image)
    features = text_to_features([text])
    return classifier.predict(features)


image_paths = ["./images/image1.png", "./images/image2.png", "./images/image3.png"]	
labels = ["Physics", "Math", "Physics"]
new_image_path = ["./new_images/crop_47.png"]

images = [preprocess_image(image_path) for image_path in image_paths]
texts = [extract_text(image) for image in images]
features = text_to_features(texts)
classifier = train_classifier(features, labels)

# Train the classifier
features, vectorizer = text_to_features(texts)  
classifier = train_classifier(features, labels)


print(predict_label(classifier, vectorizer, new_image_path))