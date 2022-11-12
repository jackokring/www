# Phinka tools for data processing

Launch by `python -m phinka` with `python-is-python3` installed. Help is available with the `--help` option. Check out the package source of `phinka.__main__.py` for more details.

# `blwz` compression

A data compression tool. A BWT transform followed by partition on the following letter, with an offset LZW per partition and then another partition into three symbol rate groups with a final gzip.

The BWT groups similar symbols. The partition keeps the LZW dictionary smaller. The second partition removes some common most significant bits from the LZW dictionary keys. The gzip then chooses a good coding for the final symbol stream based on remaining entropy.