import bs4
import mechanize
import hashlib
import re
import sys
import os
import io
import time
import atexit
import events


__author__ = 'tradel'


class Zone(object):
    BASE_URL = 'https://download.appdynamics.com'

    SAAS = 1
    ON_PREMISE = 3

    ZONE_MAP = {'on-premise': 3,
                'saas': 1}

    PRODUCTS = ['controller', 'euem-processor', 'java-agent', 'ibm-agent', 'machine-agent',
                'dotnet-agent', 'php-agent', 'ios-agent', 'android-agent', 'geo-server', 'ad4db',
                'events-service', 'analytics-agent', 'analytics-processor', 'dbagent']

    PRODUCT_MAP = {'controller': 'controller',
                   'euem-processor': 'euem',
                   'dotnet-agent': 'dotNetAgentSetup',
                   'dbagent': 'dbagent',
                   'ad4db': 'AppD-Database',
                   'java-agent': 'AppServerAgent',
                   'ibm-agent': 'AppServerAgent-ibm',
                   'machine-agent': 'MachineAgent',
                   'php-agent': 'appdynamics-php-agent',
                   'ios-agent': 'iOSAgent',
                   'android-agent': 'AndroidAgent',
                   'geo-server': 'GeoServer',
                   'events-service': 'events-service',
                   'analytics-agent': 'analytics-agent',
                   'analytics-processor': 'analytics-processor'}

    PLATFORM_EXT_MAP = {'linux': 'sh',
                        'windows': 'exe',
                        'mac': 'dmg'}

    status = events.Event()
    success = events.Event()
    download_progress = events.Event()

    user_home = os.environ['HOME']
    cookie_fname = os.path.join(user_home, '.cookiejar')

    def __init__(self, zone_id, version=None, username=None, password=None, debug=False, use_cookies=True):
        self._cookie_jar = self._browser = None
        self._zone_id = None  #
        self._version = None  # currently selected version
        self._versions = None  # list of available versions
        self._files = None  # dict of {file, url} available for selected version
        self._checksums = None  # dict of {file, sha256} for available files
        self.debug = debug
        self.use_cookies = use_cookies
        self.username = username
        self.password = password

        self.zone_id = zone_id
        self.version = version

    @property
    def cookie_jar(self):
        cj = getattr(self, '_cookie_jar', None)

        if cj is None:
            cj = mechanize.LWPCookieJar(Zone.cookie_fname)

            if self.use_cookies:
                try:
                    cj.load()
                except IOError:
                    pass

            def save_cookies():
                if self.use_cookies:
                    Zone.status(self, "Saving cookies to " + Zone.cookie_fname)
                    cj.save()
                    Zone.success(self)

            atexit.register(save_cookies)
            self._cookie_jar = cj

        return cj

    @property
    def browser(self):
        b = getattr(self, '_browser', None)

        if b is None:
            b = mechanize.Browser()
            b.set_handle_robots(False)
            b.set_debug_http(self.debug)
            b.set_cookiejar(self.cookie_jar)
            b.addheaders = [("User-agent", "Mozilla/5.0 (compatible; DownloadAutomator/0.1)"),
                            ("From", self.username)]
            self._browser = b

            if self.debug:
                b.set_debug_http(True)
                b.set_debug_redirects(True)
                b.set_debug_responses(True)

        return b

    @property
    def zone_id(self):
        return self._zone_id

    @zone_id.setter
    def zone_id(self, z):
        if isinstance(z, str):
            z = Zone.ZONE_MAP[z]
        self._zone_id = z

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, ver):
        if ver is not None:
            avail_versions = self.get_versions()
            if ver == 'latest':
                ver = avail_versions[0]
            else:
                if ver not in avail_versions:
                    raise ValueError('{0} is not in the list of available download versions'.format(ver))

        self._version = ver

    def _open_url(self, url):
        browser = self.browser
        browser.open(url)

        assert self.username is not None, 'Username must be supplied'
        assert self.password is not None, 'Password must be supplied'

        # if we get redirected to the SSO login page, fill it in and submit the form:
        if "login" in browser.geturl():
            browser.select_form(nr=0)
            browser.form['username'] = self.username
            browser.form['password'] = self.password
            browser.submit()

        return browser

    def get_versions(self):
        versions = getattr(self, '_versions', None)

        if versions is None:
            versions = []

            Zone.status(self, 'Checking available product versions')

            browser = self._open_url('{0}/browse/zone/{1}/'.format(self.BASE_URL, self.zone_id))

            soup = bs4.BeautifulSoup(browser.response().read())
            dropdown = soup.find('table', id='version_disp').find('select')
            for opt in dropdown.find_all('option'):
                if re.match(r'[0-9]+', opt['value']):
                    versions.append(opt['value'])

            self._versions = versions
            Zone.success(self)

        return versions

    def _get_file_url(self, filename):
        files = getattr(self, '_files', None)

        if files is None:

            Zone.status(self, 'Listing available files')

            browser = self._open_url('{0}/browse/zone/{1}/?version={2}'.format(self.BASE_URL,
                                                                               self.zone_id, self.version))

            files = {}
            for link in browser.links():
                attrs = {}
                for (x, y) in link.attrs:
                    attrs[x] = y
                # attrs = {x: y for (x, y) in link.attrs}
                if link.url == '#' and 'onclick' in attrs and 'link_check' in attrs['onclick']:
                    m = re.match(r"link_check\('(.*)'\);return false;", attrs['onclick'])
                    files[link.text] = Zone.BASE_URL + m.group(1)

            self._files = files
            Zone.success(self)

        return files[filename]

    def _get_file_checksum(self, filename):
        sums = getattr(self, '_checksums', None)

        if sums is None:

            url = self._get_file_url('sha256sum.txt')

            Zone.status(self, 'Downloading file checksums')

            response = self.browser.open(url)
            sums = {}
            for line in response.xreadlines():
                (sha256, fname) = line.rstrip().split()
                sums[fname] = sha256

            response.close()
            self._checksums = sums
            Zone.success(self)

        return sums[filename]

    def download_file(self, filename, output='.'):

        target = output
        if os.path.isdir(target):
            target = os.path.join(target, filename)

        url = self._get_file_url(filename)
        true_hash = self._get_file_checksum(filename)

        Zone.status(self, 'Starting download of ' + filename)
        now = time.time()

        response = self.browser.open(url)
        total_bytes = long(response.info()['Content-length'])

        with io.open(target, 'wb') as f:
            hasher = hashlib.sha256()
            while True:
                args = {'filename': filename, 'target': target, 'url': url,
                        'start_time': now, 'now_time': time.time(),
                        'true_hash': true_hash, 'calc_hash': hasher.hexdigest(),
                        'bytes_read': response.tell(), 'total_bytes': total_bytes}
                Zone.download_progress(self, args)

                data = response.read(io.DEFAULT_BUFFER_SIZE)
                if not data:
                    break
                hasher.update(data)
                f.write(data)

        response.close()

        if hasher.hexdigest() != true_hash:
            print >> sys.stderr, "Error: sha256 hash of downloaded file does " + \
                                 "not match expected, " + hasher.hexdigest() + " != " + true_hash
            os.remove(target)

        Zone.success(self)
        return target

    @staticmethod
    def _validate_product(product, platform='linux', bits=64, package='rpm'):
        if isinstance(bits, str):
            bits = int(bits)

        if product == 'controller':
            assert platform in ['linux', 'windows', 'mac'], 'Platform must be "linux", "windows", or "mac".'
            if platform == 'mac':
                assert bits != 32, 'A 32bit installer is not available on the Mac platform.'
            else:
                assert bits in [32, 64], 'You must select 32bit or 64bit.'
        elif product == 'euem-processor':
            assert platform in ['linux', 'windows'], 'Platform must be "linux" or "windows".'
            assert bits == 64, 'The EUEM processor is only supported as a 64bit installer.'
        elif product == 'dotnet-agent':
            assert platform == 'windows', 'The dotNet agent is only supported on Windows platforms.'
            assert bits in [32, 64], 'You must select 32bit or 64bit.'
        elif product == 'ad4db':
            assert platform in ['linux', 'windows'], 'Platform must be "linux" or "windows".'
            assert bits == 64, 'AppD4DB is only supported as a 64bit installer.'
        elif product == 'php-agent':
            assert platform == 'linux', 'The PHP agent is only supported on Linux.'
            assert bits in [32, 64], 'You must select 32bit or 64bit.'
            assert package in ['rpm', 'tar'], 'You must select RPM or tar.bz2 packaging.'
        else:
            assert product in ['java-agent', 'ibm-agent', 'machine-agent', 'ios-agent',
                               'android-agent', 'geo-server', 'events-service',
                               'analytics-processor', 'analytics-agent', 'dbagent'], \
                'Product name is not valid.'

    def _product2filename(self, product, platform='linux', bits=64, package='rpm'):
        if isinstance(bits, str):
            bits = int(bits)

        if product == 'controller':
            suffix = Zone.PLATFORM_EXT_MAP[platform]
            return 'controller_{0}bit_{1}-{2}.{3}'.format(bits, platform, self.version, suffix)
        elif product == 'euem-processor':
            suffix = Zone.PLATFORM_EXT_MAP[platform]
            return 'euem-{0}bit-{1}-{2}.{3}'.format(bits, platform, self.version, suffix)
        elif product == 'dotnet-agent':
            return 'dotNetAgentSetup{0}-{1}.msi'.format(('64' if bits == 64 else ''), self.version)
        elif product == 'ad4db':
            return 'AppD-Database-{0}'.format('Linux64.tar.gz' if platform == 'linux' else 'Setup.zip')
        elif product == 'php-agent':
            if package == 'rpm':
                arch = 'x86_64' if (bits == 64) else 'i686'
                return 'appdynamics-php-agent-{0}-1.{1}.rpm'.format(self.version, arch)
            else:
                arch = 'x64' if (bits == 64) else 'x86'
                return 'appdynamics-php-agent-{0}-linux-{1}.tar.bz2'.format(arch, self.version)
        else:
            def zipname(name):
                return '{0}-{1}.zip'.format(Zone.PRODUCT_MAP[name], self.version)

            return zipname(product)

    def get_filename(self, product, platform='linux', bits=64, package='rpm'):
        Zone._validate_product(product, platform, bits, package)
        return self._product2filename(product, platform, bits, package)

    def get_url(self, product, platform='linux', bits=64, package='rpm'):
        fname = self.get_filename(product, platform, bits, package)
        return self._get_file_url(fname)

    def download_product(self, product, platform='linux', bits=64, package='rpm', output='.'):
        filename = self.get_filename(product, platform, bits, package)
        return self.download_file(filename, output)
