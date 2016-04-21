#
# Conditional build:
%bcond_with	doc	# build doc (not in source tarball)
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	pyxs
Summary:	pyxs - XenStore access the Python way
Summary(pl.UTF-8):	pyxs - pythonowy dostęp do XenStore
Name:		python-%{module}
Version:	0.4.0
Release:	1
License:	LGPL v3
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/pyxs/%{module}-%{version}.tar.gz
# Source0-md5:	cbf42444287ea82e4d0877c3be55ea06
URL:		https://github.com/selectel/pyxs
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 3.4
BuildRequires:	python3-setuptools
%endif
%if %{with docs}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyxs a pure Python XenStore client implementation, which covers all of
the libxs features and adds some nice Pythonic sugar on top. Here's a
shortlist:

- pyxs supports both Python 2 and 3,
- works over a Unix socket or XenBus,
- has a clean and well-documented API,
- is writen in easy to understand Python,
- can be used with gevent or eventlet.

%package -n python3-%{module}
Summary:	pyxs - XenStore access the Python way
Summary(pl.UTF-8):	pyxs - pythonowy dostęp do XenStore
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
pyxs a pure Python XenStore client implementation, which covers all of
the libxs features and adds some nice Pythonic sugar on top. Here's a
shortlist:

- pyxs supports both Python 2 and 3,
- works over a Unix socket or XenBus,
- has a clean and well-documented API,
- is writen in easy to understand Python,
- can be used with gevent or eventlet.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
