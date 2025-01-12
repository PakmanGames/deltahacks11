import face_recognition as frg
import pickle as pkl
import os
import cv2
import numpy as np
import yaml
from collections import defaultdict
from typing import Tuple, Dict, Any, Optional

from typing import List

class FaceDatabase:
    def __init__(self, config_path: str = 'config.yaml'):
        self.cfg = yaml.load(open(config_path, 'r'), Loader=yaml.FullLoader)
        self.dataset_dir = self.cfg['PATH']['DATASET_DIR']
        self.pkl_path = self.cfg['PATH']['PKL_PATH']
        
    def load(self) -> Dict:
        with open(self.pkl_path, 'rb') as f:
            return pkl.load(f)
            
    def save(self, data: Dict) -> None:
        with open(self.pkl_path, 'wb') as f:
            pkl.dump(data, f)

class FaceRecognition:
    def __init__(self, database: FaceDatabase):
        self.db = database
        
    def detect_faces(self, image: np.ndarray) -> bool:
        return len(frg.face_locations(image)) > 0
        
    def encode_face(self, image: np.ndarray) -> np.ndarray:
        return frg.face_encodings(image)[0]
        
    def recognize(self, image: np.ndarray, tolerance: float) -> Tuple[np.ndarray, str, str]:
        database = self.db.load()
        known_encodings = [database[id]['encoding'] for id in database.keys()]
        
        face_locations = frg.face_locations(image)
        face_encodings = frg.face_encodings(image, face_locations)
        
        name = id_val = 'Unknown'
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = frg.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
            distances = frg.face_distance(known_encodings, face_encoding)
            
            if True in matches:
                match_idx = matches.index(True)
                name = database[match_idx]['name']
                id_val = database[match_idx]['id']
                distance = round(distances[match_idx], 2)
                cv2.putText(image, str(distance), (left, top-30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
                
            cv2.rectangle(image, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(image, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
            
        return image, name, id_val

class FaceManager:
    def __init__(self):
        self.db = FaceDatabase()
        self.recognizer = FaceRecognition(self.db)
        
    def submit_new(self, name: str, id_val: str, image: Any, old_idx: Optional[int] = None) -> int:
        database = self.db.load()
        
        if isinstance(image, bytes):
            image = cv2.imdecode(np.fromstring(image.read(), np.uint8), 1)
            
        if not self.recognizer.detect_faces(image):
            return -1
            
        encoding = self.recognizer.encode_face(image)
        existing_ids = [database[i]['id'] for i in database.keys()]
        
        new_idx = old_idx if old_idx is not None else len(database)
        
        if old_idx is None and id_val in existing_ids:
            return 0
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        database[new_idx] = {
            'image': image,
            'id': id_val,
            'name': name,
            'encoding': encoding
        }
        
        self.db.save(database)
        return True
        
    def get_info(self, id_val: str) -> Tuple[Optional[str], Optional[np.ndarray], Optional[int]]:
        database = self.db.load()
        for idx, person in database.items():
            if person['id'] == id_val:
                return person['name'], person['image'], idx
        return None, None, None

    def get_all_info(self) -> List[Tuple[str, np.ndarray, str]]:
        database = self.db.load()
        contacts = []
        for idx, person in database.items():
            contacts.append((person['name'], person['image'], person['id']))
        return contacts
        
    def delete_one(self, id_val: str) -> bool:
        database = self.db.load()
        for key, person in database.items():
            if person['id'] == str(id_val):
                del database[key]
                self.db.save(database)
                return True
        return False
        
    def build_dataset(self) -> None:
        information = defaultdict(dict)
        counter = 0
        
        for image in os.listdir(self.db.dataset_dir):
            if not image.endswith('.jpg'):
                continue
                
            image_path = os.path.join(self.db.dataset_dir, image)
            image_name = image.split('.')[0]
            parsed_name = image_name.split('_')
            person_id = parsed_name[0]
            person_name = ' '.join(parsed_name[1:])
            
            face_image = frg.load_image_file(image_path)
            information[counter].update({
                'image': face_image,
                'id': person_id,
                'name': person_name,
                'encoding': self.recognizer.encode_face(face_image)
            })
            counter += 1
            
        with open(os.path.join(self.db.dataset_dir, 'database.pkl'), 'wb') as f:
            pkl.dump(information, f)

# Maintain original interface
face_manager = FaceManager()
get_databse = face_manager.db.load
recognize = face_manager.recognizer.recognize
isFaceExists = face_manager.recognizer.detect_faces
submitNew = face_manager.submit_new
get_info_from_id = face_manager.get_info
get_all_info = face_manager.get_all_info
deleteOne = face_manager.delete_one
build_dataset = face_manager.build_dataset

if __name__ == "__main__":
    deleteOne(4)