from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from EntropyCounter import count_entropy_of_bytes

initialization_block = get_random_bytes(16)
key = b'key4567890123456'

files = ["resources/greenland_grid_velo.bmp", "resources/demo24.bmp"]
for file_to_open in files:
    print("For file " + file_to_open + ":")
    file = open(file_to_open, "rb")
    img_bytes = bytearray(file.read())
    header = img_bytes[:53]
    #header_entropy = count_entropy_of_bytes(header)
    #print(f"Header entropy no encryption: {header_entropy}")
    body = img_bytes[54:]
    print(f'Unencrypted entropy = {count_entropy_of_bytes(img_bytes)}')
    file.close()

    diff = 32 - (len(img_bytes) % 32)
    padding = bytearray(b'0' * diff)

    img_bytes.extend(padding)

    ecb = AES.new(key, AES.MODE_ECB)
    cbc = AES.new(key, AES.MODE_CBC, initialization_block)

    encrypted_ecb_no_header = ecb.encrypt(body + bytearray(b'0' * (32 - (len(body) % 32))))
    encrypted_cbc_no_header = cbc.encrypt(body + bytearray(b'0' * (32 - (len(body) % 32))))

    full_ecb = header + encrypted_ecb_no_header
    full_cbc = header + encrypted_cbc_no_header

    ecb_entropy_no_header = count_entropy_of_bytes(full_ecb)
    cbc_entropy_no_header = count_entropy_of_bytes(full_cbc)

    print(f'ECB entropy without encrypting header = {ecb_entropy_no_header}')
    print(f'CBC entropy without encrypting header = {cbc_entropy_no_header}')

    ecb = AES.new(key, AES.MODE_ECB)
    cbc = AES.new(key, AES.MODE_CBC, initialization_block)

    encrypted_ecb = ecb.encrypt(img_bytes)
    encrypted_cbc = cbc.encrypt(img_bytes)

    ecb_entropy = count_entropy_of_bytes(encrypted_ecb)
    cbc_entropy = count_entropy_of_bytes(encrypted_cbc)

    print(f'ECB entropy = {ecb_entropy}')
    print(f'CBC entropy = {cbc_entropy}')

    f = open("outputs/ecb" + file_to_open.replace("resources/", "-"), 'wb')
    f.write(full_ecb)
    f.close()
    f = open("outputs/ccb" + file_to_open.replace("resources/", "-"), 'wb')
    f.write(full_cbc)
    f.close()
    print("-----------------")

