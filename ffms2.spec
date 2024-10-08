#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	FFmpegSource - FFmpeg wrapper library
Summary(pl.UTF-8):	FFmpegSource - biblioteka obudowująca FFmpeg
Name:		ffms2
Version:	5.0
Release:	1
License:	MIT (ffmpegsource itself), GPL v3+ (forced by ffmpeg)
Group:		Libraries
#Source0Download: https://github.com/FFMS/ffms2/releases
Source0:	https://github.com/FFMS/ffms2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c90259950777de3c429a78038a6a00a3
URL:		https://github.com/FFMS/ffms2
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1:1.11
# libavformat >= 60.16.0 libavcodec >= 60.31.0 libswscale >= 7.5.0 libavutil >= 58.29.0 libswresample >= 4.12.0
BuildRequires:	ffmpeg-devel >= 6.1
%ifarch %{armv6}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Obsoletes:	ffmpegsource < 2.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FFmpegSource (usually known as FFMS or FFMS2) is a cross-platform
wrapper library around FFmpeg, plus some additional components to deal
with file formats FFmpeg's libavformat has (or used to have) problems
with. It gives you an easy, convenient way to say "open and decompress
this media file for me, I don't care how you do it" and get frame- and
sample-accurate access (usually), without having to bother with the
sometimes less than straightforward and less than perfectly documented
FFmpeg API.

%description -l pl.UTF-8
FFmpegSource (zwykle zwana FFMS lub FFMS2) to wieloplatformowa
biblioteka obudowująca FFmpeg wraz z paroma dodatkowymi komponentami
mającymi radzić sobie z formatami plików, z którymi libavformat z
FFmpeg ma (lub miał) problemy. Umożliwia w łatwy sposób zażądanie
"otwórz i zdekompresuj ten plik, nieważne jak" i uzyskanie dostępu
(zwykle) z dokładnością do ramek i próbek, bez potrzeby zajmowania się
często złożonym, nie najlepiej udokumentowanym API FFmpeg.

%package devel
Summary:	Header files for FFmpegSource library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FFmpegSource
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ffmpeg-devel >= 6.1
Requires:	libstdc++-devel
Requires:	zlib-devel
Provides:	ffmpegsource-devel = %{version}-%{release}
Obsoletes:	ffmpegsource-devel < 2.20

%description devel
Header files for FFmpegSource library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FFmpegSource.

%package static
Summary:	Static FFmpegSource library
Summary(pl.UTF-8):	Statyczna biblioteka FFmpegSource
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	ffmpegsource-static < 2.20

%description static
Static FFmpegSource library.

%description static -l pl.UTF-8
Statyczna biblioteka FFmpegSource.

%prep
%setup -q

install -d src/config

%build
CXXFLAGS="%{rpmcxxflags} -Wall -Wextra"
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%ifarch %{armv6}
	LIBS=-latomic \
%endif
	--disable-silent-rules \
	--enable-shared \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libffms2.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/ffmsindex
%attr(755,root,root) %{_libdir}/libffms2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffms2.so.5

%files devel
%defattr(644,root,root,755)
%doc doc/ffms2-*.md
%attr(755,root,root) %{_libdir}/libffms2.so
%{_includedir}/ffms.h
%{_includedir}/ffmscompat.h
%{_pkgconfigdir}/ffms2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libffms2.a
%endif
