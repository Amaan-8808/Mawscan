

import mimetypes


def mime_backend(filename):
    diff = filename.split(".")
    extension_to_mime = {
    '.323': 'text/h323',
    '.3g2': 'video/3gpp2',
    '.3gp': 'video/3gpp',
    '.7z': 'application/x-7z-compressed',
    '.abw': 'application/x-abiword',
    '.ai': 'application/postscript',
    '.aac': 'audio/aac',
    '.arc': 'application/x-freearc',
    '.avi': 'video/x-msvideo',
    '.azw': 'application/vnd.amazon.ebook',
    '.bin': 'application/octet-stream',
    '.bmp': 'image/bmp',
    '.bz': 'application/x-bzip',
    '.bz2': 'application/x-bzip2',
    '.csh': 'application/x-csh',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.eot': 'application/vnd.ms-fontobject',
    '.epub': 'application/epub+zip',
    '.gif': 'image/gif',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.ico': 'image/vnd.microsoft.icon',
    '.ics': 'text/calendar',
    '.jar': 'application/java-archive',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.jsonld': 'application/ld+json',
    '.mid': 'audio/midi',
    '.midi': 'audio/midi',
    '.mjs': 'text/javascript',
    '.mp3': 'audio/mpeg',
    '.mpeg': 'video/mpeg',
    '.mpkg': 'application/vnd.apple.installer+xml',
    '.odp': 'application/vnd.oasis.opendocument.presentation',
    '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
    '.odt': 'application/vnd.oasis.opendocument.text',
    '.oga': 'audio/ogg',
    '.ogv': 'video/ogg',
    '.ogx': 'application/ogg',
    '.opus': 'audio/opus',
    '.otf': 'font/otf',
    '.png': 'image/png',
    '.pdf': 'application/pdf',
    '.php': 'application/x-httpd-php',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.rar': 'application/vnd.rar',
    '.rtf': 'application/rtf',
    '.sh': 'application/x-sh',
    '.svg': 'image/svg+xml',
    '.swf': 'application/x-shockwave-flash',
    '.tar': 'application/x-tar',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.ts': 'video/mp2t',
    '.ttf': 'font/ttf',
    '.txt': 'text/plain',
    '.vsd': 'application/vnd.visio',
    '.wav': 'audio/wav',
    '.weba': 'audio/webm',
    '.webm': 'video/webm',
    '.webp': 'image/webp',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.xhtml': 'application/xhtml+xml',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xml': 'application/xml',
    '.xul': 'application/vnd.mozilla.xul+xml',
    '.zip': 'application/zip',
    '.3gp': 'video/3gpp',
    '.3g2': 'video/3gpp2',
    '.7z': 'application/x-7z-compressed',
    '.ace': 'application/x-ace-compressed',
    '.aac': 'audio/aac',
    '.ai': 'application/illustrator',
    '.aif': 'audio/aiff',
    '.aiff': 'audio/aiff',
    '.amr': 'audio/amr',
    '.apk': 'application/vnd.android.package-archive',
    '.appimage': 'application/vnd.appimage',
    '.arj': 'application/x-arj',
    '.asf': 'video/x-ms-asf',
    '.asx': 'audio/x-ms-asx',
    '.avi': 'video/x-msvideo',
    '.bat': 'application/x-msdownload',
    '.bin': 'application/octet-stream',
    '.bmp': 'image/bmp',
    '.bz': 'application/x-bzip',
    '.bz2': 'application/x-bzip2',
    '.cab': 'application/vnd.ms-cab-compressed',
    '.caf': 'audio/x-caf',
    '.cgm': 'image/cgm',
    '.class': 'application/x-java-applet',
    '.cmx': 'image/x-cmx',
    '.cpio': 'application/x-cpio',
    '.cpt': 'application/mac-compactpro',
    '.cr2': 'image/x-canon-cr2',
    '.csh': 'application/x-csh',
    '.css': 'text/css',
    '.cue': 'application/x-cue',
    '.cur': 'image/x-win-bitmap',
    '.deb': 'application/x-deb',
    '.dcm': 'application/dicom',
    '.dcr': 'application/x-director',
    '.dds': 'image/vnd.ms-dds',
    '.der': 'application/x-x509-ca-cert',
    '.dng': 'image/x-adobe-dng',
    '.doc': 'application/msword',
    '.dot': 'application/msword',
    '.dtd': 'application/xml-dtd',
    '.dwg': 'image/vnd.dwg',
    '.dxf': 'image/vnd.dxf',
    '.egg': 'application/octet-stream',
    '.eot': 'application/vnd.ms-fontobject',
    '.eps': 'application/postscript',
    '.epub': 'application/epub+zip',
    '.exe': 'application/x-msdownload',
    '.f4v': 'video/x-f4v',
    '.fbs': 'image/vnd.fastbidsheet',
    '.fh': 'image/x-freehand',
    '.flac': 'audio/flac',
    '.flv': 'video/x-flv',
    '.fpx': 'image/vnd.fpx',
    '.fst': 'image/vnd.fst',
    '.fvt': 'image/vnd.fvt',
    '.g3': 'image/g3fax',
    '.gif': 'image/gif',
    '.glb': 'model/gltf-binary',
    '.gltf': 'model/gltf+json',
    '.gz': 'application/gzip',
    '.gzip': 'application/gzip',
    '.h261': 'video/h261',
    '.h263': 'video/h263',
    '.h264': 'video/h264',
    '.hdr': 'image/vnd.radiance',
    '.htm': 'text/html',
    '.html': 'text/html',
    '.ico': 'image/vnd.microsoft.icon',
    '.ics': 'text/calendar',
    '.iff': 'image/iff',
    '.img': 'application/octet-stream',
    '.iso': 'application/x-iso9660-image',
    '.java': 'text/x-java-source',
    '.jpe': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.jp2': 'image/jp2',
    '.json': 'application/json',
    '.jp2': 'image/jp2',
    '.jpm': 'image/jpm',
    '.jpx': 'image/jpx',
    '.kar': 'audio/midi',
    '.key': 'application/vnd.apple.keynote',
    '.ktx': 'image/ktx',
    '.less': 'text/css',
    '.lha': 'application/x-lzh-compressed',
    '.lharc': 'application/x-lzh-compressed',
    '.lnk': 'application/x-ms-shortcut',
    '.lz': 'application/x-lzip',
    '.lzh': 'application/x-lzh-compressed',
    '.lzma': 'application/x-lzma',
    '.lzo': 'application/x-lzop',
    '.m21': 'application/mp21',
    '.m4a': 'audio/m4a',
    '.m4b': 'audio/m4b',
    '.m4p': 'audio/m4p',
    '.m4u': 'video/vnd.mpegurl',
    '.m4v': 'video/x-m4v',
    '.mar': 'application/octet-stream',
    '.mdb': 'application/x-msaccess',
    '.mdi': 'image/vnd.ms-modi',
    '.mht': 'multipart/mixed',
    '.mhtml': 'multipart/mixed',
    '.mobi': 'application/x-mobipocket-ebook',
    '.mov': 'video/quicktime',
    '.mp2': 'audio/mpeg',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.mpkg': 'application/vnd.apple.installer+xml',
    '.msi': 'application/x-msdownload',
    '.msm': 'application/octet-stream',
    '.msp': 'application/octet-stream',
    '.mxf': 'application/mxf',
    '.npx': 'image/vnd.net-fpx',
    '.numbers': 'application/vnd.apple.numbers',
    '.o': 'application/octet-stream',
    '.oga': 'audio/ogg',
    '.ogv': 'video/ogg',
    '.ogx': 'application/ogg',
    '.opus': 'audio/opus',
    '.otf': 'font/otf',
    '.pages': 'application/vnd.apple.pages',
    '.pbm': 'image/x-portable-bitmap',
    '.pct': 'image/pict',
    '.pdb': 'application/vnd.palm',
    '.pdf': 'application/pdf',
    '.pgm': 'image/x-portable-graymap',
    '.pgp': 'application/pgp-encrypted',
    '.pkg': 'application/octet-stream',
    '.pl': 'application/x-perl',
    '.pm': 'application/x-perl',
    '.png': 'image/png',
    '.pnm': 'image/x-portable-anymap',
    '.pot': 'application/vnd.ms-powerpoint',
    '.ppa': 'application/vnd.ms-powerpoint',
    '.ppm': 'image/x-portable-pixmap',
    '.pps': 'application/vnd.ms-powerpoint',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.ps': 'application/postscript',
    '.psd': 'image/vnd.adobe.photoshop',
    '.py': 'application/x-python',
    '.qt': 'video/quicktime',
    '.ra': 'audio/x-realaudio',
    '.ram': 'audio/x-pn-realaudio',
    '.rar': 'application/vnd.rar',
    '.rm': 'audio/x-pn-realaudio',
    '.rpm': 'application/x-redhat-package-manager',
    '.rss': 'application/rss+xml',
    '.rtf': 'application/rtf',
    '.rpm': 'application/x-redhat-package-manager',
    '.rv': 'video/vnd.rn-realvideo',
    '.s3m': 'audio/s3m',
    '.sh': 'application/x-sh',
    '.sha256': 'application/octet-stream',
    '.shar': 'application/x-shar',
    '.shtm': 'text/html',
    '.shtml': 'text/html',
    '.sit': 'application/x-stuffit',
    '.sitx': 'application/x-stuffitx',
    '.sketch': 'application/octet-stream',
    '.snd': 'audio/basic',
    '.so': 'application/octet-stream',
    '.stl': 'model/stl',
    '.svg': 'image/svg+xml',
    '.swf': 'application/x-shockwave-flash',
    '.tar': 'application/x-tar',
    '.tbz': 'application/x-bzip-compressed-tar',
    '.tbz2': 'application/x-bzip-compressed-tar',
    '.tga': 'image/tga',
    '.tgz': 'application/gzip-compressed',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.tk': 'application/x-tcl',
    '.torrent': 'application/x-bittorrent',
    '.ttf': 'font/ttf',
    '.txt': 'text/plain',
    '.udeb': 'application/x-debian-package',
    '.umx': 'audio/x-mod',
    '.vcard': 'text/vcard',
    '.vcf': 'text/vcard',
    '.vmdk': 'application/x-virtualbox-vmdk',
    '.vob': 'video/dvd',
    '.vtt': 'text/vtt',
    '.wav': 'audio/x-wav',
    '.weba': 'audio/webm',
    '.webm': 'video/webm',
    '.webp': 'image/webp',
    '.wma': 'audio/x-ms-wma',
    '.wmv': 'video/x-ms-wmv',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.wpd': 'application/vnd.wordperfect',
    '.wpl': 'application/vnd.ms-wpl',
    '.wps': 'application/vnd.ms-works',
    '.xar': 'application/vnd.xara',
    '.xbm': 'image/x-xbitmap',
    '.xcf': 'image/x-xcf',
    '.xht': 'application/xhtml+xml',
    '.xhtml': 'application/xhtml+xml',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xml': 'application/xml',
    '.xpm': 'image/x-xpixmap',
    '.xsl': 'application/xml',
    '.xwd': 'image/x-xwindowdump',
    '.xz': 'application/x-xz',
    '.yaml': 'text/yaml',
    '.yml': 'text/yaml',
    '.zip': 'application/zip',
    '.z': 'application/x-compress',
    '.Z': 'application/x-compress',
    '.zoo': 'application/x-zoo',
    '.zst': 'application/zstd'
    }
    
    ext_diff = "."+str(diff[-1])
    if ext_diff in list(extension_to_mime.keys()):
        mime = extension_to_mime[ext_diff]
    else:
        try:
            kind = mimetypes.guess(filename)[0]
            return kind
        except:
            pass
    return mime
