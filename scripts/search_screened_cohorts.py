#!/usr/bin/env python3
"""Search and strictly screen public cohort candidates in parallel.

The script searches Europe PMC literature and NCBI GEO DataSets for each tumor
separately. Search hits are candidates only; they still require manual review
of the primary source and the repository cohort-screening gate.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import threading
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path


USER_AGENT = "spatial-continuum-cohort-screen/0.1"
DEFAULT_OUTPUT = Path("data/derived/cohort_search_screened.json")
NCBI_MIN_INTERVAL_SECONDS = 0.45
_ncbi_lock = threading.Lock()
_last_ncbi_request = 0.0


@dataclass(frozen=True)
class TumorSpec:
    name: str
    europe_query: str
    geo_query: str
    required_groups: tuple[tuple[str, ...], ...]
    excluded_terms: tuple[str, ...]


SPECS = (
    TumorSpec(
        name="GIST",
        europe_query='GIST AND imatinib AND (recurrence OR "recurrence-free survival" OR RFS) AND (patient OR cohort)',
        geo_query='GIST imatinib recurrence patient cohort',
        required_groups=(("gist",), ("imatinib",), ("recurrence", "recurrence-free", "RFS"), ("patient", "patients", "cohort", "clinical trial", "trial")),
        excluded_terms=("cell line", "xenograft", "mouse", "in vitro", "cell culture", "2d", "3d", "review", "meta-analysis"),
    ),
    TumorSpec(
        name="melanoma",
        europe_query='melanoma AND (dabrafenib OR vemurafenib OR BRAF inhibitor) AND (trametinib OR MEK inhibitor) AND (response OR resistance OR progression)',
        geo_query='melanoma BRAF MEK inhibitor patient response resistance',
        required_groups=(("melanoma",), ("dabrafenib", "vemurafenib", "braf inhibitor"), ("trametinib", "mek inhibitor", "mek"), ("response", "resistance", "progression"), ("patient", "patients", "cohort", "clinical trial", "trial")),
        excluded_terms=("cell line", "xenograft", "mouse", "in vitro", "cell culture", "2d", "3d", "review", "meta-analysis"),
    ),
    TumorSpec(
        name="breast",
        europe_query='breast AND (alpelisib OR taselisib OR pictilisib OR buparlisib) AND letrozole AND (response OR progression OR survival)',
        geo_query='breast alpelisib letrozole response patient',
        required_groups=(("breast",), ("alpelisib", "taselisib", "pictilisib", "buparlisib"), ("letrozole",), ("response", "progression", "survival"), ("patient", "patients", "cohort", "clinical trial", "trial")),
        excluded_terms=("cell line", "xenograft", "mouse", "in vitro", "cell culture", "2d", "3d", "review", "meta-analysis"),
    ),
    TumorSpec(
        name="renal",
        europe_query='("renal cell carcinoma" OR ccRCC) AND atezolizumab AND bevacizumab AND (PFS OR "progression-free survival" OR response) AND (patient OR cohort OR trial)',
        geo_query='renal cell carcinoma atezolizumab bevacizumab PFS response cohort',
        required_groups=(("renal cell carcinoma", "ccrcc"), ("atezolizumab",), ("bevacizumab",), ("pfs", "progression-free", "response"), ("patient", "patients", "cohort", "clinical trial", "trial")),
        excluded_terms=("cell line", "xenograft", "mouse", "in vitro", "cell culture", "2d", "3d", "review", "meta-analysis"),
    ),
    TumorSpec(
        name="pancreas",
        europe_query='(pancreatic OR PDAC) AND nivolumab AND gemcitabine AND "nab-paclitaxel" AND (PFS OR "progression-free survival" OR response)',
        geo_query='pancreatic nivolumab gemcitabine nab-paclitaxel PFS response patient',
        required_groups=(("pancreatic", "pdac"), ("nivolumab",), ("gemcitabine",), ("nab-paclitaxel", "nab paclitaxel"), ("pfs", "progression-free", "response"), ("patient", "patients", "cohort", "clinical trial", "trial")),
        excluded_terms=("cell line", "xenograft", "mouse", "in vitro", "cell culture", "2d", "3d", "review", "meta-analysis", "sotigalimab", "apx005m", "ipilimumab", "hydroxychloroquine", "bms-813160", "quemliclustat", "zimberelimab"),
    ),
)


def fetch_json(url: str, ncbi: bool = False) -> dict:
    global _last_ncbi_request
    if ncbi:
        with _ncbi_lock:
            elapsed = time.monotonic() - _last_ncbi_request
            if elapsed < NCBI_MIN_INTERVAL_SECONDS:
                time.sleep(NCBI_MIN_INTERVAL_SECONDS - elapsed)
            _last_ncbi_request = time.monotonic()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 2:
                raise
            retry_after = error.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else 1.5 * (attempt + 1)
            time.sleep(delay)


def search_europe(spec: TumorSpec, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode({"query": spec.europe_query, "format": "json", "resultType": "core", "pageSize": max_results})
    payload = fetch_json(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}")
    hits = []
    for result in payload.get("resultList", {}).get("result", []):
        publication_types = result.get("pubType") or result.get("pubTypeList", {}).get("pubType", [])
        hits.append({
            "source": "Europe PMC",
            "identifier": result.get("pmid") or result.get("id"),
            "title": result.get("title", ""),
            "text": " ".join(filter(None, [result.get("title", ""), result.get("abstractText", "")])),
            "publication_types": publication_types,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{result.get('pmid')}/" if result.get("pmid") else None,
        })
    return hits


def search_geo(spec: TumorSpec, max_results: int) -> list[dict]:
    params = urllib.parse.urlencode({"db": "gds", "term": spec.geo_query, "retmode": "json", "retmax": max_results})
    search = fetch_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}", ncbi=True)
    ids = search.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    summary_params = urllib.parse.urlencode({"db": "gds", "id": ",".join(ids), "retmode": "json"})
    payload = fetch_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{summary_params}", ncbi=True)
    hits = []
    for identifier in ids:
        result = payload.get("result", {}).get(identifier, {})
        hits.append({
            "source": "NCBI GEO",
            "identifier": result.get("accession") or identifier,
            "title": result.get("title", ""),
            "text": " ".join(filter(None, [result.get("title", ""), result.get("summary", "")])),
            "publication_types": [],
            "url": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={result.get('accession')}" if result.get("accession") else None,
        })
    return hits


def screen_hit(spec: TumorSpec, hit: dict) -> dict:
    text = re.sub(r"\s+", " ", hit.get("text", "")).lower()
    missing_groups = [list(group) for group in spec.required_groups if not any(term in text for term in group)]
    exclusions = [term for term in spec.excluded_terms if term in text]
    publication_types = hit.get("publication_types", [])
    if isinstance(publication_types, str):
        publication_types = [publication_types]
    if any("review" in str(pub_type).lower() or "meta-analysis" in str(pub_type).lower() for pub_type in publication_types):
        exclusions.append("publication_type_review")
    hit["missing_required_groups"] = missing_groups
    hit["exclusion_hits"] = exclusions
    hit["screen_status"] = "PASS" if not missing_groups and not exclusions else "REVIEW" if not exclusions else "REJECT"
    return hit


def run_source(spec: TumorSpec, source: str, max_results: int) -> tuple[str, str, list[dict], str | None]:
    try:
        hits = search_europe(spec, max_results) if source == "Europe PMC" else search_geo(spec, max_results)
        return spec.name, source, [screen_hit(spec, hit) for hit in hits], None
    except Exception as error:  # Network failures are recorded per source, not hidden.
        return spec.name, source, [], f"{type(error).__name__}: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-results", type=int, default=25)
    args = parser.parse_args()

    results: dict[str, dict] = {spec.name: {"queries": {"Europe PMC": spec.europe_query, "NCBI GEO": spec.geo_query}, "hits": [], "errors": []} for spec in SPECS}

    # Europe PMC tolerates parallel requests; NCBI E-utilities are deliberately
    # serialized to avoid rate limiting and preserve a complete audit trail.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SPECS)) as executor:
        europe_futures = [executor.submit(run_source, spec, "Europe PMC", args.max_results) for spec in SPECS]
        for future in concurrent.futures.as_completed(europe_futures):
            tumor, source, hits, error = future.result()
            results[tumor]["hits"].extend(hits)
            if error:
                results[tumor]["errors"].append({"source": source, "error": error})

    for spec in SPECS:
        tumor, source, hits, error = run_source(spec, "NCBI GEO", args.max_results)
        results[tumor]["hits"].extend(hits)
        if error:
            results[tumor]["errors"].append({"source": source, "error": error})

    for record in results.values():
        record["hits"] = sorted(record["hits"], key=lambda hit: (hit["screen_status"], hit["source"], hit["identifier"] or ""))
        record["pass_count"] = sum(hit["screen_status"] == "PASS" for hit in record["hits"])
        record["review_count"] = sum(hit["screen_status"] == "REVIEW" for hit in record["hits"])
        record["reject_count"] = sum(hit["screen_status"] == "REJECT" for hit in record["hits"])

    report = {
        "method": "parallel Europe PMC and NCBI GEO search with tumor-specific treatment/endpoint filters",
        "candidate_only": True,
        "tumors": results,
        "interpretation": "PASS means a candidate satisfies text-level filters only; primary-source review and data/cohort screening remain mandatory.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({tumor: {key: value for key, value in record.items() if key.endswith("_count") or key == "errors"} for tumor, record in results.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
