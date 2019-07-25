from pathlib import Path

import pgpy


def decrypt_message(message, private_key_file_path: Path, private_key_passphrase: str) -> str:
    our_key, _ = pgpy.PGPKey.from_file(private_key_file_path)
    with our_key.unlock(private_key_passphrase):
        encrypted_text_message = pgpy.PGPMessage.from_blob(message)
        decrypted_message = our_key.decrypt(encrypted_text_message)

        return decrypted_message.message
