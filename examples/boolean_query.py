from valis import valis, Dataset, ALL
from auth import VALIS_AUTH_USER, VALIS_AUTH_KEY

valis.login(VALIS_AUTH_USER, VALIS_AUTH_KEY)

# search for variants in both TCGA and EXAC
tcga_exac_intersection = valis.variants.query(datasets=ALL([Dataset.TCGA, Dataset.EXAC]))

# print first 10 variant with full metadata fields:
print(tcga_exac_intersection.fetch(full=True, limit=10))


