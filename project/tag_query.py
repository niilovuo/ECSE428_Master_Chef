from project.db import TagRepo

def get_all_tags():
    """
    Returns all the tags available on the server

    Returns
    -------
    All the tags
    """

    return TagRepo.select_all()
