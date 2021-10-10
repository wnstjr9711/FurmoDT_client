import os
import re
import six
import sys
import json
import tqdm
import shutil
import requests
import tempfile
import textwrap
import warnings
import os.path as osp
from bs4 import BeautifulSoup
from six.moves import urllib_parse
from PySide2.QtCore import QThread

home = osp.expanduser("~")
CHUNK_SIZE = 512 * 1024
PROGRESS = 0


# ******************************************** 쓰레드 작업 ******************************************** #
class DownLoadThread(QThread):
    def __init__(self, main, download_link, video_path):
        super(DownLoadThread, self).__init__()
        self.main = main
        self.download_link = download_link
        self.video_path = video_path

    def run(self):
        download(self.download_link, self.video_path, self.main.video_progressbar)
        self.main.event_video_set()
# ******************************************** 쓰레드 작업 ******************************************** #


if hasattr(textwrap, "indent"):
    indent_func = textwrap.indent
else:
    def indent_func(text, prefix):
        def prefixed_lines():
            for line in text.splitlines(True):
                yield prefix + line if line.strip() else line

        return "".join(prefixed_lines())


def get_url_from_gdrive_confirmation(contents):
    url = ""
    for line in contents.splitlines():
        m = re.search(r'href="(\/uc\?export=download[^"]+)', line)
        if m:
            url = "https://docs.google.com" + m.groups()[0]
            url = url.replace("&amp;", "&")
            break
        m = re.search("confirm=([^;&]+)", line)
        if m:
            confirm = m.groups()[0]
            url = re.sub(
                r"confirm=([^;&]+)", r"confirm={}".format(confirm), url
            )
            break
        m = re.search('"downloadUrl":"([^"]+)', line)
        if m:
            url = m.groups()[0]
            url = url.replace("\\u003d", "=")
            url = url.replace("\\u0026", "&")
            break
        m = re.search('<p class="uc-error-subcaption">(.*)</p>', line)
        if m:
            error = m.groups()[0]
            raise RuntimeError(error)
    if not url:
        raise RuntimeError(
            "Cannot retrieve the public link of the file. "
            "You may need to change the permission to "
            "'Anyone with the link', or have had many accesses."
        )
    return url


def parse_url(url, warning=True):
    """Parse URLs especially for Google Drive links.
    file_id: ID of file on Google Drive.
    is_download_link: Flag if it is download link of Google Drive.
    """
    parsed = urllib_parse.urlparse(url)
    query = urllib_parse.parse_qs(parsed.query)
    is_gdrive = parsed.hostname == "drive.google.com"
    is_download_link = parsed.path.endswith("/uc")

    file_id = None
    if is_gdrive and "id" in query:
        file_ids = query["id"]
        if len(file_ids) == 1:
            file_id = file_ids[0]
    match = re.match(r"^/file/d/(.*?)/view$", parsed.path)
    if match:
        file_id = match.groups()[0]

    if warning and is_gdrive and not is_download_link:
        warnings.warn(
            "You specified Google Drive Link but it is not the correct link "
            "to download the file. Maybe you should try: {url}".format(
                url="https://drive.google.com/uc?id={}".format(file_id)
            )
        )

    return file_id, is_download_link


def download(url, output, bar):
    """Download file from URL.
    Parameters
    ----------
    url: str
        URL. Google Drive URL is also supported.
    output: str, optional
        Output filename. Default is basename of URL.
    bar: Qt.roundProgressBar
    Returns
    -------
    output: str
        Output filename.
    """
    url_origin = url
    sess = requests.session()

    # Load cookies
    cache_dir = osp.join(home, ".cache", "gdown")
    if not osp.exists(cache_dir):
        os.makedirs(cache_dir)
    cookies_file = osp.join(cache_dir, "cookies.json")
    if osp.exists(cookies_file):
        with open(cookies_file) as f:
            cookies = json.load(f)
        for k, v in cookies:
            sess.cookies[k] = v

    file_id, is_download_link = parse_url(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # NOQA
    }
    while True:
        res = sess.get(url, headers=headers, stream=True)
        # Save cookies
        with open(cookies_file, "w") as f:
            cookies = [
                (k, v)
                for k, v in sess.cookies.items()
                if not k.startswith("download_warning_")
            ]
            json.dump(cookies, f, indent=2)

        if "Content-Disposition" in res.headers:
            # This is the file
            break
        if not (file_id and is_download_link):
            break

        # Need to redirect with confirmation
        try:
            url = get_url_from_gdrive_confirmation(res.text)
        except RuntimeError as e:
            print("Access denied with the following error:")
            error = "\n".join(textwrap.wrap(str(e)))
            error = indent_func(error, "\t")
            print("\n", error, "\n", file=sys.stderr)
            print(
                "You may still be able to access the file from the browser:",
                file=sys.stderr,
            )
            print("\n\t", url_origin, "\n", file=sys.stderr)
            return
    if file_id and is_download_link:
        m = re.search('filename="(.*)"', res.headers["Content-Disposition"])
        filename_from_url = m.groups()[0]
    else:
        filename_from_url = osp.basename(url)

    if output is None:
        output = filename_from_url
    output_is_path = isinstance(output, six.string_types)
    if output_is_path and output.endswith(osp.sep):
        if not osp.exists(output):
            os.makedirs(output)
        output = osp.join(output, filename_from_url)

    if output_is_path:
        tmp_file = tempfile.mktemp(
            suffix=tempfile.template,
            prefix=osp.basename(output),
            dir=osp.dirname(output),
        )
        f = open(tmp_file, "wb")
    else:
        tmp_file = None
        f = output

    try:
        pbar = tqdm.tqdm(res.content, bar_format='{desc}: {percentage:3.0f}')
        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            pbar.update(len(chunk))
            bar.rpb_setValue(int(str(pbar)))
        pbar.close()
        if tmp_file:
            f.close()
            shutil.move(tmp_file, output)
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        sess.close()
        try:
            if tmp_file:
                os.remove(tmp_file)
        except OSError:
            pass
    return output


def getfilename(fid):
    # 공유링크로 파일이름 가져오기
    try:
        res = requests.get(fid)
        soup = BeautifulSoup(res.text, 'html.parser')
        f_name = soup.find('title').text.split()[0]
        return f_name
    except requests.exceptions.RequestException:
        return None
