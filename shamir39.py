import argparse
import binascii
import itertools
import sys

from mnemonic import Mnemonic
import shamir_mnemonic


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('Must be a positive integer')
    return ivalue


def phrase_to_seed(phrase):
    entropy = mn.to_entropy(phrase)
    return binascii.hexlify(entropy)


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--combine', action='store_true')
group.add_argument('--split', action='store_true')
parser.add_argument('-t', '--threshold', type=check_positive, required=True,
                    help='Number of shares required to decrypt secret')
parser.add_argument('-n', '--number', type=check_positive, required=True,
                    help='Number of total shares')
args = parser.parse_args()

m = args.threshold
n = args.number

if (m + 1) > n:
    print('The number of shares must be greater than the threshold.')
    sys.exit()


mn = Mnemonic('english')
phrase = input('Enter BIP39 phrase:\n')
seed = phrase_to_seed(phrase)
print()
print(seed.decode())

print('\nGenerating mnemonics...')
mnemonics = shamir_mnemonic.generate_mnemonics(1, [(m, n)], seed)[0]

combinations = [combo for combo in itertools.combinations(mnemonics, m)]

for combo in combinations:
    secret = shamir_mnemonic.combine_mnemonics(combo)
    if secret != seed:
        print('THERE WAS AN ERROR WITH THE MNEMONICS. TRY AGAIN.')
        sys.exit()

print()
for i, mnemonic in enumerate(mnemonics, 1):
    print('===========')
    print(f'Mnemonic {i}')
    print('===========\n')
    print(f'{mnemonic}\n')
