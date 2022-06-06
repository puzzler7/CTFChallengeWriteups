# Unintended solve for Cookie Clicker

The first released build of Cookie Clicker didn't work on my machine - apparently, it was compiled for a newer libc version. The challenge dev did release a recompiled version, but it was long after I had solved, so I don't know what the challenge was actually about (presumably, something about clicking cookies).

However, the challenge is still solvable. We're given a zip file full of Linux libraries, along with several folders that appear to be Python packages, and an ELF file called `cookieclicker`.

```sh
$ la
assets                                         libgraphite2.so.3                    libwebp.so.7
base_library.zip                               libharfbuzz.so.0                     libX11.so.6
_cffi_backend.cpython-310-x86_64-linux-gnu.so  libicudata.so.71                     libXau.so.6
cookieclicker                                  libicuuc.so.71                       libXdmcp.so.6
importlib_metadata-4.8.1-py3.10.egg-info       libimagequant.so.0                   libXext.so.6
ld-linux-x86-64.so.2                           libjpeg.so.8                         libXft.so.2
libbrotlicommon.so.1                           liblzma.so.5                         libxml2.so.2
libbrotlidec.so.1                              libncursesw.so.6                     libXrender.so.1
libbz2.so.1.0                                  libopenblas64_p-r0-2f7c42d4.3.18.so  libxslt.so.1
libcrypto.so.1.1                               libopenjp2.so.7                      libXss.so.1
lib-dynload                                    libpcre.so.1                         libz.so.1
libexpat.so.1                                  libpng16.so.16                       libzstd.so.1
libexslt.so.0                                  libpython3.10.so.1.0                 lxml
libffi.so.8                                    libquadmath-96973f99.so.0.0.0        markupsafe
libfontconfig.so.1                             libraqm.so.0                         numpy
libfreetype.so.6                               libreadline.so.8                     PIL
libfribidi.so.0                                libssl.so.1.1                        psutil
libgcc_s.so.1                                  libstdc++.so.6                       setuptools-60.6.0-py3.10.egg-info
libgcrypt.so.20                                libtcl8.6.so                         tcl
libgfortran-040039e1.so.5.0.0                  libtiff.so.5                         tcl8
libglib-2.0.so.0                               libtk8.6.so                          tk
libgomp.so.1                                   libwebpdemux.so.2
libgpg-error.so.0                              libwebpmux.so.3

$ file cookieclicker
cookieclicker: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9aa10fdfbf5d72b09b2d97792cbec044e608aabd, for GNU/Linux 2.6.32, stripped
```

A bit of research finds that this is a PyInstaller application, and we can view some of its insides with `pyi-archive_viewer cookieclicker`.

```sh
$ pyi-archive_viewer cookieclicker
 pos, length, uncompressed, iscompressed, type, name
[(0, 219, 287, 1, 'm', 'struct'),
 (219, 1022, 1754, 1, 'm', 'pyimod01_os_path'),
 (1241, 4093, 8853, 1, 'm', 'pyimod02_archive'),
 (5334, 7441, 17553, 1, 'm', 'pyimod03_importers'),
 (12775, 1496, 3105, 1, 'm', 'pyimod04_ctypes'),
 (14271, 833, 1372, 1, 's', 'pyiboot01_bootstrap'),
 (15104, 528, 835, 1, 's', 'pyi_rth_subprocess'),
 (15632, 450, 678, 1, 's', 'pyi_rth_inspect'),
 (16082, 698, 1071, 1, 's', 'pyi_rth_pkgutil'),
 (16780, 1170, 2136, 1, 's', 'pyi_rth_multiprocessing'),
 (17950, 2004, 4195, 1, 's', 'pyi_rth_pkgres'),
 (19954, 368, 505, 1, 's', 'pyi_rth__tkinter'),
 (20322, 5553, 11622, 1, 's', 'cookieclicker'),
 (25875, 5428455, 5428455, 0, 'z', 'PYZ-00.pyz')]
? x cookieclicker
to filename? extract_cookie
```

From here, running `strings` on `extract_cookie` yields the base64 string `bjAwYnp7WXVtbXlDMDBraWV6fQ==`, which translates to the flag `n00bz{YummyC00kiez}`.