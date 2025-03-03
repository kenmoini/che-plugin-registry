import yaml, requests

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
                        versionData = { 'id': extensionPath, 'version': vVersion }
                        extensions.append(versionData)
            # Defaults to latest version
            else:
                versionData = { 'id': extensionPath, 'version': metadata.get('version') }
                extensions.append(versionData)
            

print(extensions)
