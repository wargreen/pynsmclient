Python nsmclient
Version 0.1 - April 2013
Author: Nils Gey ich@nilsgey.de http://www.nilsgey.de  
Non Session Manager Author: Jonathan Moore Liles  <male@tuxfamily.org> http://non.tuxfamily.org/nsm/


[Purpose]

Python nsmclient is a convenience wrapper around liblo and NSM-OSC 
syntax to implement Non Session support easily in your own Python
programs.
You don't need any OSC knowledge to use this package.

[Instructions]

Copy nsmclient.py into your source directory and 
	import nsmclient
	
Then call nsmclient.init() with the correct parameters.
Please see example.py, a well documented, minimal and working example.
Only 30 lines of code. 

The important part is that your application follows the NSM rules
(see example.py documentation and nsm website http://non.tuxfamily.org/nsm/)

[Dependencies]

Non-Session Manager http://non.tuxfamily.org/nsm/
liblo (tested with version 0.26) http://liblo.sourceforge.net/
pyliblo - Python 3 bindings for liblo. (tested with version 0.9.1) http://das.nasophon.de/pyliblo/

[License]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
