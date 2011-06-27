Summary:	FFmpegSource - FFmpeg wrapper library
Summary(pl.UTF-8):	FFmpegSource - biblioteka obudowująca FFmpeg
Name:		ffmpegsource
Version:	2.15
Release:	2
License:	MIT (ffmpegsource itself), GPL v3+ (forced by ffmpeg)
Group:		Libraries
#Source0Download: http://code.google.com/p/ffmpegsource/downloads/list
Source0:	http://ffmpegsource.googlecode.com/files/%{name}-%{version}_src.7z
# Source0-md5:	0d0e2d4f6c4424e5f182f40f451c064e
Patch0:		%{name}-c++.patch
Patch1:		%{name}-ffmpeg-0.8.patch
URL:		http://code.google.com/p/ffmpegsource/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake
BuildRequires:	ffmpeg-devel >= 0.8.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	p7zip
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
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
(zwykle) z dokładnością do ramek i próbek, bez potrzeby zajmowania
się często złożonym, nie najlepiej udokumentowanym API FFmpeg.

%package devel
Summary:	Header files for FFmpegSource library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FFmpegSource
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ffmpeg-devel >= 0.8.0
Requires:	libstdc++-devel
Requires:	zlib-devel

%description devel
Header files for FFmpegSource library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FFmpegSource.

%package static
Summary:	Static FFmpegSource library
Summary(pl.UTF-8):	Statyczna biblioteka FFmpegSource
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FFmpegSource library.

%description static -l pl.UTF-8
Statyczna biblioteka FFmpegSource.

%prep
%setup -q -c -T -n %{name}-%{version}_src
7z -o.. x %{SOURCE0}
%undos src/core/{indexing,lavfindexer,utils}.cpp
%patch0 -p1
%patch1 -p1
%{__rm} configure

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/ffmsindex
%attr(755,root,root) %{_libdir}/libffms2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffms2.so.2

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,css}
%attr(755,root,root) %{_libdir}/libffms2.so
%{_libdir}/libffms2.la
%{_includedir}/ffms.h
%{_includedir}/ffmscompat.h
%{_pkgconfigdir}/ffms2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libffms2.a
