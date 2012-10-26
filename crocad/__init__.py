#!python
# -*- coding: utf-8 -*-
#
# This file is part of Crochet CAD, a library and script for generating
# crochet patterns for simple 3D shapes.
#
# Copyright (C) 2010, 2011 Mark Smith <mark.smith@practicalpoetry.co.uk>
#
# Crochet CAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
crocad - A Python library for generating crochet patterns.

This module provides `main`, which is the entry-point for command-line
execution of the module's functionality.
"""

import logging
import sys

import gettext
import locale

class NullHandler(logging.Handler):
    """
    A Handler that does nothing. Prevents error messages if crocad is used
    as a library and logging is not configured.
    """
    def emit(self, record):
        """Do nothing."""
        pass
logging.getLogger('crocad').addHandler(NullHandler())

from crocad import donut, ball, cone


__all__ = ['main']


LOG = logging.getLogger('crocad')


COMMAND_ALIASES = {
    'torus': 'donut',
    'sphere': 'ball',
}


def find_command(command):
    """
    Attempts to find an imported module with the name `command`, and then
    obtains and returns that moule's `main` function.
    """
    command = COMMAND_ALIASES.get(command, command)
    
    command_module = globals().get(command)
    if hasattr(command_module, 'main'):
        return getattr(command_module, 'main')
    else:
        raise Exception('Unknown command: %s' % command)

def init_localization():
	"""Prepare localization"""
	locale.setlocale(locale.LC_ALL, '')
	
	loc = locale.getlocale()
	filename = "res/messages_%s.mo" & locale.getlocale()[0][0:2]
	
	try:
		logging.debug("Opening message file %s for locale %s", filename, loc[0])
		trans = gettext.GNUTranslations(open(filename, "rb"))
	except IOError:
		logging.debug("Locale not found. Using default messages.")
		trans = gettext.NullTranslations()
	
	trans.install()	
	

def main(argv=sys.argv[1:]):
    """ Crochet CAD's command-line entry-point. """
    import optparse
    
    opt_parser = optparse.OptionParser("""%prog [-va] COMMAND [COMMAND-OPTIONS]
  
Help:
  %prog --help
  %prog COMMAND --help""",
description="""
Generate a crochet pattern for a geometric primitive, specified as COMMAND.
Supported commands are 'ball', 'donut', and 'cone'. For details of options for a
specific command, run '%prog COMMAND --help' with the name of the command.
""".strip()
)
    opt_parser.disable_interspersed_args()
    
    optgroup = optparse.OptionGroup(opt_parser, (_('Global Options'),
    _('Global options must be provided before the name of the crochet-cad'
    ' command. They can be used for any crochet-cad command.')))
    optgroup.add_option(_('-v'), _('--verbose'), action='count', default=0,
        help=_('print out extra information - only really used for debugging.'))
    optgroup.add_option(_('-a'), _('--accurate'), action='store_true', default=False,
        help=_('generate an exact pattern'
        ' which may not produce such an even end-product.'))
    optgroup.add_option(_('-i'), _('--inhuman'), action='store_true', default=False,
        help=_('Instead of printing instructions, just print the row-counts,'
        ' one per line.'))
    opt_parser.add_option_group(optgroup)
    
    global_options, args = opt_parser.parse_args(argv)
    
    logging.basicConfig()
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
    if global_options.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif global_options.verbose > 1:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if args:
        command = args.pop(0)
        find_command(command)(args, global_options)
    else:
        opt_parser.error(_('No command was provided.'))


if __name__ == '__main__':
    init_localization()
    main()
