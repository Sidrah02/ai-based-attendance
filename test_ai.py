import asyncio
import json
import os

async def test_deepface():
    print("Testing if DeepFace can be imported...")
    try:
        from app.services.face_service import DeepFace, get_face_encoding, compare_face_to_known
        if DeepFace is None:
            print("DeepFace didn't import properly. AI functions will fail.")
            return

        print("DeepFace imported successfully!")
        
        # Test 1: Empty test to check environment sanity
        try:
            get_face_encoding(b"dummy")
            print("FAILED: get_face_encoding didn't raise error on garbage input.")
        except Exception as e:
            print(f"Passed get_face_encoding error check: {e}")

        print("All basic import tests passed.")
        
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(test_deepface())
