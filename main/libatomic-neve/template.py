pkgname = "libatomic-neve"
pkgver = "0.90.0"
pkgrel = 0
build_style = "makefile"
pkgdesc = "ABI-compatible GNU libatomic alternative"
license = "Apache-2.0"
url = "https://github.com/neve-linux/libatomic-neve"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "0c445d7c6445bb1035bcf6919abd2160a173fa240690dfa7e73463332c2ac5db"
options = ["bootstrap", "!lto"]

if self.profile().arch == "aarch64":
    # avoid emitting dependencies on builtins
    tool_flags = {"CFLAGS": ["-mno-outline-atomics"]}


@subpackage("libatomic-neve-devel")
def _(self):
    return self.default_devel()
