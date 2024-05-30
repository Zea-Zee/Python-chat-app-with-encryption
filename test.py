import unittest
from p2p_chat import encoder, decoder


class TestEncoderDecoder(unittest.TestCase):

    def test_encode_decode(self):
        test_strings = [
            "Hello, World!",
            "This is a test string.",
            "Another example with numbers 12345",
            "!@#$%^&*()_+-=[]{};':\",.<>/?",
            "",
            " ",
            "\033[94m"
        ]

        for test_string in test_strings:
            with self.subTest(test_string=test_string):
                encoded = encoder(test_string)
                decoded = decoder(encoded)
                self.assertEqual(decoded, test_string, f"Failed for string: {test_string}")

    def test_decode_empty_string(self):
        self.assertEqual(decoder(""), "", "Empty string decoding failed")

    def test_encode_single_character(self):
        self.assertEqual(decoder(encoder("A")), "A", "Single character encoding failed")
        
    def test_encode_color_test(self):
        self.assertEqual(decoder(encoder("\033[94m")), "\033[94m", "Color test failed")

    def test_decode_corrupted_data(self):
        original_string = "Corrupted data example"
        encoded = encoder(original_string)
        # Introduce a single-bit error
        corrupted = list(encoded)
        corrupted[0] = '1' if corrupted[0] == '0' else '0'
        corrupted_encoded = ''.join(corrupted)
        decoded = decoder(corrupted_encoded)
        self.assertEqual(decoded, original_string, "Decoding failed to correct a single-bit error")

if __name__ == '__main__':
    unittest.main()
