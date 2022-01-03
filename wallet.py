from ecdsa import SigningKey


class Wallet:
    """
    The class for the wallet

    Attributes
    ----------
    private_key : SigningKey
        The private key of the wallet
    public_key : str
        The public key of the wallet
    """

    def __init__(self):
        self.private_key: SigningKey = None
        self.public_key: str = None

    @classmethod
    def from_private_key(cls, private_key: bytes) -> "Wallet":
        """
        Generates a wallet from a private key

        Parameters
        ----------
        private_key : bytes
            The private key of the wallet

        Returns
        -------
        Wallet
            The wallet generated from the private key
        """
        wallet = cls()
        wallet.private_key = SigningKey.from_pem(private_key)
        wallet.public_key = wallet.private_key.verifying_key.to_string().hex()
        return wallet

    @classmethod
    def generate(cls) -> "Wallet":
        """
        Generates a new wallet

        Returns
        -------
        Wallet
            The wallet generated
        """
        wallet = cls()
        wallet.private_key = SigningKey.generate()
        wallet.public_key = wallet.private_key.verifying_key.to_string().hex()
        return wallet
