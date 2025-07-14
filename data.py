import csv
import os
from typing import List, Tuple


def test_splits(txt_file: str, out_path: str, doc_types: List[Tuple[str, str]],
                only_domain: str = None, only_format: str = None):
    """Test splits using test txt file"""
    with open(txt_file, "r", encoding="utf-8") as rf, open(out_path, "w", encoding="utf-8") as wf:
        lines = rf.readlines()
        doc_indx = 0

        for line in lines:
            if line[:10] == "-DOCSTART-":
                doc_indx += 1
                domain, doc_format = doc_types[doc_indx]

            if (not only_domain or only_domain == domain) and (not only_format or only_format == doc_format):
                if len(line) > 1:
                    text, *_, label = line.split(" ")
                    wf.write(text + " " + label + "")
                else:
                    wf.write("\n")


def from_csv(csv_path: str, out_path: str, outputs: bool = False,
             only_domain: str = None, only_format: str = None):
    """CSV to CoNLL format"""
    with open(csv_path, "r", encoding="utf-8") as rf, open(out_path, "w", encoding="utf-8") as wf:
        read = csv.reader(rf)

        for line in read:
            
            if outputs:
                _, text, true, _, pred, domain, doc_format, *_ = line
                text = text.replace("\\", "")
                
                if (text != "text") and (not only_domain or only_domain == domain) and (not only_format or only_format == doc_format):
                    wf.write(text + " " + pred + "\n")

            else:
                id, text, domain, doc_format, label, *_ = line
                text = text.replace("\\", "")

                if (text != "text") and (not only_domain or only_domain == domain) and (not only_format or only_format == doc_format):
                    wf.write(text + " " + label + "\n")
                        

def get_doc_types(csv_file: str):
    with open(csv_file, "r", encoding="utf-8") as rf:
        read = csv.reader(rf)

        doc_types = []

        for line in read:
            _, domain, doc_format, _ = line
            doc_types.append((domain, doc_format))  # 0 index is header

        return doc_types


def _manage_file_name(test_set: str, domain: str, doc_format: str):
    filename = [test_set]
    if domain:
        filename.append(domain.lower().replace(" ", "_"))
    if doc_format:
        filename.append(doc_format.lower().replace(" ", "_"))

    return os.path.join(test_set, "_".join(filename) + ".txt")


if __name__ == "__main__":
    doc_types = get_doc_types("document_types.csv")

    domains = [None, 'SPORTS', 'WORLD EVENTS', 'ECONOMY']
    doc_formats = [None, 'TEXT ARTICLE', 'DATA REPORT', 'HYBRID']

    tests = ["conll_sharp", "conll_sharp_asp_order"]
    models = ["xlm_flert", "luke", "asp"]

    for domain in domains:
        for doc_format in doc_formats:

            # CoNLL-03 from TXT
            out_path = _manage_file_name("conll_03", domain, doc_format)
            test_splits("original_conll/test.txt", out_path, doc_types=doc_types, only_domain=domain, only_format=doc_format)

            # CoNLL# from CSV (both orders)
            for test in tests:
                out_path = _manage_file_name(test, domain, doc_format)
                from_csv(f"test_csvs/{test}.csv", out_path, only_domain=domain, only_format=doc_format)

            # Outputs for all models on CoNLL#
            for model in models:
                out_path = _manage_file_name(f"{model}_sharp", domain, doc_format)
                from_csv(f"output_csvs/{model}_sharp_outputs.csv", out_path, outputs=True, only_domain=domain,
                        only_format=doc_format)
                
            # Outputs for all XLM-FLERT on CoNLL-03
            out_path = _manage_file_name("xlm_flert_03", domain, doc_format)
            from_csv(f"output_csvs/xlm_flert_03_outputs.csv", out_path, outputs=True, only_domain=domain,
                    only_format=doc_format)         


    