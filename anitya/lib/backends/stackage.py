# -*- coding: utf-8 -*-

"""
(c) 2015 - Copyright Red Hat Inc
Authors:
  Jens Petersen <petersen@redhat.com>
"""


from anitya.lib.backends import BaseBackend, get_versions_by_regex


class StackageBackend(BaseBackend):
    """The custom class for Haskell projects hosted on Stackage.org.
    This backend allows to specify a version_url and a regex that will
    be used to retrieve the version information.
    """

    name = "Stackage"
    examples = [
        "https://www.stackage.org/package/conduit",
        "https://www.stackage.org/package/cabal-install",
    ]

    @classmethod
    def get_version_url(cls, project):
        """Method called to retrieve the url used to check for new version
        of the project provided, project that relies on the backend of this plugin.

        Attributes:
            project (:obj:`anitya.db.models.Project`): Project object whose backend
                corresponds to the current plugin.

        Returns:
            str: url used for version checking
        """
        url = f"https://www.stackage.org/package/{project.name}"  # noqa: E231

        return url

    @classmethod
    def get_versions(cls, project):
        """Method called to retrieve all the versions (that can be found)
        of the projects provided, project that relies on the backend of
        this plugin.
        :arg Project project: a :class:`anitya.db.models.Project` object whose backend
            corresponds to the current plugin.
        :return: a list of all the possible releases found
        :return type: list
        :raise AnityaPluginException: a
            :class:`anitya.lib.exceptions.AnityaPluginException` exception
            when the versions cannot be retrieved correctly
        """
        url = cls.get_version_url(project)

        regex = (
            rf"<a href=\"https://hackage.haskell.org/package/{project.name}\">"  # noqa: E231
            r"<span class=\"version\">([\d.]*).*</span></a>"
        )

        return get_versions_by_regex(url, regex, project)

    @classmethod
    def check_feed(cls):  # pragma: no cover
        """Method called to retrieve the latest uploads to a given backend,
        via, for example, RSS or an API.

        Not Supported

        Returns:
            :obj:`list`: A list of 4-tuples, containing the project name, homepage, the
            backend, and the version.

        Raises:
             NotImplementedError: If backend does not
                support batch updates.

        """
        raise NotImplementedError()
