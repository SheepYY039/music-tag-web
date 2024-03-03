import base64
import os

from mutagen.flac import VCFLACDict
from mutagen.id3 import ID3

from applications.task.utils import detect_language
from component import music_tag


class MusicIDS:
    def __init__(self, folder=None, file=None):
        if folder:
            folder = folder.encode("utf-8", "replace").decode()
            self.file = music_tag.load_file(folder)
            self.path = folder
        elif file:
            folder = file.filename.encode("utf-8", "replace").decode()
            self.file = file
            self.path = folder
        self.artwork_w = 0
        self.artwork_h = 0
        self.artwork_size = 0

    @property
    def album_name(self):
        album_name = self.file["album"].value
        album_name = album_name.replace(" ", "")
        if not album_name:
            album_name = "未知专辑"
        return self.file["album"].value

    @property
    def album(self):
        album_name = self.file["album"].value
        album_name = album_name.replace(" ", "")
        if not album_name:
            return ""
        return self.file["album"].value

    @property
    def album_type(self):
        try:
            if isinstance(self.file.mfile.tags, VCFLACDict):
                return self.file.mfile.tags.get("RELEASETYPE")[0]
            elif isinstance(self.file.mfile.tags, ID3):
                return self.file.mfile.tags.get("TXXX:MusicBrainz Album Type").text[0]
            else:
                return ""
        except Exception:
            return ""

    @property
    def album_artist(self):
        return self.file["albumartist"].value

    @property
    def artist_name(self):
        return self.file["artist"].value

    @property
    def artist(self):
        return self.file["artist"].value

    @property
    def year(self):
        try:
            year = self.file["year"].value
        except Exception:
            return 0
        try:
            year = int(year)
        except Exception:
            year_list = year.split("-")
            if year_list and year_list[0]:
                try:
                    return int(year_list[0].replace(" ", ""))
                except Exception:
                    return 0
        return year

    @property
    def genre(self):
        genre = self.file["genre"].value
        if genre:
            genre = genre.upper()
        else:
            genre = "未知"
        return genre

    @property
    def comment(self):
        return self.file["comment"].value

    @property
    def lyrics(self):
        return self.file["lyrics"].value

    @property
    def duration(self):
        return round(self.file["#length"].value, 2)

    @property
    def size(self):
        return round(os.path.getsize(self.path) / 1024 / 1024, 2)

    @property
    def suffix(self):
        return self.file["#codec"].value

    @property
    def bit_rate(self):
        return int(self.file["#bitrate"].value / 1000)

    @property
    def track_number(self):
        try:
            return self.file["tracknumber"].value
        except Exception:
            return self.file.mfile.tags["tracknumber"][0]

    @property
    def disc_number(self):
        try:
            return self.file["discnumber"].value
        except Exception:
            return self.file.mfile.tags["discnumber"][0]

    @property
    def title(self):
        return self.file["title"].value

    @property
    def artwork(self):
        try:
            bs64_img = ""
            artwork = self.file["artwork"].values
            if artwork:
                if isinstance(artwork[0], bytes):
                    # eval_artwork = literal_eval(artwork[0])
                    # with open("test.xmp", "wb") as f:
                    #     f.write(artwork[0])
                    bs64_img = base64.b64encode(artwork[0]).decode()

                else:
                    zip_img = artwork[0].raw_thumbnail([128, 128])
                    bs64_img = base64.b64encode(zip_img).decode()
                    self.artwork_w = artwork[0].width
                    self.artwork_h = artwork[0].height
                    self.artwork_size = round(len(artwork[0].raw) / 1024 / 1024, 2)
            return "data:image/jpeg;base64," + bs64_img
        except Exception as e:
            print(e)
            return ""

    @property
    def file_name(self):
        return os.path.basename(self.path)

    @property
    def language(self):
        try:
            if isinstance(self.file.mfile.tags, VCFLACDict):
                language = self.file.mfile.tags.get("LANGUAGE")[0]
            elif isinstance(self.file.mfile.tags, ID3):
                language = self.file.mfile.tags.get("TXXX:LANGUAGE").text[0]
            else:
                language = ""
        except Exception:
            language = ""
        if language:
            return language
        else:
            try:
                return detect_language(self.lyrics)
            except Exception:
                return ""

    def to_dict(self):
        return {
            "year": self.year,
            "comment": self.comment,
            "lyrics": self.lyrics,
            "duration": self.duration,
            "size": self.size,
            "bit_rate": self.bit_rate,
            "tracknumber": self.track_number,
            "discnumber": self.disc_number,
            "artwork": self.artwork,
            "artwork_w": self.artwork_w,
            "artwork_h": self.artwork_h,
            "artwork_size": self.artwork_size,
            "title": self.title or self.file_name.split(".")[0],
            "artist": self.artist,
            "album": self.album,
            "album_type": self.album_type,
            "genre": self.genre,
            "filename": self.file_name,
            "albumartist": self.album_artist,
            "language": self.language,
        }

    def var_dict(self):
        return {
            "title": self.title or self.file_name.split(".")[0],
            "artist": self.artist,
            "albumartist": self.album_artist,
            "discnumber": self.disc_number,
            "tracknumber": self.track_number,
            "album": self.album,
            "filename": self.file_name,
        }
