# Che Plugin Registry - Helper

When deploying Che/Red Hat OpenShift DevSpaces in a disconnected environment, you need to mirror some VSCode Extensions.  You can do this pretty easily with the [OpenVSX](https://github.com/EclipseFdn/open-vsx.org) bits.  You can't really pull things from the Microsoft VSCode Extension Marketplace due to licensing terms, but most of the ones you need you'll find on OpenVSX and can easily mirror those.

This repo has a YAML file, `mirror.yml` - this file houses the definition of what extensions you want to mirror.  You can do the latest version, last N versions, all available versions, or a specific version.

That file is used by the `generate-mirror-json.py` script - this will use the OpenVSX API to gather the metadata of the extensions listed in the `mirror.yml` file and generates the mirror JSON needed to build a Plugin Registry Mirror image.

The `generate.sh` script will run that Python script as well as perform all the other steps needed to build/push the Plugin Registry image.

1. Modify `mirror.yml` to suit your needs - use https://open-vsx.org/ as a source
2. Optionally run `python3 generate-mirror-json.py [-o my-file.json]` to test
3. Modify `generate.sh` to suit your needs
4. Run `./generate.sh` to do the full generate of an image and to push it to your remote registry.