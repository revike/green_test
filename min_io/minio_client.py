import urllib3
from minio import Minio

# from core.config import SERVER_MIN_IO, PORT_MIN_IO, ACCESS_KEY_MIN_IO, \
#     SECRET_KEY_MIN_IO
from env_min_io import SERVER_MIN_IO, PORT_MIN_IO, ACCESS_KEY_MIN_IO, \
    SECRET_KEY_MIN_IO

client = Minio(
    f"{SERVER_MIN_IO}:{PORT_MIN_IO}",
    access_key=ACCESS_KEY_MIN_IO,
    secret_key=SECRET_KEY_MIN_IO,
    secure=False,
    http_client=urllib3.ProxyManager(
        f"http://{SERVER_MIN_IO}:{PORT_MIN_IO}/",
        timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
        cert_reqs="CERT_REQUIRED",
        retries=urllib3.Retry(
            total=5,
            backoff_factor=0.2,
            status_forcelist=[500, 502, 503, 504],
        ),
    ),
)
