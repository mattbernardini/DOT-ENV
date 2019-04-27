"""Flags which will be nearly universal across models."""

from __future__ import absolute_import, division, print_function

from absl import flags

from ._conventions import help_wrap

def mail_server(email = True, alias = True, config = True, relay = True, debug = True):
    key_flags = []

    if email:
        flags.define

def _email(add = True, update = True, delete = True, restrict = True, list = True):
    key_flags = []
    if add:
        flags.DEFINE_list(
            name="email-add", short_name="ea", default="",
            help=help_wrap("Used to add emails to the server."
            " Must be a csv list with name and passwords appearing after eachother."
            "i.e. foo@bar.com, this_is_a_password, paz@bar.com, this_is_another_pw")
        )
        key_flags.append("email-add")
    if update:
        flags.DEFINE_list(
            name="email-update", short_name="ed", default="",
            help=help_wrap("Used to update emails to the server."
            " Must be a csv list with name and passwords appearing after eachother."
            "i.e. foo@bar.com, this_is_a_password, paz@bar.com, this_is_another_pw")
        )
        key_flags.append("email-update")
    if delete:
        flags.DEFINE_list(
            name="email-delete", short_name="el", default="",
            help=help_wrap("Used to delete emails to the server."
            " Must be a csv list with name and passwords appearing after eachother."
            "i.e. foo@bar.com, paz@bar.com")
        )

