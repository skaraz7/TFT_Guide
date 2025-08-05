import requests
import json
import os
from typing import Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore

URL = "https://data.metatft.com/lookups/TFTSet15_latest_en_us.json"

def fetch_tft_data() -> Dict[str, Any]:
    """Fetch TFT Set 15 data from MetaTFT API"""
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

def parse_champions(data: Dict[str, Any]) -> list:
    """Parse champions from raw data"""
    champions = []
    for unit in data.get("units", []):
        if unit.get("characterName"):
            champions.append({
                "apiName": unit["apiName"],
                "name": unit.get("name"),
                "cost": unit.get("cost"),
                "traits": unit.get("traits", []),
                "ability": unit.get("ability", {}),
            })
    return champions

def parse_items(data: Dict[str, Any]) -> list:
    """Parse items from raw data"""
    items = []
    for item in data.get("items", []):
        items.append({
            "apiName": item["apiName"],
            "name": item.get("name"),
            "desc": item.get("desc", ""),
            "composition": item.get("composition", []),
            "effects": item.get("effects", {}),
        })
    return items

def parse_traits(data: Dict[str, Any]) -> list:
    """Parse traits from raw data"""
    traits = []
    for trait in data.get("traits", []):
        traits.append({
            "apiName": trait["apiName"],
            "name": trait.get("name"),
            "desc": trait.get("desc", ""),
            "effects": trait.get("effects", []),
        })
    return traits

def parse_augments(data: Dict[str, Any]) -> list:
    """Parse augments from raw data"""
    augments = []
    for aug in data.get("augments", []):
        augments.append({
            "apiName": aug["apiName"],
            "name": aug.get("name"),
            "desc": aug.get("desc", ""),
            "tier": aug.get("tier"),
        })
    return augments

def init_firebase():
    """Initialize Firebase connection"""
    if not firebase_admin._apps:
        firebase_key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "firebase-key.json")
        cred = credentials.Certificate(firebase_key_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://tft-metapro-default-rtdb.firebaseio.com/',
            'projectId': 'tft-metapro'
        })
    return firestore.client(database_id='tftset15')

def upload_to_firebase(data: Dict[str, Any]):
    """Upload parsed data to Firebase Firestore"""
    try:
        db = init_firebase()
        
        # Upload each category
        for category, items in data.items():
            collection_ref = db.collection(category)
            
            # Clear existing data (skip if collection doesn't exist)
            try:
                docs = collection_ref.limit(1).stream()
                for doc in docs:
                    # Collection exists, clear it
                    batch = db.batch()
                    docs_to_delete = collection_ref.stream()
                    for doc in docs_to_delete:
                        batch.delete(doc.reference)
                    batch.commit()
                    break
            except:
                pass  # Collection doesn't exist yet
            
            # Upload new data
            for item in items:
                collection_ref.add(item)
            
            print(f"Uploaded {len(items)} {category} to Firebase")
            
    except Exception as e:
        print(f"Error uploading to Firebase: {e}")
        print("Tip: Enable Firestore API at: https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=tft-metapro")
        return False
    return True

def save_parsed_data(use_firebase=False):
    """Fetch and save all parsed TFT data"""
    print("Fetching TFT Set 15 data...")
    raw_data = fetch_tft_data()
    
    parsed_data = {
        "champions": parse_champions(raw_data),
        "items": parse_items(raw_data),
        "traits": parse_traits(raw_data),
        "augments": parse_augments(raw_data),
    }
    
    # Save to JSON
    with open("tft_set15_parsed.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved: {len(parsed_data['champions'])} champions, {len(parsed_data['items'])} items, {len(parsed_data['traits'])} traits, {len(parsed_data['augments'])} augments")
    
    # Upload to Firebase if requested
    if use_firebase:
        success = upload_to_firebase(parsed_data)
        if not success:
            print("Firebase upload failed, but JSON file was created successfully.")

if __name__ == "__main__":
    # Subir datos a la base de datos 'tftset15'
    save_parsed_data(use_firebase=True)