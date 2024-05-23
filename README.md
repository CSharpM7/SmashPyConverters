# Smash Py Converters
Drag n Drop / GUI tools for quickly converting a handful of files. You will need to download the respective programs from their sources in order to use these. Then place each python script in that same folder.

## Requirements
- Python 3.9+
- ArcExplorer

## Python Dependencies (use pip install)
- tkinterdnd2

## GUIs
Requires you to extract the source file and have it in ArcExplorer
- nusPatch: Converts nus3audio to a patch file. Needs [nus3audio_patcher.exe](https://github.com/Raytwo/ARCropolis/wiki/NUS3Audio-Patching-(Features))
- parcel: Converts prc and other param files to their patch variants and vice versa. Needs [paracobNet](https://github.com/benhall-7/paracobNET/releases/latest) and a `paramlabels.csv` file
- yamlistPatch: Converts motion_list files to a patch file. Needs [yamlist](https://github.com/ultimate-research/motion_lib/releases/latest)

## Drag n Drops:
- yamlist: Converts motion_list.bin to motion_list.yaml and vice versa. Needs [yamlist](https://github.com/ultimate-research/motion_lib/releases/latest)
- paramxml: Runs paramxml.exe via drag and drop for you
