import requests
import json

from qib.util import const


def http_put(url: str, headers: dict, body: dict, title: str = None) -> requests.Response:
    """
    Send a HTTP PUT request to the given URL with the given headers and json data.
    (Optionally) Specify a title for logging.
    """
    log_title = f"[{title}] " if title else ""

    retries = 0
    while retries <= const.NW_MAX_RETRIES:
        try:
            response = requests.put(
                url,
                headers = headers,
                json = body,
                timeout = const.NW_TIMEOUT
            )

            # check response status
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise RuntimeError(f"{log_title} HTTP error: {err}")

            # check if offline
            if response.json()['status'] == 'offline':
                raise RuntimeError(f"{log_title} Setup is offline")
        except requests.exceptions.Timeout:
            retries += 1
            print(f"{log_title} Timeout: {retries}/{const.NW_MAX_RETRIES} retries")
            
        # TODO: Process response
        return response

    # check timeout error
    if retries > const.NW_MAX_RETRIES:
        raise RuntimeError(f"{log_title} Timeout error: Max retries exceeded")
