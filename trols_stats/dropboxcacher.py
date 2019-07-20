"""DropBox support.

"""
import contextlib
import time
import dropbox
import logging


class DropBoxCacher(object):
    """

    """
    def __init__(self, token):
        """A :class:`dropbox.Dropbox`

        """
        self.__dbx = dropbox.Dropbox(token)

    def list_folder(self, path):
        """List a folder.

        Return a dict mapping unicode filenames to
        FileMetadata|FolderMetadata entries.

        """
        source_path = path
        if source_path[0] != '/':
            source_path = '/' + source_path

        files = {}
        try:
            with self.stopwatch('list_folder'):
                res = self.__dbx.files_list_folder(source_path)
        except dropbox.exceptions.ApiError as err:
            logging.error('Folder listing failed for "%s": %s', source_path, err)
        else:
            for entry in res.entries:
                files[entry.name] = entry

        return files

    @staticmethod
    @contextlib.contextmanager
    def stopwatch(message):
        """Context manager to print how long a block of code took.

        """
        time_start = time.time()
        try:
            yield
        finally:
            time_end = time.time()
        logging.info('Total elapsed time for %s: %.3fs', message, time_end - time_start)
