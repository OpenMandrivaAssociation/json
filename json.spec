Name:		json
Version:	20260814
Release:	1
Summary:	JSON encoders and decoders in Java
Group:		Development/Java
License:	Public Domain
URL:		https://github.com/stleary/JSON-java
Source0:	https://github.com/stleary/JSON-java/archive/refs/tags/%{version}.tar.gz#/JSON-java-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

Obsoletes:	%{name}-javadoc < %{version}

%description
Reference implementation of JSON for Java. 20260814 is the current
release. The Java module is org.json. Tests are skipped.

%prep
%autosetup -n JSON-java-%{version}
# Upstream packaging is bundle. The bundle, moditect and publishing
# plugins are not installed. The test dependencies are not needed.
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def local(tag):
    return tag.rsplit("}", 1)[-1]

def artifact_of(elem):
    for item in elem:
        if local(item.tag) == "artifactId":
            return (item.text or "").strip()
    return ""

def child_text(elem, name):
    for item in elem:
        if local(item.tag) == name:
            return (item.text or "").strip()
    return ""

drop_plugins = {
    "maven-bundle-plugin",
    "maven-source-plugin",
    "maven-javadoc-plugin",
    "maven-gpg-plugin",
    "moditect-maven-plugin",
    "central-publishing-maven-plugin",
    "replacer",
}
tree = ET.parse("pom.xml")
root = tree.getroot()
packaging = None
for child in list(root):
    if local(child.tag) == "packaging":
        packaging = child
if packaging is None or (packaging.text or "").strip() != "bundle":
    raise SystemExit("packaging was not bundle")
packaging.text = "jar"
removed = []
for parent in list(root.iter()):
    for child in list(parent):
        kind = local(child.tag)
        if kind == "plugin" and artifact_of(child) in drop_plugins:
            parent.remove(child)
            removed.append(artifact_of(child))
        elif kind == "dependency" and child_text(child, "scope") == "test":
            parent.remove(child)
            removed.append(artifact_of(child))
missing = drop_plugins - set(removed)
if missing:
    raise SystemExit("not removed " + " ".join(sorted(missing)))
tree.write("pom.xml", encoding="UTF-8", xml_declaration=True)
text = Path("pom.xml").read_text(encoding="utf-8")
if "<packaging>jar</packaging>" not in text:
    raise SystemExit("packaging jar missing")
for art in sorted(drop_plugins):
    if "<artifactId>" + art + "</artifactId>" in text:
        raise SystemExit("survived " + art)
if "<scope>test</scope>" in text:
    raise SystemExit("test dependency survived")
if "<source>1.8</source>" not in text or "<target>1.8</target>" not in text:
    raise SystemExit("compiler level missing")
PY

%build -a
cat > target/module-info.java << 'EOF'
module org.json {
    exports org.json;
}
EOF
javac --release 9 \
	--patch-module org.json=target/classes \
	-d target/classes \
	target/module-info.java
test -s target/classes/module-info.class
jar uf target/json-%{version}.jar -C target/classes module-info.class
java --module-path target/json-%{version}.jar --describe-module org.json | grep -q '^org.json'

%files -f .mfiles
%doc LICENSE README.md
