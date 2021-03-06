"""
Auto-auth page (used to automatically log in during testing).
"""

import re
import urllib
from bok_choy.page_object import PageObject
from . import BASE_URL


class AutoAuthPage(PageObject):
    """
    The automatic authorization page.
    When allowed via the django settings file, visiting
    this url will create a user and log them in.
    """

    def __init__(self, browser, username=None, email=None, password=None, staff=None, course_id=None, roles=None):
        """
        Auto-auth is an end-point for HTTP GET requests.
        By default, it will create accounts with random user credentials,
        but you can also specify credentials using querystring parameters.

        `username`, `email`, and `password` are the user's credentials (strings)
        `staff` is a boolean indicating whether the user is global staff.
        `course_id` is the ID of the course to enroll the student in.
        Currently, this has the form "org/number/run"

        Note that "global staff" is NOT the same as course staff.
        """
        super(AutoAuthPage, self).__init__(browser)

        # Create query string parameters if provided
        self._params = {}

        if username is not None:
            self._params['username'] = username

        if email is not None:
            self._params['email'] = email

        if password is not None:
            self._params['password'] = password

        if staff is not None:
            self._params['staff'] = "true" if staff else "false"

        if course_id is not None:
            self._params['course_id'] = course_id

        if roles is not None:
            self._params['roles'] = roles

    @property
    def url(self):
        """
        Construct the URL.
        """
        url = BASE_URL + "/auto_auth"
        query_str = urllib.urlencode(self._params)

        if query_str:
            url += "?" + query_str

        return url

    def is_browser_on_page(self):
        return True

    def get_user_id(self):
        message = self.css_text('BODY')[0].strip()
        match = re.search(r' user_id ([^$]+)$', message)
        return match.groups()[0] if match else None
