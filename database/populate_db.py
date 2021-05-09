import warnings
import os
import io
import pandas as pd
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")

engine = create_engine('postgresql://postgres:1234@localhost:5432')


def main() -> None:
    vcf = read_vcf("database/data/unziped.vcf")
    restructured_vcf = reformat(vcf)
    restructured_vcf.to_sql("variants", engine, if_exists="append", index=False, chunksize=1_000)


def read_vcf(path: str):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': str, 'ID': str, 'REF': str, 'ALT': str,
               'FORMAT': str},
        sep='\t',
    ).rename(columns={'#CHROM': 'POS', "POS": "ID", "ID": "REF", "REF": "ALT", "ALT FORMAT": "FORMAT"}).reset_index()


def reformat(vcf: pd.DataFrame) -> pd.DataFrame:
    restructured_vcf = pd.DataFrame()
    restructured_vcf["chromosome"] = vcf["index"]
    restructured_vcf["position"] = vcf["POS"].astype(int)
    restructured_vcf["rsid"] = vcf["ID"].str.strip()
    restructured_vcf["ref"] = vcf["REF"].str.strip()
    restructured_vcf["alt"] = vcf["ALT"].str.strip()
    restructured_vcf["info"] = vcf["FORMAT"].str.strip()
    restructured_vcf = restructured_vcf.drop_duplicates(["chromosome", "position"])
    return restructured_vcf


if __name__ == "__main__":
    main()
