import hashlib

class ChecksumGenerator:
    @staticmethod
    def generate(file_path, method="sha256"):
        hash_func = hashlib.new(method)
        with open(file_path, "rb") as f:
            hash_func.update(f.read())
        return hash_func.hexdigest()
