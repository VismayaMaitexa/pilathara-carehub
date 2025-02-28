import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError
import re
import warnings

warnings.filterwarnings("ignore")
import pytesseract

# Specify the Tesseract executable path if it's not in the PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path based on your installation

# Configure the path for Tesseract (if needed)
# For Windows: 
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Preprocess the image (grayscale, noise reduction, contrast enhancement)
def preprocess_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
        img = img.filter(ImageFilter.MedianFilter())  # Remove noise
        img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
        return img
    except Exception as e:
        print(f"Error in preprocessing image: {e}")
        return None

# OCR function to extract text from the image
def extract_text_from_image(image_path):
    try:
        img = preprocess_image(image_path)  # Preprocess the image
        if img is None:
            return "Error in preprocessing image."
        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(img)
        return text
    except UnidentifiedImageError:
        print("UnidentifiedImageError: Cannot identify image file. Please use a supported format (e.g., JPG, PNG).")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Define patterns to extract specific values (e.g., Hemoglobin, MCV)
def extract_values(text):
    patterns = {
        'Hemoglobin': r'Hemoglobin \(Hb\)\s+([\d.]+)',  
        'MCV': r'Mean Corpuscular Volume \(MCV\)\s+([\d.]+)',  
        'MCH': r'MCH\s+([\d.]+)',  
        'MCHC': r'MCHC\.\s+([\d.]+)',  
        'Gender': r'Sex\s+:\s+(\w+)'  
    }

    extracted_values = {}
    missing_values = []

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_values[key] = match.group(1)
        else:
            missing_values.append(key)

    return extracted_values, missing_values

# Function to preprocess extracted features (e.g., convert to appropriate types)
def preprocess_features(report_features):
    # Map 'Gender' to 0 for Male and 1 for Female
    gender_mapping = {'Male': 0, 'Female': 1}
    report_features['Gender'] = gender_mapping.get(report_features['Gender'], 0)  # Default to 0 if gender is unknown

    # Convert string values to float
    for key, value in report_features.items():
        if isinstance(value, str):
            try:
                report_features[key] = float(value)
            except ValueError:
                pass  # If it can't be converted, leave it as is

    # Reorder the dictionary to match the desired order
    ordered_keys = ['Gender', 'Hemoglobin', 'MCH', 'MCHC', 'MCV']
    ordered_report_features = {key: report_features[key] for key in ordered_keys if key in report_features}

    return list(ordered_report_features.values())

# Simulate predicting anemia using a dummy model (replace with your actual model)
def predict_anemia(preprocessed_values):
    # Dummy prediction logic (0 for no anemia, 1 for anemia)
    # Replace this with your actual model's prediction logic
    if len(preprocessed_values) == 5:
        return "Anemia detected \t താങ്കള്‍ക്ക് അനീമിയ ബാധിചിരുക്കുന്നു.", True
    else:
        return "No anemia detected \t താങ്കള്‍ക്ക് അനീമിയ ഇല്ല.", False

# Main pipeline function to handle the entire process
def anemia_prediction_pipeline(image_path):
    # Step 1: Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    
    if extracted_text is None:
        return "Error: Unable to extract text from the image.", None

    print(f"Extracted text:\n{extracted_text}")  # Debugging - print extracted text

    # Step 2: Extract required values from the text
    extracted_values, missing_values = extract_values(extracted_text)

    # Step 3: Handle missing values
    if missing_values:
        return "Missing data for prediction: " + ", ".join(missing_values), None

    print(f"Extracted values: {extracted_values}")  # Debugging - print extracted values

    # Step 4: Preprocess the extracted values
    preprocessed_values = preprocess_features(extracted_values)

    # Step 5: Use the model to predict anemia
    prediction_result, _ = predict_anemia(preprocessed_values)
    print('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
    print(prediction_result)

    return prediction_result, None

# Example usage
image_path = "C:/Users/visma/Downloads/IMG-20250201-WA0002.jpg"
result, _ = anemia_prediction_pipeline(image_path)
print(result)



