import argparse
import binascii
import itertools
import sys

from mnemonic import Mnemonic
import shamir_mnemonic

MN = Mnemonic('english')


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('Must be a positive integer')
    return ivalue


def check_bip39_phrase(phrase):
    return MN.check(phrase)


def phrase_to_seed(phrase):
    try:
        entropy = MN.to_entropy(phrase)
    except ValueError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(2)
    return entropy


def seed_to_phrase(seed):
    return MN.to_mnemonic(seed)


def combine_mnemonics(m):
    shares = []
    for i in range(m):
        print('\n=========================')
        share = input(f'Enter mnemonic share #{i+1}:\n').strip()
        print('=========================')
        shares.append(share)
    try:
        seed = shamir_mnemonic.combine_mnemonics(shares)
    except shamir_mnemonic.MnemonicError as e:
        print()
        print(e, file=sys.stderr)
        sys.exit(2)
    phrase = seed_to_phrase(seed)
    return seed, phrase


def combine_output(seed, phrase):
    print()
    print(f'SEED: {seed.hex()}')
    print()
    print(f'BIP39 PASSPHRASE: {phrase}')
    print()


def print_seed(seed):
    print()
    print('\n======================================')
    print(f'SEED: {seed.hex()}')
    print('======================================')
    print()


def split_mnemonic(m, n):
    phrase = input('Enter BIP39 phrase:\n')

    is_valid = check_bip39_phrase(phrase)
    if not is_valid:
        print('The BIP39 phrase is invalid.', file=sys.stderr)
        sys.exit(2)

    seed = phrase_to_seed(phrase)

    print_seed(seed)
    print('\nGenerating shares...')
    mnemonics = shamir_mnemonic.generate_mnemonics(1, [(m, n)], seed)[0]

    combinations = [combo for combo in itertools.combinations(mnemonics, m)]

    for combo in combinations:
        secret = shamir_mnemonic.combine_mnemonics(combo)
        if secret != seed:
            print(
                'Error: a combination of shares failed to verify. Try again.',
                file=sys.stderr)
            sys.exit(2)

    return mnemonics


def split_output(mnemonics):
    print()
    for i, mnemonic in enumerate(mnemonics, 1):
        print('===========')
        print(f'Mnemonic {i}')
        print('===========\n')
        print(f'{mnemonic}\n')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--combine', action='store_true',
                       help='Recover secret from shares')
    group.add_argument('-s', '--split', action='store_true',
                       help='Split secret into shares')
    parser.add_argument('-t', '--threshold', type=check_positive,
                        required=True,
                        help='Number of shares required to recover secret')
    parser.add_argument('-n', '--number', type=check_positive,
                        help='Number of total shares')
    args = parser.parse_args()

    if args.split and args.number is None:
        parser.error('when using --split, -n/--number is required')

    m = args.threshold
    n = args.number

    if args.combine:
        seed, phrase = combine_mnemonics(m=m)
        combine_output(seed, phrase)
    elif args.split:
        if (m + 1) > n:
            parser.error(
                'The number of shares must be greater than the threshold.')
        mnemonics = split_mnemonic(m=m, n=n)
        split_output(mnemonics)


main()
