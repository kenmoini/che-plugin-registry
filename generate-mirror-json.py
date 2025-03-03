import yaml, requests, argparse, json, time

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', action='store', dest='output', help='Output file')
args = parser.parse_args()

extensions = []

with open('mirror.yml') as f:
    result =  yaml.safe_load(f)

    for extension in result.get('openvsx'):
        extensionPath = extension.get('name')
        extensionNamespace = extensionPath.split('.')[0]
        extensionName = extensionPath.split('.')[1]
        version = extension.get('version')
        
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
            # Get all versions
            elif version == "all":
                for kVersion, vVersion in metadata.get('allVersions').items():
                    if kVersion != 'latest' and kVersion != 'pre-release':
                        versionData = { 'id': extensionPath, 'version': kVersion }
                        extensions.append(versionData)
            # Defaults to latest version
            else:
                versionData = { 'id': extensionPath, 'version': metadata.get('version') }
                extensions.append(versionData)
            

# Write the output to a file
if args.output:
    with open(args.output, 'w') as f:
        json.dump(extensions, f, indent=2)
else:
    print("- Outputting to console")
    print(json.dump(extensions, indent=2))
