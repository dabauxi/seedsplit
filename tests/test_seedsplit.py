import pytest
from click import BadArgumentUsage
from shamir_mnemonic import MnemonicError

from seedsplit.__main__ import _recover, _split

seed = (
    "island rich ghost moral city vital ignore plastic slab drift surprise "
    "grid idea distance regret gospel page across bird obscure copy either vessel jeans"
)

seed_12_words = (
    "island rich ghost moral city vital ignore plastic slab drift surprise grid"
)

seed_no_valid_language = (
    "witch collapse practice feed shame open despair creek road again ice least"
)


def _split_recover(seed_phrase: str):
    mnemonics = _split(
        mnemonic=seed_phrase,
        required_parts=4,
        overall_parts=5,
        passphrase="secretphrase",
    )
    recover_mnemonics = ",".join(mnemonics[0][:4])
    return _recover(recover_mnemonics, "secretphrase")


def test_split_and_recover_mnemonic():
    assert seed == _split_recover(seed)


def test_split_and_recover_mnemonic_12_words():
    assert seed_12_words == _split_recover(seed_12_words)


def test_split_and_recover_wrong_bip_language():
    with pytest.raises(BadArgumentUsage):
        _split_recover(seed_no_valid_language)


def test_split_recover_missing_shard():
    mnemonics = _split(
        mnemonic=seed, required_parts=4, overall_parts=5, passphrase="secretphrase"
    )
    # one shard missing
    recover_mnemonics = ",".join(mnemonics[0][:3])
    with pytest.raises(MnemonicError):
        _recover(recover_mnemonics.strip(), "secretphrase")
