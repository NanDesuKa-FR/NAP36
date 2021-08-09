# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Signature\pss.py
from Cryptodome.Util.py3compat import bchr, bord, iter_range
import Cryptodome.Util.number
from Cryptodome.Util.number import ceil_div, long_to_bytes, bytes_to_long
from Cryptodome.Util.strxor import strxor
from Cryptodome import Random

class PSS_SigScheme:
    __doc__ = 'A signature object for ``RSASSA-PSS``.\n    Do not instantiate directly.\n    Use :func:`Cryptodome.Signature.pss.new`.\n    '

    def __init__(self, key, mgfunc, saltLen, randfunc):
        """Initialize this PKCS#1 PSS signature scheme object.

        :Parameters:
          key : an RSA key object
            If a private half is given, both signature and
            verification are possible.
            If a public half is given, only verification is possible.
          mgfunc : callable
            A mask generation function that accepts two parameters:
            a string to use as seed, and the lenth of the mask to
            generate, in bytes.
          saltLen : integer
            Length of the salt, in bytes.
          randfunc : callable
            A function that returns random bytes.
        """
        self._key = key
        self._saltLen = saltLen
        self._mgfunc = mgfunc
        self._randfunc = randfunc

    def can_sign(self):
        """Return ``True`` if this object can be used to sign messages."""
        return self._key.has_private()

    def sign(self, msg_hash):
        """Create the PKCS#1 PSS signature of a message.

        This function is also called ``RSASSA-PSS-SIGN`` and
        it is specified in
        `section 8.1.1 of RFC8017 <https://tools.ietf.org/html/rfc8017#section-8.1.1>`_.

        :parameter msg_hash:
            This is an object from the :mod:`Cryptodome.Hash` package.
            It has been used to digest the message to sign.
        :type msg_hash: hash object

        :return: the signature encoded as a *byte string*.
        :raise ValueError: if the RSA key is not long enough for the given hash algorithm.
        :raise TypeError: if the RSA key has no private half.
        """
        if self._saltLen is None:
            sLen = msg_hash.digest_size
        else:
            sLen = self._saltLen
        if self._mgfunc is None:
            mgf = lambda x, y: MGF1(x, y, msg_hash)
        else:
            mgf = self._mgfunc
        modBits = Cryptodome.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        em = _EMSA_PSS_ENCODE(msg_hash, modBits - 1, self._randfunc, mgf, sLen)
        em_int = bytes_to_long(em)
        m_int = self._key._decrypt(em_int)
        signature = long_to_bytes(m_int, k)
        return signature

    def verify(self, msg_hash, signature):
        """Check if the  PKCS#1 PSS signature over a message is valid.

        This function is also called ``RSASSA-PSS-VERIFY`` and
        it is specified in
        `section 8.1.2 of RFC8037 <https://tools.ietf.org/html/rfc8017#section-8.1.2>`_.

        :parameter msg_hash:
            The hash that was carried out over the message. This is an object
            belonging to the :mod:`Cryptodome.Hash` module.
        :type parameter: hash object

        :parameter signature:
            The signature that needs to be validated.
        :type signature: bytes

        :raise ValueError: if the signature is not valid.
        """
        if self._saltLen is None:
            sLen = msg_hash.digest_size
        else:
            sLen = self._saltLen
        if self._mgfunc:
            mgf = self._mgfunc
        else:
            mgf = lambda x, y: MGF1(x, y, msg_hash)
        modBits = Cryptodome.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)
        if len(signature) != k:
            raise ValueError('Incorrect signature')
        signature_int = bytes_to_long(signature)
        em_int = self._key._encrypt(signature_int)
        emLen = ceil_div(modBits - 1, 8)
        em = long_to_bytes(em_int, emLen)
        _EMSA_PSS_VERIFY(msg_hash, em, modBits - 1, mgf, sLen)


def MGF1(mgfSeed, maskLen, hash_gen):
    """Mask Generation Function, described in `B.2.1 of RFC8017
    <https://tools.ietf.org/html/rfc8017>`_.

    :param mfgSeed:
        seed from which the mask is generated
    :type mfgSeed: byte string

    :param maskLen:
        intended length in bytes of the mask
    :type maskLen: integer

    :param hash_gen:
        A module or a hash object from :mod:`Cryptodome.Hash`
    :type hash_object:

    :return: the mask, as a *byte string*
    """
    T = b''
    for counter in iter_range(ceil_div(maskLen, hash_gen.digest_size)):
        c = long_to_bytes(counter, 4)
        hobj = hash_gen.new()
        hobj.update(mgfSeed + c)
        T = T + hobj.digest()

    assert len(T) >= maskLen
    return T[:maskLen]


