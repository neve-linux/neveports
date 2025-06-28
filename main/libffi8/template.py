pkgname = "libffi8"
pkgver = "3.4.8"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--includedir=/usr/include",
    "--disable-multi-os-directory",
    "--with-pic",
    # https://github.com/libffi/libffi/pull/647
    # some stuff (notably gobject-introspection) uses
    # libffi incorrectly, prevent them from being broken for now
    "--disable-exec-static-tramp",
]
# regen causes lost symvers which is a build abi break
#
# correct:
#
# $ nm -D /usr/lib/libffi.so.8.1.4|grep ffi_type_double
# 0000000000001558 R ffi_type_double@@LIBFFI_BASE_8.0
#
# bad:
#
# 0000000000001568 R ffi_type_double
#
configure_gen = []
hostmakedepends = ["pkgconf"]
# actually only on x86 and arm (tramp.c code) but it does not hurt
makedepends = ["linux-headers"]
pkgdesc = "Library supporting Foreign Function Interfaces"
license = "MIT"
url = "http://sourceware.org/libffi"
source = f"https://github.com/libffi/libffi/releases/download/v{pkgver}/libffi-{pkgver}.tar.gz"
sha256 = "bc9842a18898bfacb0ed1252c4febcc7e78fa139fd27fdc7a3e30d9d9356119b"
# dejagnu
options = ["!check", "linkundefver"]


def post_install(self):
    self.install_license("LICENSE")


@subpackage("libffi8-devel")
def _(self):
    self.provides = [self.with_pkgver("libffi-devel")]

    return self.default_devel(extra=["usr/share/info"])
