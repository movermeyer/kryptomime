# -*- coding: utf-8 -*-
#
# EMail kryptography support
#
# This file is part of kryptomime, a Python module for email kryptography.
# Copyright © 2013-2015 Thomas Tanner <tanner@gmx.net>
# 
# This library is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the included GNU Lesser General
# Public License file for details.
# 
# You should have received a copy of the GNU General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.
# For more details see the file COPYING.

from .core import KeyMissingError
from .mail import create_mail, protect_mail

# semantic version:
# major (backwards incompatible if >1),
# minor (backwards compatible, feature-level),
# implementation (bugfixes)
version = (0,5,0)
