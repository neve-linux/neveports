pkgname = "neveutils"
pkgver = "14.3.0"
pkgrel = 0
build_style = "meson"
configure_args = [
    "--libexecdir=/usr/lib/neveutils",
    "-Dchimera_realpath=enabled",
]
hostmakedepends = ["flex", "byacc", "meson", "pkgconf"]
makedepends = [
    "acl-devel",
    "bzip2-devel",
    "libedit-devel",
    "libxo-devel",
    "musl-bsd-headers",
    "ncurses-devel",
    "openssl3-devel",
    "xz-devel",
    "zlib-ng-compat-devel",
]
depends = ["base-files", "debianutils"]
# compat
provides = [
    self.with_pkgver("musl-fts"),
    self.with_pkgver("musl-rpmatch"),
]
pkgdesc = "Neve Linux userland"
license = "BSD-2-Clause"
url = "https://github.com/neve-linux/neveutils"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "ec6179277bc5e6d24036865e3740c09f712c6f4e0f900255ef96463c95ef450f"
hardening = ["vis", "cfi"]
# no test suite
options = ["bootstrap", "!check"]

if self.stage > 0:
    makedepends += ["linux-headers", "zstd-devel"]
    configure_args += ["-Dtiny=enabled"]
    # don't bother in stage 0
    depends += ["sd-tools"]
else:
    makedepends += ["libxo-devel-static"]
    configure_args += ["-Dzstd=disabled"]


def init_configure(self):
    if self.stage > 0:
        return

    spath = str(self.bldroot_path / "usr/lib")

    # since meson translates all `-lfoo` into absolute paths to libraries,
    # and pkg-config's libdir is set to /usr/lib in this case, fool it
    # into giving out the correct paths to make meson happy
    self.env["PKG_CONFIG_LIBCRYPTO_LIBDIR"] = spath
    self.env["PKG_CONFIG_LIBEDIT_LIBDIR"] = spath


def post_install(self):
    # license
    self.install_license("LICENSE")
    # less
    self.uninstall("usr/bin/zless")
    self.uninstall("usr/share/man/man1/zless.1")
    # base shell
    self.install_shell("/usr/bin/sh")
    # tiny tools
    tdest = "usr/lib/neveutils/tiny"
    self.install_dir(tdest)
    for f in (self.destdir / "usr/bin").glob("*.tiny"):
        self.mv(f, self.destdir / tdest / f.stem)
    # etc files, handled with tmpfiles
    self.install_dir("usr/share/neveutils")
    self.install_tmpfiles(self.files_path / "neveutils.conf")
    self.install_tmpfiles(
        self.files_path / "neveutils-extra.conf", name="neveutils-extra"
    )
    for f in (self.destdir / "etc").iterdir():
        self.mv(f, self.destdir / "usr/share/neveutils")


@subpackage("neveutils-devel-man")
def _(self):
    # former conflicts with fts/rpmatch manpages
    self.replaces = ["man-pages-devel<6.9.1-r3"]
    return ["usr/share/man/man3"]


@subpackage("neveutils-devel")
def _(self):
    # compat
    self.provides = [
        self.with_pkgver("musl-fts-devel"),
        self.with_pkgver("musl-rpmatch-devel"),
    ]
    # explicitly non-lto
    self.options = ["ltostrip", "!splitstatic"]
    return self.default_devel()


@subpackage("neveutils-extra")
def _(self):
    self.subdesc = "additional tools"
    self.depends = [self.parent]

    return [
        "cmd:calendar",
        "cmd:cal",
        "cmd:compress",
        "cmd:cu",
        "cmd:ee",
        "cmd:ex",
        "cmd:fetch",
        "cmd:gencat",
        "cmd:locate*",
        "cmd:m4",
        "cmd:nc",
        "cmd:ncal",
        "cmd:nex",
        "cmd:nvi",
        "cmd:nview",
        "cmd:patch",
        "cmd:telnet",
        "cmd:tip",
        "cmd:uncompress",
        "cmd:vi",
        "cmd:view",
        "man:remote.5",
        "man:locate.updatedb.8",
        "man:updatedb.8",
        "usr/lib/neveutils/locate.*",
        "usr/lib/tmpfiles.d/neveutils-extra.conf",
        "usr/share/neveutils/locate.rc",
        "usr/share/vi",
    ]
