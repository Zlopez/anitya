# -*- coding: utf-8 -*-

"""
(c) 2014-2020 - Copyright Red Hat Inc

Authors:
  Pierre-Yves Chibon <pingou@pingoured.fr>
  Ralph Bean <rbean@redhat.com>
  Michal Konecny <mkonecny@redhat.com>

"""

from anitya.lib import xml2dict
from anitya.lib.backends import BaseBackend
from anitya.lib.exceptions import AnityaPluginException


def _get_versions(url):
    """Retrieve the versions for the provided url."""
    try:
        req = PearBackend.call_url(url)
    except Exception as err:  # pragma: no cover
        raise AnityaPluginException(f"Could not contact {url}") from err

    data = req.text
    versions = []
    for line in data.split("\n"):
        if "<v>" in line and "</v>" in line:
            version = line.split("v>", 2)[1].split("</")[0]
            versions.append(version)
    return versions


class PearBackend(BaseBackend):
    """The custom class for projects hosted on pear.php.net.

    This backend allows to specify a version_url and a regex that will
    be used to retrieve the version information.
    """

    name = "PEAR"
    examples = [
        "https://pear.php.net/package/Auth/",
        "https://pear.php.net/package/PHP_UML",
    ]

    @classmethod
    def get_version(cls, project):
        """Method called to retrieve the latest version of the projects
        provided, project that relies on the backend of this plugin.

        :arg Project project: a :class:`anitya.db.models.Project` object whose backend
            corresponds to the current plugin.
        :return: the latest version found upstream
        :return type: str
        :raise AnityaPluginException: a
            :class:`anitya.lib.exceptions.AnityaPluginException` exception
            when the version cannot be retrieved correctly

        """
        return cls.get_versions(project)[0]

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
        name = project.name.lower()
        url_template = "https://pear.php.net/rest/r/%(name)s/allreleases.xml"

        if "-" in name:
            name = name.replace("-", "_")

        url = url_template % {"name": name}

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
        versions = []
        versions = _get_versions(url)

        if not versions:
            raise AnityaPluginException(f"No versions found for {project.name.lower()}")

        # Filter retrieved versions
        filtered_versions = cls.filter_versions(versions, project.version_filter)

        return filtered_versions

    @classmethod
    def check_feed(cls):
        """Return a generator over the latest 10 uploads to PEAR

        by querying an RSS feed.
        """

        url = "https://pear.php.net/feeds/latest.rss"

        try:
            response = cls.call_url(url)
        except Exception as err:  # pragma: no cover
            raise AnityaPluginException(f"Could not contact {url}") from err

        try:
            parser = xml2dict.XML2Dict()
            data = parser.fromstring(response.text)
        except Exception as err:  # pragma: no cover
            raise AnityaPluginException(f"No XML returned by {url}") from err

        items = data["RDF"]["item"]
        for entry in items:
            title = entry["title"]["value"]
            name, version = title.rsplit(None, 1)
            homepage = f"https://pear.php.net/package/{name}"  # noqa: E231
            yield name, homepage, cls.name, version
