import logging
import os
from typing import Callable, Any, Dict, Union
import requests
from requests.auth import HTTPBasicAuth
from functools import wraps
from .types import Collection, CollectionResponse

BASE_URL = "https://modac.cancer.gov/api"

_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


def ensure_authenticated(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self: "MoDaCClient", *args: Any, **kwargs: Any) -> Any:
        if not self._token:
            self.authenticate()
        return func(self, *args, **kwargs)

    return wrapper


# Not sure if we need it, just wrap it with loggers
def log_action(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self: "MoDaCClient", *args: Any, **kwargs: Any) -> Any:
        _logger.warning(
            f"Calling function '{func.__name__}' with args: {args} kwargs: {kwargs}"
        )
        result = func(self, *args, **kwargs)
        _logger.warning(f"Function '{func.__name__}' returned: {result}")
        return result

    return wrapper


class MoDaCClient:
    BASE_URL = "https://modac.cancer.gov/api"

    def __init__(self) -> None:
        self._token: str = ""
        self.authenticate()

    def authenticate(self) -> bool:
        url = "/".join((self.BASE_URL, "authenticate"))
        auth_resp = requests.get(url, auth=self._login_headers())
        auth_resp.raise_for_status()
        self._token = auth_resp.content.decode("utf-8")
        return True

    @ensure_authenticated
    @log_action
    def get_collection(self, path: str) -> Union[Collection, None]:
        url = "/".join((self.BASE_URL, "collection", path))
        _logger.warning(f"Get collection. Making requests to {url}")

        resp = requests.get(url + "?list=true", headers=self._token_headers())
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            _logger.error(f"HTTPError: {e}")
            _logger.error(f"Response Content: {resp.content.decode('utf-8')}")
            raise
        collection_response: CollectionResponse = resp.json().get("collections", [])[0]
        return collection_response.get("collection")

    @ensure_authenticated
    @log_action
    def download_file(self, file_path: str, local_filename: str) -> bool:
        url = "/".join((self.BASE_URL, "v2", "dataObject", file_path, "download"))
        _logger.warning(f"Making requests to {url}")
        resp = requests.post(url, headers=self._token_headers(), json={})
        resp.raise_for_status()
        with open(local_filename, "wb") as f:
            f.write(resp.content)
        return True

    def _token_headers(self) -> Dict[str, str]:
        headers = {"Authorization": f"Bearer {self._token}"}
        return headers

    def _login_headers(self) -> HTTPBasicAuth:
        username = os.getenv('MODAC_USER')
        password = os.getenv('MODAC_PASS')
        if not username or not password:
            _logger.warning(
                "Define your MODAC username by setting MODAC_USER='my-username'\nAlternatively, you can call os.environ['MODAC_USER'] = 'my-username'"
            )
            _logger.warning(
                "Define your MODAC password by setting MODAC_PASS='my-password'\nAlternatively, you can call os.environ['MODAC_PASS'] = 'my-password'"
            )
            raise Exception("Undefined username and/or password")
        return HTTPBasicAuth(username=username, password=password)

    @ensure_authenticated
    @log_action
    def download_all_files_in_collection(
        self, path: str, download_sub_collection: bool = False
    ) -> None:
        collection = self.get_collection(path)
        if collection is not None:
            collection_name = collection["collectionName"].split("/")[-1]
            # Create directory for collection
            if not os.path.exists(collection_name):
                os.makedirs(collection_name)

            # Extract data object paths
            data_objects = collection.get("dataObjects", [])

            for data_object in data_objects:
                file_path = data_object.get("path")
                if file_path:
                    local_filename = os.path.join(collection_name, file_path.split("/")[-1])
                    self.download_file(file_path, local_filename)
                    _logger.info(f"Downloaded: {local_filename}")

            if download_sub_collection:
                # Extract sub-collection paths and recursively download their files
                sub_collections = collection.get("subCollections", [])
                for sub_collection in sub_collections:
                    sub_collection_path = sub_collection.get("path")
                    if sub_collection_path:
                        self.download_all_files_in_collection(sub_collection_path, True)

