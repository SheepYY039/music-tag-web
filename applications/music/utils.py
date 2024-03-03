import os
import urllib.parse
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible


def get_file_path(instance, filename):
    return ChunkedPath("attachments")(instance, filename)


@deconstructible
class ChunkedPath:
    def sanitize_filename(self, filename):
        return filename.replace("/", "-")

    def __init__(self, root, preserve_file_name=True):
        self.root = root
        self.preserve_file_name = preserve_file_name

    def __call__(self, instance, filename):
        self.sanitize_filename(filename)
        uid = str(uuid.uuid4())
        chunk_size = 2
        chunks = [uid[i : i + chunk_size] for i in range(0, len(uid), chunk_size)]
        if self.preserve_file_name:
            parts = chunks[:3] + [filename]
        else:
            ext = os.path.splitext(filename)[1][1:].lower()
            new_filename = "".join(chunks[3:]) + f".{ext}"
            parts = chunks[:3] + [new_filename]
        return os.path.join(self.root, *parts)


def strip_absolute_media_url(path):
    if (
        settings.MEDIA_URL.startswith("http://")
        or settings.MEDIA_URL.startswith("https://")
        and path.startswith(settings.MEDIA_URL)
    ):
        path = path.replace(settings.MEDIA_URL, "/media/", 1)
    return path


def get_file_path_view(audio_file):
    # serve_path = settings.MUSIC_DIRECTORY_SERVE_PATH
    # prefix = settings.MUSIC_DIRECTORY_PATH
    serve_path = ""
    prefix = ""
    t = settings.REVERSE_PROXY_TYPE
    if t == "nginx":
        # we have to use the internal locations
        try:
            path = audio_file.url
            path = path.replace("/attachments", "", 1)
        except AttributeError:
            # a path was given
            if not serve_path or not prefix:
                raise ValueError(
                    "You need to specify MUSIC_DIRECTORY_SERVE_PATH and "
                    "MUSIC_DIRECTORY_PATH to serve in-place imported files"
                )
            path = "/music" + audio_file.replace(prefix, "", 1)
        path = strip_absolute_media_url(path)
        if path.startswith("http://") or path.startswith("https://"):
            protocol, remainder = path.split("://", 1)
            hostname, r_path = remainder.split("/", 1)
            r_path = urllib.parse.quote(r_path)
            path = protocol + "://" + hostname + "/" + r_path
            return (settings.PROTECT_FILES_PATH + "/media/" + path).encode("utf-8")
        # needed to serve files with % or ? chars
        path = urllib.parse.quote(path)
        return path.encode("utf-8")
    if t == "apache2":
        try:
            path = audio_file.path
        except AttributeError:
            # a path was given
            if not serve_path or not prefix:
                raise ValueError(
                    "You need to specify MUSIC_DIRECTORY_SERVE_PATH and "
                    "MUSIC_DIRECTORY_PATH to serve in-place imported files"
                )
            path = audio_file.replace(prefix, serve_path, 1)
        path = strip_absolute_media_url(path)
        return path.encode("utf-8")
