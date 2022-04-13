import hashlib
import os

def find_md5_collision_and_print(target_prefix):
    max_iter = 1000000
    for _ in range(max_iter):
        random_binary = os.urandom(16) # 產生指定長度的隨機bytes, 長度from spec
        new_prefix = hashlib.md5(random_binary).hexdigest()[:4]

        if new_prefix == target_prefix:
            print(target_prefix, random_binary.hex())
            return

    print(f'Can\'t find collision in {max_iter} times try.')


if __name__ == "__main__":
    input_str = input()
    key = bytes.fromhex(input_str)  # 從hex字串轉bytes
    prefix_len = 4  # from spec

    md5 = hashlib.md5()
    md5.update(key) 
    target_prefix = md5.hexdigest()[:prefix_len]    # 取16進位的hash後的字串的前[prefix_len]位

    find_md5_collision_and_print(target_prefix)