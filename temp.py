import cv2
import numpy as np
import pytesseract

# Set the path to the Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to load and preprocess images
def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
    return image


# Function to extract visual features (you can customize this based on your needs)
def extract_visual_features(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the average intensity as a feature
    average_intensity = np.mean(gray_image)
    
    # Return the feature vector
    return np.array([average_intensity])

# Function to extract text features using OCR
def extract_text_features(image):
    text = pytesseract.image_to_string(image).lower()
    
    # Define keywords related to subjects or topics
    math_keywords = ['math', 'algebra', 'geometry', 'calculus']
    science_keywords = ['science', 'physics', 'chemistry', 'biology']
    
    # Check the presence of keywords in the text
    math_feature = any(keyword in text for keyword in math_keywords)
    science_feature = any(keyword in text for keyword in science_keywords)
    
    # Return the feature vector
    return np.array([math_feature, science_feature], dtype=np.float32)

# Load and preprocess your dataset
# ...

# Create a Normal Bayes Classifier
model = cv2.ml.NormalBayesClassifier_create()

# Example data (replace this with your actual data loading logic)
visual_features = np.random.rand(10, 1)  # Replace with actual visual features
text_features = np.random.randint(2, size=(10, 2))  # Replace with actual text features
labels = np.random.randint(2, size=10)  # Replace with actual labels

# Prepare data for training
features = np.concatenate((visual_features, text_features), axis=1)
features = np.array(features, dtype=np.float32)
labels = np.array(labels, dtype=np.int32)

# Train the classifier
model.train(features, cv2.ml.ROW_SAMPLE, labels)

# Now, you can use the trained model to predict the subject or topic of new images
# For example, assume `new_image_path` is the path to the image to be classified
new_image = load_and_preprocess_image("./image.jpg")
new_text_features = np.array([extract_text_features(new_image)], dtype=np.float32)
new_visual_features = np.array([extract_visual_features(new_image)], dtype=np.float32)
new_features = np.concatenate((new_visual_features, new_text_features), axis=1)

# Predict the label
_, result = model.predict(new_features)
predicted_label = int(result[0])

# Use the predicted_label in your application
print(f"The predicted label is: {predicted_label}")
# ...
