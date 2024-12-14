%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$
%global debug_package %{nil}

Name:           ros-jazzy-ament-cmake-pyflakes
Version:        0.17.1
Release:        0%{?dist}%{?release_suffix}
Summary:        ROS ament_cmake_pyflakes package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jazzy-ament-cmake-test
Requires:       ros-jazzy-ament-pyflakes
BuildRequires:  ros-jazzy-ament-cmake-core
BuildRequires:  ros-jazzy-ament-cmake-test

%if 0%{?with_tests}
BuildRequires:  ros-jazzy-ament-cmake-copyright
BuildRequires:  ros-jazzy-ament-cmake-lint-cmake
%endif

%description
The CMake API for ament_pyflakes to check code using pyflakes.

%prep
%autosetup -p1

%build
# 修复 PYTHONPATH 环境变量
export PYTHONPATH=/opt/ros/jazzy/lib/python3.11/site-packages:$PYTHONPATH

# 修复 CMAKE_PREFIX_PATH 和 PKG_CONFIG_PATH
export CMAKE_PREFIX_PATH=/opt/ros/jazzy
export PKG_CONFIG_PATH=/opt/ros/jazzy/lib/pkgconfig

# 输出环境变量以验证设置
echo "PYTHONPATH: $PYTHONPATH"
echo "CMAKE_PREFIX_PATH: $CMAKE_PREFIX_PATH"
echo "PKG_CONFIG_PATH: $PKG_CONFIG_PATH"

# 验证 ament_package 是否可用
python3 -c "import ament_package" || { echo "ament_package not found"; exit 1; }

# 创建构建目录并进入
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# 检查是否存在测试目录或文件
if [ -d "tests" ] || ls test_*.py *_test.py > /dev/null 2>&1; then
    %__python3 -m pytest tests || echo "RPM TESTS FAILED"
else
    echo "No tests to run, skipping."
fi
%endif

%files
/opt/ros/jazzy/*

%changelog
* Sun Dec 15 2024 Chris Lalancette <clalancette@gmail.com> - 0.17.1-0
- Autogenerated by Bloom

