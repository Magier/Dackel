from pathlib import Path
import shutil
from git import Repo
import zipfile
import sigma

import urllib

import sigma.collection

RULES_SUBDIR: str = "rules"

PATH = Path("rules/sigmahq")


def _sync_with_git():
    GITHUB_REPO: str = "https://github.com/SigmaHQ/sigma.git"
    if PATH.exists():
        repo = Repo(PATH)
    else:
        PATH.mkdir(exist_ok=True)
        repo = Repo.clone_from(GITHUB_REPO, PATH)
    return repo


def sync():
    zip_path = download_latest_repo()
    num_extracted_files = extract_rules(zip_path)
    # remove the downloaded archive again
    # Path(zip_path).unlink()
    print(f"downloaded {num_extracted_files} from SigmaHQ")


def download_latest_repo() -> Path:
    GITHUB_REPO: str = "https://github.com/SigmaHQ/sigma/archive/master.zip"
    # dl_path, status = urlretrieve(GITHUB_REPO, filename=PATH / "master.zip")
    zip_path = PATH / "master.zip"
    PATH.mkdir(exist_ok=True)

    with urllib.request.urlopen(GITHUB_REPO) as response, open(zip_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
    return zip_path


def extract_rules(zip_path: Path) -> int:
    # Currently, repo offers 3 types of rules in dedicated folders:
    # - `rules`: Are threat agnostic, their aim is to detect a behavior or an implementation of a technique or procedure that was, can or will be used by a potential threat actor.
    # - `rules-threat-hunting`: Are broader in scope and are meant to give the analyst a starting point to hunt for potential suspicious or malicious activity
    # - `rules-emerging-threats`: Are rules that cover specific threats, that are timely and relevant for certain periods of time. These threats include specific APT campaigns, exploitation of Zero-Day vulnerabilities, specific malware used during an attack,...etc.
    keep_dirs = {"rules", "rules-threat-hunting", "rules-emerging-threats"}
    num_extracted_files = 0
    with zipfile.ZipFile(zip_path, "r") as zip:
        for f in zip.infolist():
            if f.file_size == 0:  # ignore folders
                continue
            if any(f.filename.startswith(f"sigma-master/{rule_dir}/") for rule_dir in keep_dirs):
                raw_content = zip.read(f)
                f.filename = f.filename.replace("sigma-master", str(PATH))
                if f.filename.endswith(".yml") and is_rule_relevant(raw_content):
                    zip.extract(f)
                    num_extracted_files += 1
    return num_extracted_files


def is_rule_relevant(raw: bytes) -> bool:
    # TODO: parse to Sigma object and check logsource
    data = raw.decode("utf-8")

    s = sigma.collection.SigmaCollection.from_yaml(data)
    for r in s.rules:
        if is_logsource_relevant(r.logsource.product, r.logsource.category, r.logsource.service):
            return True
    return False


SUPPORTED_PRODUCTS = {"kubernetes", "linux"}
SUPPORTED_CATEGORIES = {"dns"}
SUPPORTED_SERVICES = {}


def is_logsource_relevant(product: str | None, category: str | None, service: str | None) -> bool:
    if product in SUPPORTED_PRODUCTS:
        return True
    if category in SUPPORTED_CATEGORIES:
        return True
    if service in SUPPORTED_SERVICES:
        return True

    if category == "network_connection":
        # TODO filter rule if anything specific to an OS as well, if so, log the case
        # e.g. commands like `Image`, `Image|contains`, `CommandLine|contains`
        return True

    # TODO: for rules of other OS' try to translate them where possible
    # e.g. vscode tunnel, which is available only for windows, but works with DNS query

    # https://github.com/SigmaHQ/sigma/blob/master/rules/windows/network_connection/net_connection_win_domain_crypto_mining_pools.yml
    # https://github.com/SigmaHQ/sigma/blob/master/rules/windows/network_connection/net_connection_win_domain_devtunnels.yml
    # https://github.com/SigmaHQ/sigma/blob/master/rules/windows/network_connection/net_connection_win_domain_btunnels.yml

    return False
