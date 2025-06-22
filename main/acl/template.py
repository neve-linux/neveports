pkgname = "acl"
pkgver = "2.3.2"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--libdir=/usr/lib", "--libexecdir=/usr/lib"]
# cycle neveutils -> acl -> automake -> neveutils
configure_gen = []
hostmakedepends = ["pkgconf"]
makedepends = ["attr-devel"]
checkdepends = ["perl"]
pkgdesc = "Access Control List filesystem support"
license = "LGPL-2.1-or-later"
url = "https://savannah.nongnu.org/projects/acl"
source = f"$(NONGNU_SITE)/acl/acl-{pkgver}.tar.gz"
sha256 = "5f2bdbad629707aa7d85c623f994aa8a1d2dec55a73de5205bac0bf6058a2f7c"
# test suite makes assumptions about a GNU environment
options = ["bootstrap", "!check"]


@subpackage("acl-devel")
def _(self):
    self.depends += ["attr-devel"]

    return self.default_devel(man="5")


@subpackage("acl-progs")
def _(self):
    return self.default_progs(extra=["usr/share"])
