==========================
AppDynamics Download Robot
==========================

Current version: 0.1.4
Released: 23-Jun-2015

.. image:: https://img.shields.io/travis/tradel/appd-download-bot.svg
   :target: https://travis-ci.org/tradel/appd-download-bot/

.. image:: https://img.shields.io/pypi/dm/AppDynamicsDownloader.svg
   :target: https://pypi.python.org/pypi/AppDynamicsDownloader/


SYNOPSIS
--------

::

    download-appdynamics [options] product_name

DESCRIPTION
-----------

``download-appdynamics`` is a tool to automate downloading product releases from
the AppDynamics web site. It automates the entire process for you:

-  opening a connection to `<http://download.appdynamics.com>`__,
-  logging into the Single Sign-On (SSO) server,
-  selecting the product zone (SaaS or on-premise),
-  selecting the product version,
-  downloading the product, and
-  verifying the SHA256 hash to ensure a clean download.

PRODUCT NAMES
-------------

The optional arguments must be followed by one or more product names to
download. The script is capable of downloading the following products:

+-------------------------+----------------------------------------------------+
| Product Name            | Description                                        |
+=========================+====================================================+
| ``java-agent``          | App Server Agent for Java (Oracle and JRockit      |
|                         | JVM's)                                             |
+-------------------------+----------------------------------------------------+
| ``ibm-agent``           | App Server Agent for Java (IBM JVM)                |
+-------------------------+----------------------------------------------------+
| ``dotnet-agent``        | App Server Agent for .NET                          |
+-------------------------+----------------------------------------------------+
| ``php-agent``           | App Server Agent for PHP                           |
+-------------------------+----------------------------------------------------+
| ``machine-agent``       | Standalone Machine Agent                           |
+-------------------------+----------------------------------------------------+
| ``controller``          | AppDynamics controller                             |
+-------------------------+----------------------------------------------------+
| ``euem-processor``      | On-premise EUEM collector                          |
+-------------------------+----------------------------------------------------+
| ``geo-server``          | On-premise Geo Server                              |
+-------------------------+----------------------------------------------------+
| ``ad4db``               | AppDynamics for Databases server                   |
+-------------------------+----------------------------------------------------+
| ``dbagent``             | AppDynamics integrated database agent              |
+-------------------------+----------------------------------------------------+
| ``events-service``      | Events service for analytics                       |
+-------------------------+----------------------------------------------------+
| ``analytics-processor`` | On-premise analytics processor                     |
+-------------------------+----------------------------------------------------+
| ``analytics-agent``     | Analytics agent extension                          |
+-------------------------+----------------------------------------------------+
| ``ios-agent``           | SDK for Apple iOS devices                          |
+-------------------------+----------------------------------------------------+
| ``android-agent``       | SDK for Android devices                            |
+-------------------------+----------------------------------------------------+

*NOTE*: The Node.js agent is not included because it is normally
downloaded with ``npm``.

OPTIONS
-------

``-u`` *username*, ``--username`` *username*
    Account name to be used for AppDynamics Single Sign-On (SSO) authentication.

``-p`` *password*, ``--password`` *password*
    Password for SSO login.

``-b`` {32,64}, ``--bits`` {32,64}
    Request 32-bit or 64-bit version of the product. Defaults to 64-bit.

``-s`` {linux,windows}, ``--os`` {linux,windows,mac}
    Operating system platform.

``-f`` {tar,rpm}, ``--format`` {tar,rpm}
    Packaging format for Linux downloads. Currently only affects the PHP agent, 
    which is available in tar and rpm formats.

``-z`` {saas,on-premise}, ``--zone`` {saas,on-premise}
    Specify the download zone. Currently this script only supports the 
    "saas" and "on-premise" zones.

``-v`` version, ``--version=`` version
    Product version to download.
    Default: latest version available.

``-o`` output, ``--output=`` output
    Path to save downloaded file. If the target is a directory, 
    the original filename will be appended.

``-h``, ``--help``
    Show this help message and exit

``-q``, ``--quiet``
    Skip display of progress and status.

``-d``, ``--debug``
    Display debugging information about HTTP connections, cookies, etc.

``-n``, ``--no-download``
    Don't download the file, just display the actions to be taken.


EXAMPLES
--------

Download a copy of the latest version of the Java agent::

    download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx java-agent

Download version 3.7.17 of the Java agent::

    download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx -v 3.7.17 java-agent

Download the latest Java agent, and save the file as ``foo.zip``::

    download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx -o foo.zip java-agent

Download the latest 64-bit PHP agent in RPM package format::

    download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx -b64 -f rpm php-agent

Download the latest controller for Windows::

    download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx --os=windows controller

Don't download anything, just print the URL where version 3.9.5 of the controller can be found::

    ./download-appdynamics -n -q -u tradel@appdynamics.com -p xxxxxxxx --os=windows controller


SAMPLE OUTPUT
-------------

::

    bash% ./download-appdynamics -u tradel@appdynamics.com -p xxxxxxxx java-agent
    Checking available product versions . . .
    Listing available files . . .
    Downloading file checksums . . .
    AppServerAgent-3.9.6.0.zip [=========================] 100% |   9.4MB |   326KBps
    AppServerAgent-3.9.6.0.zip saved to ./AppServerAgent-3.9.6.0.zip

    Done!
    Saving cookies to /Users/tradel/.cookiejar . . .


REQUIREMENTS
------------

``download-appdynamics`` requires 2.6 or later. It has been tested with 2.6 and
2.7. It has not been tested with python3.

The following modules are required:

-  `Argparse <https://pypi.python.org/pypi/argparse>`__
-  `BeautifulSoup4 <https://pypi.python.org/pypi/beautifulsoup4>`__
-  `Mechanize <https://pypi.python.org/pypi/mechanize>`__

The easiest way to install the prerequisites is with ``pip``:

::

    pip install -r requirements.txt

AUTHORS
-------

Todd Radel (tradel@appdynamics.com)
