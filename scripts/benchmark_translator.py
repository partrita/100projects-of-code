
import timeit
import sys
from unittest.mock import MagicMock

# Mock speech_recognition
mock_sr = MagicMock()
sys.modules['speech_recognition'] = mock_sr

SIGN_LANGUAGE_DB = {
    f"word_{i}": f"assets/asset_{i}.mp4" for i in range(10000)
}

def translate_original(text):
    words = text.split()
    matched_assets = [SIGN_LANGUAGE_DB[word] for word in words if word in SIGN_LANGUAGE_DB]
    return matched_assets

def translate_optimized(text):
    words = text.split()
    matched_assets = [v for word in words if (v := SIGN_LANGUAGE_DB.get(word)) is not None]
    return matched_assets

# Test with a very long text to amplify differences
test_words = [f"word_{i % 10000}" if i % 2 == 0 else f"unknown_{i}" for i in range(10000)]
test_text = " ".join(test_words)

def benchmark():
    # Warm up
    translate_original(test_text)
    translate_optimized(test_text)

    number = 5000
    original_time = timeit.timeit(lambda: translate_original(test_text), number=number)
    optimized_time = timeit.timeit(lambda: translate_optimized(test_text), number=number)

    print(f"Iterations: {number}")
    print(f"Original time: {original_time:.4f}s")
    print(f"Optimized time: {optimized_time:.4f}s")
    improvement = (original_time - optimized_time) / original_time * 100
    print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    benchmark()
