"""Utility functions"""

import subprocess
import logging
import sys

import xxhash


PV_TYPE_VIRTBLOCK = "virtblock"
PV_TYPE_SUBVOL = "subvol"


class CommandException(Exception):
    """Custom exception for command execution"""
    def __init__(self, ret, out, err):
        self.ret = ret
        self.out = out
        self.err = err
        msg = "[%d] %s %s" % (ret, out, err)
        super().__init__(msg)


def get_volname_hash(volname):
    """XXHash based on Volume name"""
    return xxhash.xxh64_hexdigest(volname)


def get_volume_path(voltype, volhash, volname):
    """Volume path based on hash"""
    return "%s/%s/%s/%s" % (
        voltype,
        volhash[0:2],
        volhash[2:4],
        volname
    )


def execute(*cmd):
    """
    Execute command. Returns output and error.
    Raises CommandException on error
    """
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise CommandException(proc.returncode, out.strip(), err.strip())
    return (out.strip(), err.strip())


def logf(msg, **kwargs):
    """Formats message for Logging"""
    if kwargs:
        msg += "\t"

    for msg_key, msg_value in kwargs.items():
        msg += " %s=%s" % (msg_key, msg_value)

    return msg


def logging_setup():
    """Logging Setup"""
    root = logging.getLogger()
    # verbose = os.environ.get("VERBOSE", False)
    verbose = True
    root.setLevel(logging.INFO)
    if verbose:
        root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    if verbose:
        handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s "
                                  "[%(module)s - %(lineno)s:%(funcName)s] "
                                  "- %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)