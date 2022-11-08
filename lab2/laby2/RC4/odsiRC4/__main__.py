import typer
from .RC4 import RC4
from .BruteForce import BruteForce
app = typer.Typer(help="For information on specific command, please use :\n\npython3 odsiRC4 <command> --help\n\n")
algorithm = RC4()


@app.command()
def encrypt(key: str, text: str):
    """
    Encrypts given <text> using given <key> with RC4 algorithm.

    Usage:


    python3 odsiRC4 encrypt "<key in quotation marks>" "<Text in mandatory quotation marks>"
    """
    encrypted = algorithm.encrypt(key, text)
    encrypted_str = ''.join(list(map(chr, encrypted)))
    print(f"Decimal values of encrypted text: {encrypted}")
    print(f"Characters: {list(map(chr, encrypted))}")
    print(f"String: {encrypted_str}")


@app.command()
def decrypt(key: str, text: str):
    """
        Decrypts given <text> using given <key> with RC4 algorithm.

        Usage:


        python3 odsiRC4 decrypt "<key in quotation marks>" "<Encrypted text in quotation marks>"
    """
    decrypted = algorithm.decrypt(key, text)
    decrypted_str = ''.join(list(map(chr, decrypted)))
    print(f"Decimal values of encrypted text: {decrypted}")
    print(f"Characters: {list(map(chr, decrypted))}")
    print(f"String: {decrypted_str}")


@app.command()
def get_key_stream(key: str):
    """
           Creates key stream using given <key> with RC4 algorithm.

           Usage:


           python3 odsiRC4 get-key-stream "<key in quotation marks>"
    """
    key_stream = algorithm.__generate_key_stream__(key)
    stringified_key = ''.join(list(map(chr, key_stream)))
    print(f"Generated key stream in string: {stringified_key}\n\n")
    print(f"Generated key stream: {key_stream}")

if __name__ == "__main__":
    app()