def _EMSA_PSS_ENCODE(mhash, emBits, randFunc, mgf, sLen):
    r"""
    Implement the ``EMSA-PSS-ENCODE`` function, as defined
    in PKCS#1 v2.1 (RFC3447, 9.1.1).

    The original ``EMSA-PSS-ENCODE`` actually accepts the message ``M``
    as input, and hash it internally. Here, we expect that the message
    has already been hashed instead.

    :Parameters:
      mhash : hash object
        The hash object that holds the digest of the message being signed.
      emBits : int
        Maximum length of the final encoding, in bits.
      randFunc : callable
        An RNG function that accepts as only parameter an int, and returns
        a string of random bytes, to be used as salt.
      mgf : callable
        A mask generation function that accepts two parameters: a string to
        use as seed, and the lenth of the mask to generate, in bytes.
      sLen : int
        Length of the salt, in bytes.

    :Return: An ``emLen`` byte long string that encodes the hash
      (with ``emLen = \ceil(emBits/8)``).

    :Raise ValueError:
        When digest or salt length are too big.
    """
    emLen = ceil_div(emBits, 8)
    lmask = 0
    for i in iter_range(8 * emLen - emBits):
        lmask = lmask >> 1 | 128

    if emLen < mhash.digest_size + sLen + 2:
        raise ValueError('Digest or salt length are too long for given key size.')
    salt = randFunc(sLen)
    m_prime = bchr(0) * 8 + mhash.digest() + salt
    h = mhash.new()
    h.update(m_prime)
    ps = bchr(0) * (emLen - sLen - mhash.digest_size - 2)
    db = ps + bchr(1) + salt
    dbMask = mgf(h.digest(), emLen - mhash.digest_size - 1)
    maskedDB = strxor(db, dbMask)
    maskedDB = bchr(bord(maskedDB[0]) & ~lmask) + maskedDB[1:]
    em = maskedDB + h.digest() + bchr(188)
    return em


def _EMSA_PSS_VERIFY(mhash, em, emBits, mgf, sLen):
    """
    Implement the ``EMSA-PSS-VERIFY`` function, as defined
    in PKCS#1 v2.1 (RFC3447, 9.1.2).

    ``EMSA-PSS-VERIFY`` actually accepts the message ``M`` as input,
    and hash it internally. Here, we expect that the message has already
    been hashed instead.

    :Parameters:
      mhash : hash object
        The hash object that holds the digest of the message to be verified.
      em : string
        The signature to verify, therefore proving that the sender really
        signed the message that was received.
      emBits : int
        Length of the final encoding (em), in bits.
      mgf : callable
        A mask generation function that accepts two parameters: a string to
        use as seed, and the lenth of the mask to generate, in bytes.
      sLen : int
        Length of the salt, in bytes.

    :Raise ValueError:
        When the encoding is inconsistent, or the digest or salt lengths
        are too big.
    """
    emLen = ceil_div(emBits, 8)
    lmask = 0
    for i in iter_range(8 * emLen - emBits):
        lmask = lmask >> 1 | 128

    if emLen < mhash.digest_size + sLen + 2:
        raise ValueError('Incorrect signature')
    if ord(em[-1:]) != 188:
        raise ValueError('Incorrect signature')
    maskedDB = em[:emLen - mhash.digest_size - 1]
    h = em[emLen - mhash.digest_size - 1:-1]
    if lmask & bord(em[0]):
        raise ValueError('Incorrect signature')
    else:
        dbMask = mgf(h, emLen - mhash.digest_size - 1)
        db = strxor(maskedDB, dbMask)
        db = bchr(bord(db[0]) & ~lmask) + db[1:]
        if not db.startswith(bchr(0) * (emLen - mhash.digest_size - sLen - 2) + bchr(1)):
            raise ValueError('Incorrect signature')
        if sLen > 0:
            salt = db[-sLen:]
        else:
            salt = b''
    m_prime = bchr(0) * 8 + mhash.digest() + salt
    hobj = mhash.new()
    hobj.update(m_prime)
    hp = hobj.digest()
    if h != hp:
        raise ValueError('Incorrect signature')


def new(rsa_key, **kwargs):
    """Create an object for making or verifying PKCS#1 PSS signatures.

    :parameter rsa_key:
      The RSA key to use for signing or verifying the message.
      This is a :class:`Cryptodome.PublicKey.RSA` object.
      Signing is only possible when ``rsa_key`` is a **private** RSA key.
    :type rsa_key: RSA object

    :Keyword Arguments:

        *   *mask_func* (``callable``) --
            A mask generation function that accepts two parameters: ``bytes`` to
            use as seed, and the amount of ``bytes`` to return (i.e. the mask).
            If not specified, the standard :func:`MGF1` function is used,
            based on the same hash algorithm applied to the message.

        *   *salt_bytes* (``integer``) --
            Length of the salt, in bytes.
            If not specified, it matches the digest of the hash algorithm
            applied to the message.
            If zero, the signature scheme becomes deterministic.

        *   *rand_func* (``callable``) --
            A function that returns random ``bytes``, of the desired length.
            The default is :func:`Cryptodome.Random.get_random_bytes`.

    :return: a :class:`PSS_SigScheme` signature object
    """
    mask_func = kwargs.pop('mask_func', None)
    salt_len = kwargs.pop('salt_bytes', None)
    rand_func = kwargs.pop('rand_func', None)
    if rand_func is None:
        rand_func = Random.get_random_bytes
    if kwargs:
        raise ValueError('Unknown keywords: ' + str(kwargs.keys()))
    return PSS_SigScheme(rsa_key, mask_func, salt_len, rand_func)