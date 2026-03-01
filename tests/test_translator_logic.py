
import sys
from unittest.mock import MagicMock

# Mock speech_recognition to avoid dependency issues during test
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

# The DB and functions from the qmd file
SIGN_LANGUAGE_DB = {
    "안녕하세요": "assets/hello.mp4",
    "만나서": "assets/meet.mp4",
    "반갑습니다": "assets/glad.mp4",
    "감사합니다": "assets/thanks.mp4"
}

def play_sign_language_assets(asset_paths):
    for path in asset_paths:
        print(f"[재생 중] {path} ...")

def translate_to_sign_language(text):
    if not text:
        return
    print(f"'{text}' 문장을 수어로 변환 중...")
    words = text.split()
    matched_assets = [SIGN_LANGUAGE_DB[word] for word in words if word in SIGN_LANGUAGE_DB]
    if matched_assets:
        play_sign_language_assets(matched_assets)
    else:
        print("일치하는 수어 데이터를 찾을 수 없습니다.")

if __name__ == "__main__":
    print("--- Test 1: Known words ---")
    translate_to_sign_language("만나서 반갑습니다")

    print("\n--- Test 2: Unknown words ---")
    translate_to_sign_language("모르는 단어")

    print("\n--- Test 3: Mixed words ---")
    translate_to_sign_language("안녕하세요 친구")
