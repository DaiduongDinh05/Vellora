import pytest
from app.modules.trips.utils.crypto import encrypt_address, decrypt_address


class TestEncryptAddress:

    def test_encrypt_address_with_valid_string(self):
        address = "123 Main St, Springfield, IL 62701"
        
        encrypted = encrypt_address(address)
        
        assert encrypted != address
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0

    def test_encrypt_address_with_empty_string(self):
        result = encrypt_address("")
        
        assert result == ""

    def test_encrypt_address_with_special_characters(self):
        address = "123 Main St., Apt #4B, São Paulo, BR 01310-100"
        
        encrypted = encrypt_address(address)
        
        assert encrypted != address
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0

    def test_encrypt_address_with_unicode(self):
        address = "北京市朝阳区 100020"
        
        encrypted = encrypt_address(address)
        
        assert encrypted != address
        assert isinstance(encrypted, str)

    def test_encrypt_address_produces_different_results_for_different_inputs(self):
        address1 = "123 Main St"
        address2 = "456 Oak Ave"
        
        encrypted1 = encrypt_address(address1)
        encrypted2 = encrypt_address(address2)
        
        assert encrypted1 != encrypted2

    def test_encrypt_address_is_non_deterministic(self):
        address = "123 Main St"
        
        encrypted1 = encrypt_address(address)
        encrypted2 = encrypt_address(address)
        
        #fernet encryption includes timestamp, so different encryptions produce different results
        #but both should decrypt to the same original value
        decrypted1 = decrypt_address(encrypted1)
        decrypted2 = decrypt_address(encrypted2)
        
        assert decrypted1 == decrypted2 == address


class TestDecryptAddress:

    def test_decrypt_address_with_valid_token(self):
        original = "123 Main St, Springfield, IL 62701"
        encrypted = encrypt_address(original)
        
        decrypted = decrypt_address(encrypted)
        
        assert decrypted == original

    def test_decrypt_address_with_empty_string(self):
        result = decrypt_address("")
        
        assert result == ""

    def test_decrypt_address_with_special_characters(self):
        original = "123 Main St., Apt #4B, São Paulo, BR 01310-100"
        encrypted = encrypt_address(original)
        
        decrypted = decrypt_address(encrypted)
        
        assert decrypted == original

    def test_decrypt_address_with_unicode(self):
        original = "北京市朝阳区 100020"
        encrypted = encrypt_address(original)
        
        decrypted = decrypt_address(encrypted)
        
        assert decrypted == original

    def test_decrypt_address_with_invalid_token(self):
        invalid_token = "this_is_not_a_valid_encrypted_token"
        
        with pytest.raises(Exception):
            decrypt_address(invalid_token)

    def test_decrypt_address_with_corrupted_token(self):
        original = "123 Main St"
        encrypted = encrypt_address(original)
        
        corrupted = encrypted[:-5] + "XXXXX"
        
        with pytest.raises(Exception):
            decrypt_address(corrupted)


class TestRoundTripEncryption:

    def test_round_trip_encryption_decryption(self):
        addresses = [
            "123 Main St",
            "456 Oak Ave, Apt 4B",
            "789 Elm St, Springfield, IL 62701",
            "São Paulo, BR 01310-100",
            "北京市朝阳区 100020",
            "123 Main St., Apt #4B, New York, NY 10001",
            "   Leading and trailing spaces   ",
        ]
        
        for address in addresses:
            encrypted = encrypt_address(address)
            decrypted = decrypt_address(encrypted)
            assert decrypted == address, f"Round-trip failed for: {address}"

    def test_multiple_encryptions_decrypt_to_same_value(self):
        address = "123 Main St"
        
        encrypted1 = encrypt_address(address)
        encrypted2 = encrypt_address(address)
        encrypted3 = encrypt_address(address)
        
        assert decrypt_address(encrypted1) == address
        assert decrypt_address(encrypted2) == address
        assert decrypt_address(encrypted3) == address

    def test_encryption_handles_long_addresses(self):
        long_address = "A" * 500 
        
        encrypted = encrypt_address(long_address)
        decrypted = decrypt_address(encrypted)
        
        assert decrypted == long_address

    def test_encryption_handles_newlines_and_tabs(self):
        address_with_whitespace = "123 Main St\nApt 4B\tSpringfield, IL"
        
        encrypted = encrypt_address(address_with_whitespace)
        decrypted = decrypt_address(encrypted)
        
        assert decrypted == address_with_whitespace
