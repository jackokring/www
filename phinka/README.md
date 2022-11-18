# Phinka tools for data processing

Launch by `python -m phinka` with `python-is-python3` installed. Help is available with the `--help` option. Check out the package source of `phinka.__main__.py` for more details.

# `blwz` compression

A data compression tool. A BWT transform followed by partition on the following letter, with an offset LZW per partition and then another partition into three symbol rate groups with a final gzip.

The BWT groups similar symbols. The partition keeps the LZW dictionary smaller. The second partition removes some common most significant bits from the LZW dictionary keys. The gzip then chooses a good coding for the final symbol stream based on remaining entropy.

Some say it's an experiment in removing self-partition mutual information. So when I say the LZW dictionary is smaller, each one is. But there is now an LZW dictionary for each partition. Along with common lettering in each partition from the BWT this improves the LZW.

Making the LZW index down from the last dictionary entry as zero, makes more zeros in the stream, and uncommon individual symbols have lower (more zeros) entry codes from the partition. The high bits of dictionary codes also "gtow" slower and have more zeros earlier in the partition, so these can be grouped as a secondary partitioning and effectively compressed by gzip.

It is thus an experiment in information "fission" in the partion of information blocks to test the limits of the Landau information mass energy equivalence with the "evaporated radiation" information being mutual and hence not stored with the remaining information "mass" pattern.

The "evapourate" is inferred at decompression as it has to have a necessary form to refuse the block to the required form is the hypothesis. Either it then further implies a fusion form exists or it doesn't.

# `dx` calculus

Some integration asymptotic series. Consider what gradient decent means when `f = Integral(f)'`, so a dominant integration in control system stability allows closing feedback loops and perhaps using an identity expression of the last stage input as the gradient. Given the anulus of convergence goes "off" as some "error" in polynomial greater than one powering, certain growth forms relating to the `P != NP` inverse exponential of the less than one powering supra(ex)ponetial.

Thanks
The Management
