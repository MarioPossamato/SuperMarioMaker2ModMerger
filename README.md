# SuperMarioMaker2ModMerger
A Tool For Merging Super Mario Maker 2 Mods
Version 0.2

![preview](https://github.com/MarioPossamato/SuperMarioMaker2ModMerger/blob/main/SuperMarioMaker2ModMergerData/preview.png)

A copy of Super Mario Maker 2 (01009B90006DC800) v327680 (3.0.1) is required for SMM2MM to execute properly.  Since one is not packaged with it, due to legal reasons, you will need to acquire one by using [this tool](https://github.com/DarkMatterCore/nxdumptool/releases).  The filesystem should resemble the following:
```
SuperMarioMaker2ModMerger
 └───SuperMarioMaker2
     ├───exefs
     └───romfs
         ├───Bake
         ├───Course
         ├───CourseInfo
         ├───Effect
         ├───ELink2
         ├───Env
         ├───Event
         ├───EventFlow
         ├───Font
         ├───Layout
         ├───Map
         ├───Message
         ├───Mii
         ├───Model
         ├───MyWorld
         ├───Pack
         ├───Palette
         ├───Replay
         │   └───Lesson
         ├───Rumble
         ├───SLink2
         ├───Sound
         │   ├───Effect
         │   ├───Resource
         │   │   └───Stream
         │   └───ResourceList
         └───System
             ├───Font
             └───WordList
```
Also, merging multiple SMM2 mods may take a while, so please be patient! :)

# Pre-Requisites
- [SuperMarioMaker2ModMerger](https://github.com/MarioPossamato/SuperMarioMaker2ModMerger/archive/main.zip)
- [pyyaml](https://github.com/yaml/pyyaml)
- [python-zstd](https://github.com/sergey-dryabzhinsky/python-zstd)
- [python-zstandard](https://github.com/indygreg/python-zstandard)
- [sarc](https://github.com/zeldamods/sarc/)
- [SarcLib](https://github.com/aboood40091/SarcLib)
- [libyaz0](https://github.com/aboood40091/libyaz0)
- [syaz0](https://github.com/zeldamods/syaz0)
- [byml](https://github.com/zeldamods/byml-v2)
- [oead](https://github.com/zeldamods/oead)

# Using this tool
- Run `SuperMarioMaker2ModMerger.bat`
- Click the `Add` button to add a mod to the list
- Click the `Merge` button to merge selected mods

# Reporting errors
Open a new issue [here](https://github.com/MarioPossamato/SuperMarioMaker2ModMerger/issues).  Please include the traceback, as well as links to the mods used:
```
Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    raise Exception('An error occurred!')
Exception: An error occurred!

https://gamebanana.com/gamefiles/12668
https://gamebanana.com/gamefiles/10747
```
You can also send me a message on Discord `MarioPossamato#9693` with the traceback as well as links to the mods used.

# Is SuperMarioMaker2ModMerger finished?
No.

# Where can I discuss development of SuperMarioMaker2ModMerger?
You can chat about development of SuperMarioMaker2ModMerger either in [my Discord server](https://discord.gg/8wx8uQF) or in [the Super Mario Maker 2 Deluxe Discord server](https://discord.gg/WhgdAMy).

# Who gets credit for this tool?
- [MarioPossamato](https://github.com/MarioPossamato/) for SuperMarioMaker2ModMerger
- [aboood40091](https://github.com/aboood40091/) for SarcLib and libyaz0
- [zeldamods](https://github.com/zeldamods/) for sarc, byml, syaz0, and oead
- [sergey-dryabzhinsky](https://github.com/sergey-dryabzhinsky) for python-zstd
- [indygreg](https://github.com/indygreg) for python-zstandard
- [yaml](https://github.com/yaml) for pyyaml  
Also, I want to give a special thanks to [aboood40091](https://github.com/aboood40091/) for explaining to me how a bunch of stuff in SarcLib works, as well as for giving me the `exists` function.
