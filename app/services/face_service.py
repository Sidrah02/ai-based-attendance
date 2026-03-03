import io
import json
import numpy as np
import cv2

# DeepFace will be imported when the service starts if installed correctly
try:
    from deepface import DeepFace
except ImportError:
    DeepFace = None

class FaceRecognitionError(Exception):
    pass

def get_face_encoding(image_bytes: bytes) -> str:
    """
    Extracts the face encoding (embedding) from an image using DeepFace.
    Raises an error if no faces or multiple faces are found.
    Returns a JSON string of the encoding.
    """
    if DeepFace is None:
        raise FaceRecognitionError("DeepFace library is not correctly installed.")

    try:
        # Convert bytes to numpy array for OpenCV
        img_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            raise FaceRecognitionError("Could not decode image.")

        # Extract embeddings using DeepFace
        # enforce_detection=True will raise ValueError if no face is found
        results = DeepFace.represent(img_path=img, model_name="VGG-Face", enforce_detection=True)
        
        if len(results) == 0:
            raise FaceRecognitionError("No face found in the provided image.")
        if len(results) > 1:
            raise FaceRecognitionError("Multiple faces found in the provided image. Please provide a clear picture of just one person.")
            
        # Extract the representation vector (embedding)
        encoding = results[0]["embedding"]
        
        # Convert to JSON string
        return json.dumps(encoding)
        
    except ValueError as e:
        # DeepFace throws ValueError when no face is detected with enforce_detection=True
        raise FaceRecognitionError("No face could be clearly detected. Please ensure the face is visible and well-lit.")
    except Exception as e:
        if isinstance(e, FaceRecognitionError):
            raise
        raise FaceRecognitionError(f"Error processing image: {str(e)}")


def compare_face_to_known(unknown_encoding_json: str, known_encodings_dict: dict, threshold: float = 0.40) -> tuple:
    """
    Compares an unknown face encoding against a dictionary of {student_id: encoding_json}.
    Uses Cosine distance which is standard for VGG-Face (threshold ~0.40).
    Returns a tuple (best_match_student_id, confidence_score) or (None, 0.0)
    """
    try:
        # Convert unknown encoding
        unknown_encoding = np.array(json.loads(unknown_encoding_json))
        unknown_norm = np.linalg.norm(unknown_encoding)
        
        best_match_id = None
        best_distance = float('inf')
        
        for student_id, encoding_json in known_encodings_dict.items():
            if not encoding_json:
                continue
                
            known_encoding = np.array(json.loads(encoding_json))
            known_norm = np.linalg.norm(known_encoding)
            
            # Cosine distance: 1 - cosine_similarity
            cos_sim = np.dot(known_encoding, unknown_encoding) / (known_norm * unknown_norm)
            distance = 1.0 - cos_sim
            
            if distance < best_distance:
                best_distance = distance
                best_match_id = student_id
                
        # If the best distance is below our threshold, it's a match
        if best_match_id is not None and best_distance <= threshold:
            # Confidence score can be inversely proportional to distance
            confidence_score = max(0.0, 1.0 - (best_distance / threshold))
            return best_match_id, confidence_score
            
        return None, 0.0
        
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return None, 0.0
