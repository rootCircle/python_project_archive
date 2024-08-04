from bs4 import BeautifulSoup
from urllib.request import urlopen
import platform
import UnsupportedOS

URL = "https://www.nasm.us/pub/nasm/releasebuilds"
APPEND_PARAMS_URL = "?C=M;O=D"


def main():
    soup = get_soup(f"{URL}/{APPEND_PARAMS_URL}")
    release_url = f"{URL}/{get_latest_version(soup)}/{get_platform()}"
    release_soup = get_soup(release_url)
    print(release_url)
    print(get_installer(release_soup, get_platform()))


def get_soup(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_latest_version(soup):
    return soup.select_one("tr.odd a").get("href").replace("/", "")


def get_platform():
    os_name = platform.system()
    os_name = os_name.lower()
    if "linux" in os_name:
        return "linux"
    elif "darwin" in os_name:
        return "macosx"
    elif "win32" in os_name:
        return "win32"
    elif "win64" in os_name:
        return "win64"
    else:
        return "unknown"


def get_pc_architecture():
    machine = platform.machine()
    if "64" in machine:
        return "x86_64"
    elif "86" in machine:
        return "i686"
    else:
        return None


def get_installer(soup, platform):
    UnsupportedOS.check_os_supported(platform)

    if platform in ["win32", "win64"]:
        # Select all <a> elements within <td> elements inside <tr> elements
        a_elements = soup.select("tr td a")

        # Iterate through the <a> elements and extract href for those ending with '.exe'
        for a_element in a_elements:
            inner_text = a_element.get_text()
            if inner_text.endswith(".exe"):
                exe_href = a_element.get("href")
                return exe_href

    elif platform == "macosx":
        # Select all <a> elements within <td> elements inside <tr> elements
        a_elements = soup.select("tr td a")

        # Iterate through the <a> elements and extract href for those ending with '.exe'
        for a_element in a_elements:
            inner_text = a_element.get_text()
            if inner_text.endswith(".zip"):
                exe_href = a_element.get("href")
                return exe_href

    elif platform == "linux":
        return "bruh"


if __name__ == "__main__":
    main()
