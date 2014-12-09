
AppDynamics Download Robot
==========================

## SYNOPSIS

    download.py [options] product_name


## DESCRIPTION

`download.py` is a tool to automate downloading product releases from the
AppDynamics web site. It automates the entire process for you:

* opening a connection to [http://download.appdynamics.com](),
* logging into the Single Sign-On (SSO) server,
* selecting the product zone (SaaS or on-premise), 
* selecting the product version,
* downloading the product, and
* verifying the SHA256 hash to ensure a clean download. 


## PRODUCT NAMES

The optional arguments must be followed by one or more product names to download. The script is capable of downloading the following products:

`java-agent`
: App Server Agent for Java (Oracle and JRockit JVM's)

`ibm-agent`
: App Server Agent for Java (IBM JVM)

`dotnet-agent`
: App Server Agent for .NET

`php-agent`
: App Server Agent for PHP

`machine-agent`
: Standalone Machine Agent

`controller`
: AppDynamics controller

`euem-processor`
: On-premise EUEM collector

`geo-server`
: On-premise Geo Server

`ad4db`
: AppDynamics for Databases server

`ios-agent`
: SDK for Apple iOS devices

`android-agent`
: SDK for Android devices

_NOTE_: The Node.js agent is not included because it is normally downloaded with `npm`.


## OPTIONS

`-u` _username_, `--username` _username_
:                       Account name to be used for AppDynamics Single 
                        Sign-On (SSO) authentication.

`-p` _password_, `--password` _password_
:                       Password for SSO login.

`-b` {32,64}, `--bits` {32,64}
:                       Request 32-bit or 64-bit version of the product.
                        Defaults to 64-bit.

`-s` {linux,windows}, `--os` {linux,windows}
:                       Operating system platform.

`-f` {tar,rpm}, `--format` {tar,rpm}
:                       Packaging format for Linux downloads. Currently only
                        affects the PHP agent, which is available in tar and
                        rpm formats.

`-z` {saas,on-premise}, `--zone` {saas,on-premise}
:                       Specify the download zone. Currently this script only
                        supports the "saas" and "on-premise" zones.

`-v` version, `--version=` version
:                       Product version to download. Default: latest version
                        available.

`-o` output, `--output=` output
:                       Path to save downloaded file. If the target is a
                        directory, the original filename will be appended.
                        
`-h`, `--help`
:            Show this help message and exit

`-q`, `--quiet`
:           Skip display of progress and status.

`-d`, `--debug`
:           Display debugging information about HTTP connections,
                        cookies, etc.

`-n`, `--no-download`
:     Don't download the file, just display the actions to
                        be taken.
                        
                        
## EXAMPLES

`./download.py -u tradel@appdynamics.com -p xxxxxxxx java-agent`
: Download a copy of the latest version of the Java agent.

`./download.py -u tradel@appdynamics.com -p xxxxxxxx -v 3.7.17 java-agent`
: Download version 3.7.17 of the Java agent.

`./download.py -u tradel@appdynamics.com -p xxxxxxxx -o foo.zip java-agent`
: Download the latest Java agent, and save the file as `foo.zip`.

`./download.py -u tradel@appdynamics.com -p xxxxxxxx -b64 -f rpm php-agent`
: Download the latest 64-bit PHP agent in RPM package format.

`./download.py -u tradel@appdynamics.com -p xxxxxxxx --os=windows controller`
: Download the latest controller for Windows.

`./download.py -n -q -u tradel@appdynamics.com -p xxxxxxxx --os=windows controller`
: Don't download anything, just print the URL where version 3.9.5 of the
  controller can be found.
  

## SAMPLE OUTPUT

    bash% ./download.py -u tradel@appdynamics.com -p xxxxxxxx java-agent
    Checking available product versions . . .
    Listing available files . . .
    Downloading file checksums . . .
    AppServerAgent-3.9.6.0.zip [=========================] 100% |   9.4MB |   326KBps
    AppServerAgent-3.9.6.0.zip saved to ./AppServerAgent-3.9.6.0.zip
    
    Done!
    Saving cookies to /Users/tradel/.cookiejar . . .


## REQUIREMENTS

`download.py` requires 2.6 or later. It has been tested with 2.6 and 2.7. It has not been tested with python3.

The following modules are required:

 * [Argparse](https://pypi.python.org/pypi/argparse)
 * [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
 * [Mechanize](https://pypi.python.org/pypi/mechanize)

The easiest way to install the prerequisites is with `pip`:

    pip install -r requirements.txt

## AUTHORS

Todd Radel (<tradel@appdynamics.com>)