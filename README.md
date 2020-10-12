# SuperMarioMaker2ModMerger
A Tool For Merging Super Mario Maker 2 Mods
Version 0.2

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

# Using this tool
- Open `SuperMarioMaker2ModMerger.py` in a text editor, such as Notepad or Notepad++;  
- Scroll down until you see the `SuperMarioMaker2Mods` variable definition;  
- Add the mods you want, remove the ones you don't, then hit save;  
- Run `SuperMarioMaker2ModMerger.bat` to merge them.

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
