import dropbox
import os


token = os.getenv('DROPBOX_TOKEN')
dbx = dropbox.Dropbox(token)


def save_on_dropbox(phone_number, file_url, extension):
    file_name = file_url[file_url.rfind('/')+1:]
    file_path = f'/{phone_number}/{file_name}.{extension}'
    # format: /+490001112223/257fd737153797c6681fbd43387e4d49.jpeg
    # more on result:
    # https://dropbox-sdk-python.readthedocs.io/en/latest/api/files.html#dropbox.files.SaveUrlResult
    return dbx.files_save_url(file_path, file_url)


def dropbox_folder_from(phone_number):
    path = f'/{phone_number}'
    folder_url = None
    try:
        link = dbx.sharing_create_shared_link_with_settings(path)
        folder_url = link.url
    except dropbox.exceptions.ApiError as exception:
        if exception.error.is_shared_link_already_exists():
            link = dbx.sharing_get_shared_links(path)
            folder_url = link.links[0].url
    return folder_url
