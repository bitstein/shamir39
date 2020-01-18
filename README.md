# Shamir39

This library uses Trezor's BIP39 [python-mnemonic](https://github.com/trezor/python-mnemonic) and SLIP39 [python-shamir-mnemonic](https://github.com/trezor/python-shamir-mnemonic) libraries to perform [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing) on a BIP39 passphrase.

⚠️ **This is untested software based on software that remains under review. Use at your own risk, and don't use it to protect money!** ⚠️

## Usage

This software is written in `python3` and should not rely on third-party libraries. Trezor libraries are included. Please ensure they are up to date before using.

```
usage: shamir39.py [-h] (-c | -s) -t THRESHOLD [-n NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -c, --combine         Recover secret from shares
  -s, --split           Split secret into shares
  -t THRESHOLD, --threshold THRESHOLD
                        Number of shares required to recover secret
  -n NUMBER, --number NUMBER
                        Number of total shares
```

## Learn More

* BIP39: Mnemonic code for generating deterministic keys: [https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
* SLIP-0039 : Shamir's Secret-Sharing for Mnemonic Codes: [https://github.com/satoshilabs/slips/blob/master/slip-0039.md](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)

## Other Implementations

* Ian Coleman's `slip39`: [https://github.com/iancoleman/slip39](https://github.com/iancoleman/slip39)
* Unchained Capital's `hermit`: [https://github.com/unchained-capital/hermit](https://github.com/unchained-capital/hermit)

## Criticism of Shamir's Secret Sharing

* ["Shamir Secret Snakeoil"](https://en.bitcoin.it/wiki/Shamir_Secret_Snakeoil) by Greg Maxwell [Bitcoin Wiki]
* ["Shamir's Secret Sharing Shortcomings"](https://blog.keys.casa/shamirs-secret-sharing-security-shortcomings/) by Jameson Lopp
