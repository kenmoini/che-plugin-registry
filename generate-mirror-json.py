import yaml, requests, argparse, json, time

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', action='store', dest='output', help='Output file')
args = parser.parse_args()

extensions = []

def find(list_of_tuples, value):
    try:
        return next(x for x in list_of_tuples if value in x)
    except StopIteration:
        return None

with open('mirror.yml') as f:
    result =  yaml.safe_load(f)

    for extension in result.get('openvsx'):
        extensionPath = extension.get('name')
        extensionNamespace = extensionPath.split('.')[0]
        extensionName = extensionPath.split('.')[1]
        version = extension.get('version')
        excludeVersions = extension.get('excludeVersions')
        
        # Get the extension metadata from the OpenVSX API
        # https://open-vsx.org/api
        print("Waiting for 2 seconds between requests...")
        time.sleep(2)
        print("- Getting metadata for " + extensionPath)
        extensionURL = 'https://open-vsx.org/api/' + extensionNamespace + '/' + extensionName
        metadata = requests.get(extensionURL).json()
        # Skip pre-release versions
        if metadata.get('preRelease') == None or metadata.get('preRelease') == False:
            # Just get the latest version
            if version == "latest":
                versionData = { 'id': extensionPath, 'version': metadata.get('version') }
                extensions.append(versionData)
            # Get last 10 versions
            elif version == "last-10":
                lastTen = []
                for kVersion, vVersion in metadata.get('allVersions').items():
                    if (kVersion != 'latest') and (kVersion != 'pre-release'):
                        if excludeVersions:
                            if kVersion in excludeVersions:
                                continue
                        if len(lastTen) < 10:
                            lastTen.append(kVersion)
                            versionData = { 'id': extensionPath, 'version': kVersion }
                            extensions.append(versionData)
            # Get all versions
            elif version == "all":
                for kVersion, vVersion in metadata.get('allVersions').items():
                    if kVersion != 'latest' and kVersion != 'pre-release':
                        versionData = { 'id': extensionPath, 'version': kVersion }
                        extensions.append(versionData)
            # Defaults to the specified version if it's found
            else:
                if find(metadata.get('allVersions'), version):
                    versionData = { 'id': extensionPath, 'version': version }
                else:
                    versionData = { 'id': extensionPath, 'version': metadata.get('version') }
                extensions.append(versionData)
            

# Write the output to a file
if args.output:
    with open(args.output, 'w') as f:
        json.dump(extensions, f, indent=2)
else:
    print("- Outputting to console")
    print(json.dumps(extensions, indent=2))
