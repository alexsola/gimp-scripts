# Introduction
This is a collection of scripts for GIMP that I plan to grow. These are custom scripts that I make more for practice than for real use. 

# Installation
Just copy the scripts into one of the folders configured in GIMP for `plug-ins`. Check that the scripts have the execution right on them. Example in Linux:

```
git clone https://github.com/alexsola/gimp-scripts.git
cd gimp-scripts
cp caleido.py ~/.config/GIMP/2.10/plug-ins/
chmod .config/GIMP/2.10/plug-ins/caleido.py
```

**NOTE:** At least, when I was using GIMP 2.8.10 the directory to copy the scripts was `scripts` and not `plug-ins`. So one thing to check if the scripts is not in the `Filters/Custom` menu, try copy the scripts from `plug-ins` to `scripts`.

To check where GIMP is looking for plug-ins, check `Edit -> Properties` and there, last category on the left tree: `Folders`.

# Description of the scripts
|File Name|Description|
|---------|-----------|
|caleido.py|Uses layer blending modes and layer flips and rotations to craft caleidoscope-like effect. The main difference with the Kaleidoscope effect that comes with GIMP, is that this one is based on blending modes and not reflections. In some cases, both will get same results.|
