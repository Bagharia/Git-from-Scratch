import os
import zlib

def decode_content(content):
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        pass
    
    if content.startswith(b'\xff\xfe'):
        try:
            return content.decode('utf-16-le')
        except UnicodeDecodeError:
            pass
    elif content.startswith(b'\xfe\xff'):
        try:
            return content.decode('utf-16-be')
        except UnicodeDecodeError:
            pass
    
    try:
        return content.decode('utf-16')
    except UnicodeDecodeError:
        pass
    
    try:
        return content.decode('latin1')
    except UnicodeDecodeError:
        pass
    
    return None

def cat_file(sha):
    dir_path = os.path.join(".ggit", "objects", sha[:2])
    file_path = os.path.join(dir_path, sha[2:])
    
    if not os.path.exists(file_path):
        print(f"fatal: object {sha} not found")
        return

    with open(file_path, "rb") as f:
        compressed_data = f.read()

    data = zlib.decompress(compressed_data)
    null_index = data.find(b'\x00')
    header = data[:null_index]
    content = data[null_index+1:]

    if not header.startswith(b"blob"):
        print(f"fatal: object {sha} is not a blob")
        return

    decoded = decode_content(content)
    if decoded is not None:
        print(decoded)
    else:
        print("Content is not valid UTF-8/UTF-16/latin1, printing raw bytes:")
        print(content)
