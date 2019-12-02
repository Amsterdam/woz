"""
Module Contains logic to get the latest most up to date
files to import in the WOZ database

checks:

   check date in filenames
     - we do not work with old data
   check filename changes
     - we do not work of old files because new files are renamed

"""
import logging
import os

from functools import lru_cache
from dateutil import parser

from swiftclient.client import Connection
from django.conf import settings

log = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

CONTAINER = os.getenv('GOB_OBJECTSTORE_ENV', 'productie')
WOZ_FOLDER = 'woz/CSV/'

os_connect = {
    'auth_version': '2.0',
    'authurl': 'https://identity.stack.cloudvps.com/v2.0',
    'user': 'GOB_user',
    'key': settings.OBJECTSTORE_PASSWORD,
    'tenant_name': settings.OBJECTSTORE_TENNANT,
    'os_options': {
        'tenant_id': settings.OBJECTSTORE_TENNANT_ID,
        'region_name': 'NL',
    }
}


@lru_cache(maxsize=None)
def get_conn():
    assert os.getenv('GOB_OBJECTSTORE_PASSWORD')
    return Connection(**os_connect)


def get_full_container_list(container_name, **kwargs):
    """
    Return a listing of filenames in container `container_name`
    :param container_name:
    :param kwargs:
    :return:
    """
    limit = 10000
    kwargs['limit'] = limit
    page = []
    seed = []
    _, page = get_conn().get_container(container_name, **kwargs)
    seed.extend(page)

    while len(page) == limit:
        # keep getting pages..
        kwargs['marker'] = seed[-1]['name']
        _, page = get_conn().get_container(container_name, **kwargs)
        seed.extend(page)

    return seed


def download_file(container_name, file_path):
    """
    Download a  file
    :param container_name:
    :param file_path:
    :return:
    """

    path = file_path.split('/')
    file_name = path[-1]

    log.info(f"Create file {file_name} in {settings.LOCAL_DATA_DIR}")
    newfilename = '{}/{}'.format(settings.LOCAL_DATA_DIR, file_name)

    if os.path.exists(newfilename):
        log.debug('Skipped file exists: %s', newfilename)
        return

    with open(newfilename, 'wb') as newfile:
        zipdata = get_conn().get_object(container_name, file_path)[1]
        newfile.write(zipdata)


def download_files(container_name, files_map):
    """
    Download latest files
    """

    for _, file in files_map.items():
        file.sort(reverse=True)
        file_name = file[0][1]['name']
        download_file(container_name, file_name)


def unzip_files(zipsource):
    """
    Unzip single files to the right target directory
    """

    # Extract files to the expected location
    directory = os.path.join(settings.LOCAL_DATA_DIR)

    for fullname in zipsource.namelist():
        zipsource.extract(fullname, directory)


def delete_from_objectstore(container, object_name):
    """
    remove file `object_name` fronm `container`
    :param container: Container name
    :param object_name:
    :return:
    """
    return get_conn().delete_object(container, object_name)


def delete_old_files(container_name, files_map):
    """
    Cleanup old fo;es
    """
    for _, file in files_map.items():
        log.debug('KEEP : %s', file[0][1]['name'])
        if len(file) > 1:
            # delete old files
            for _, file_object in file[1:]:
                filepath = file_object['name']
                log.debug('PURGE: %s', filepath)
                delete_from_objectstore(container_name, filepath)


def get_woz_files(container_name=CONTAINER, wozfolder=WOZ_FOLDER):
    """
    fetch files from folder in an objectstore container
    :param container_name:
    :param folder:
    :return:
    """
    log.info(f"find woz file from {wozfolder}")
    files_map = {}

    for file_object in get_full_container_list(container_name, prefix=wozfolder):
        if file_object['content_type'] == 'application/directory':
            continue

        path = file_object['name'].split('/')
        file_name = path[-1]

        if file_name.endswith('.csv'):
            dt = parser.parse(file_object['last_modified'])
            file_key = "".join(file_name.split('_')[1:])
            files_map.setdefault(file_key, []).append((dt, file_object))

    download_files(container_name, files_map)
    delete_old_files(container_name, files_map)


def fetch_woz_files():
    """
    Haal WOZ zip file op en pak uit
    :return:
    """
    logging.basicConfig(level=logging.DEBUG)
    # creat folders where files are expected.
    if not os.path.exists(settings.LOCAL_DATA_DIR):
        os.makedirs(settings.LOCAL_DATA_DIR)
    # download and unpack the zip files
    get_woz_files()
