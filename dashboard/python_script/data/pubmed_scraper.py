from Bio import Entrez
from Bio import Medline


def search_pubmed(query, max_results, retstart):
    Entrez.email = "your_email@example.com"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, retstart=retstart)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_pubmed_details(pubmed_ids):
    result_dict = {}

    for pubmed_id in pubmed_ids:
        handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="medline")
        record = Medline.read(handle)
        handle.close()

        title = record.get("TI", None)
        abstract = record.get("AB", None)
        author = record.get("AU", "")
        date_of_publication = record.get("DP", None)
        pmid = record.get("PMID", None)

        link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        result_dict[title] = {
            "abstract": abstract,
            "author": ", ".join(author),
            "date_of_publication": date_of_publication,
            "link": link
        }

    return result_dict


def get_articles(query="Sarscov2", max_results=5, offset=0):
    id_list = search_pubmed(query, max_results, offset)
    articles = fetch_pubmed_details(id_list)
    return articles


if __name__ == '__main__':
    pass
