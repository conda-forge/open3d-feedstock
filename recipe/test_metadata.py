import platform
import re
import sys
from collections import Counter
from importlib.metadata import PackageNotFoundError, distribution, distributions, version
from pathlib import Path

import open3d

expected_version = sys.argv[1]
is_linux_x86 = sys.platform.startswith("linux") and platform.machine() in {
    "i386",
    "x86_64",
    "AMD64",
}

installed_version = version("open3d")

if is_linux_x86:
    assert installed_version == expected_version
    assert version("open3d-cpu").partition("+")[0] == expected_version
else:
    assert installed_version.partition("+")[0] == expected_version
    try:
        version("open3d-cpu")
    except PackageNotFoundError:
        pass
    else:
        raise AssertionError("open3d-cpu metadata must only be installed on Linux x86")

names = Counter()
for dist in distributions():
    name = dist.metadata["Name"]
    if name:
        normalized_name = re.sub(r"[-_.]+", "-", name).lower()
        if normalized_name in {"open3d", "open3d-cpu"}:
            names[normalized_name] += 1
expected_names = (
    Counter({"open3d": 1, "open3d-cpu": 1})
    if is_linux_x86
    else Counter({"open3d": 1})
)
assert names == expected_names

package_dirs = {
    Path(dist.locate_file("open3d")).resolve()
    for dist_name in expected_names
    for dist in [distribution(dist_name)]
}
assert package_dirs == {Path(open3d.__file__).resolve().parent}

if is_linux_x86:
    alias = distribution("open3d")
    alias_dir = Path(alias.locate_file(f"open3d-{expected_version}.dist-info"))
    assert alias.read_text("INSTALLER") == "cmake\n"
    assert {path.name for path in alias_dir.iterdir()} == {"INSTALLER", "METADATA"}
