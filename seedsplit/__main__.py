from typing import List

import click
from bip_utils import Bip39ChecksumError, Bip39MnemonicGenerator, Bip39MnemonicValidator
from shamir_mnemonic import Share, generate_mnemonics
from shamir_mnemonic.recovery import RecoveryState


@click.group()
def cli() -> None:
    pass


def print_error_msg(msg, command) -> None:
    click.echo(msg, err=True)
    print_help_msg(command)


def print_help_msg(command) -> None:
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))


def _split(
    mnemonic: str, required_parts: int, overall_parts: int, passphrase: str
) -> List[List[str]]:
    if not mnemonic:
        raise click.BadArgumentUsage("Please provide a mnemonic to split")
    if not passphrase:
        raise click.BadArgumentUsage("Please provide a passphrase.")
    validator = Bip39MnemonicValidator(mnemonic.strip('"').strip("'"))
    try:
        entropy = validator.GetEntropy()
    except (ValueError, Bip39ChecksumError):
        raise click.BadArgumentUsage("No valid mnemonic.")
    if not entropy:
        raise click.BadArgumentUsage("Could not split mnemonic.")
    return generate_mnemonics(
        group_threshold=1,
        groups=[(required_parts, overall_parts)],
        master_secret=entropy,
        passphrase=str.encode(passphrase),
        iteration_exponent=1,
    )


@cli.command()
@click.option(
    "-m",
    "--mnemonic",
    default=None,
    help="Mnemonic to split e.g. 'island rich ghost moral city vital ignore ...'.",
)
@click.option(
    "--required_parts",
    default=2,
    help="Required seed parts to recover master seed phrase.",
)
@click.option("--overall_parts", default=3, help="Overall number of parts to split.")
@click.option(
    "-p", "--passphrase", default=None, help="Passphrase to unlock master seed."
)
def split(
    mnemonic: str,
    required_parts: int,
    overall_parts: int,
    passphrase: str,
) -> None:
    if required_parts < 2 or overall_parts < required_parts:
        click.echo("Please provider valid split parts")
        click.echo("Required parts have to be more than 1.")
        click.echo("Overall parts have to be more than required parts.")
        print_help_msg(split)
        exit(1)
    mnemonics = _split(mnemonic, required_parts, overall_parts, passphrase)
    for i, mnemonic in enumerate(mnemonics[0]):
        click.echo(f"\nSeed part [{i}]:")
        click.echo(mnemonic)
    click.echo("\nSuccessfully splitted seed!")


def _recover(mnemonics: str, passphrase: str) -> str:
    recovery_state = RecoveryState()
    mnemonic_parts = []
    if mnemonics:
        mnemonic_parts = mnemonics.strip('"').strip("'").split(",")
    for part in mnemonic_parts:
        share = Share.from_mnemonic(part)
        recovery_state.add_share(share)

    passphrase = recovery_state.recover(str.encode(passphrase))
    return Bip39MnemonicGenerator().FromEntropy(passphrase)


@cli.command()
@click.option(
    "--mnemonic-parts",
    default=None,
    help="Comma separated seed parts to recover master seed phrase.",
)
@click.option(
    "--passphrase", default=None, help="Passphrase to recover master seed phrase."
)
def recover(mnemonics: str, passphrase: str):
    if not mnemonics or not passphrase:
        raise click.BadArgumentUsage("Mnemonics and/or passphrase not provided.")
    seed = _recover(mnemonics, passphrase)
    click.echo("Master seed phrase:")
    click.echo(seed)
    click.echo("Successfully recovered master seed!")


if __name__ == "__main__":
    cli()
