#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Super Mario Maker 2 Mod Merger
# A Tool For Merging Super Mario Maker 2 Mods
# Version 0.2
# Created By MarioPossamato
#
# This File Is Part Of Super Mario Maker 2 Mod Merger
#
# A Copy Of Super Mario Maker 2 (01009B90006DC800) v327680 (3.0.1)
# Is Required For This Script To Work Correctly.  As One Is
# Not Packaged With Super Mario Maker 2 Mod Merger, You Will
# Need https://github.com/DarkMatterCore/nxdumptool/releases
# To Dump One.
#
# The Filesystem Should Resemble The Following:
#
# SuperMarioMaker2ModMerger
# └───SuperMarioMaker2
#     ├───exefs
#     └───romfs
#         ├───Bake
#         ├───Course
#         ├───CourseInfo
#         ├───Effect
#         ├───ELink2
#         ├───Env
#         ├───Event
#         ├───EventFlow
#         ├───Font
#         ├───Layout
#         ├───Map
#         ├───Message
#         ├───Mii
#         ├───Model
#         ├───MyWorld
#         ├───Pack
#         ├───Palette
#         ├───Replay
#         │   └───Lesson
#         ├───Rumble
#         ├───SLink2
#         ├───Sound
#         │   ├───Effect
#         │   ├───Resource
#         │   │   └───Stream
#         │   └───ResourceList
#         └───System
#             ├───Font
#             └───WordList
#
# Also, Merging Multiple Mods May Take Some Time, So Be Patient! :)
#
#============================================#
#
#==== Imports ====#
import os, pathlib, time
import zstd # Zstandard Compression Library: https://github.com/sergey-dryabzhinsky/python-zstd
import zstandard # Another Zstandard Compression Library: https://github.com/indygreg/python-zstandard
import libyaz0 # Yaz0 Compression Library By MasterVermilli0n/AboodXD: https://github.com/aboood40091/libyaz0
import sarc # Archive File Library: https://github.com/zeldamods/sarc/
import SarcLib # Archive File Library By MasterVermilli0n/AboodXD: https://github.com/aboood40091/SarcLib
#============================================#

SuperMarioMaker2 = "SuperMarioMaker2" #==== Super Mario Maker 2 Directory ====#
SuperMarioMaker2ModMergerOutput = "SuperMarioMaker2ModMergerOutput" #==== Super Mario Maker 2 Mod Merger Output Directory ====#
SuperMarioMaker2Mods = [ #==== Mods To Merge ====#
    "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample1",
    "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample2"
    #==== Add More Mods Here, Or Replace Those Above ====#
    # "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample3",
    # "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample4",
    # "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample5",
    # "SuperMarioMaker2Mods\\SuperMarioMaker2ModExample6"
]

#==== Check If The Directories Exist ====#

if os.path.exists(SuperMarioMaker2):
    pass
else:
    raise Exception('Super Mario Maker 2 Location Not Found!')

if os.path.exists(SuperMarioMaker2ModMergerOutput):
    pass
else:
    os.mkdir(SuperMarioMaker2ModMergerOutput)

for SuperMarioMaker2Mod in SuperMarioMaker2Mods:
    if os.path.exists(SuperMarioMaker2Mod):
        pass
    else:
        raise Exception('Super Mario Maker 2 Mod Location Not Found!')

#========================================#

def main():
    print("Merging Super Mario Maker 2 Mods, Please Wait...")
    for SuperMarioMaker2Mod in SuperMarioMaker2Mods: #==== Loop For Every Mod To Merge ====#
        for path, subdirs, files in os.walk(SuperMarioMaker2Mod):
            Replacements = [] #==== Create A List Of Replacements ====#

            for file in files: #==== Loop For Every File In The Mod ====#

                file_path = path[len(SuperMarioMaker2Mod):]+"\\"+file #==== Path Where The Archive File Is Located Inside The Game Files ====#

                if os.path.exists(SuperMarioMaker2+file_path):

                    print(SuperMarioMaker2Mod+file_path)

                    #==== Check If File Exists In Original Game Dump ====#
                    if os.path.exists(SuperMarioMaker2+file_path):

                        #==== Create Old And New Archive Objects For Data Comparison ====#
                        original_archive = SuperMarioMaker2+file_path
                        if original_archive.endswith(".zs"): #==== Check If The Original File Is A Zstandard Compressed SARC Archive File ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            old_archive.load(zstandard.decompress(open(SuperMarioMaker2+file_path, "rb").read()))
                        elif original_archive.endswith(".szs"): #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            old_archive.load(libyaz0.decompress(open(SuperMarioMaker2+file_path, "rb").read())) #==== Read/Decompress Original YAZ0 SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                        elif os.path.splitext(original_archive)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#:
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            old_archive.load(open(SuperMarioMaker2+file_path, "rb").read()) #==== Original Super Mario Maker 2 Archive ====#
                        else:
                            if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]): #==== Check If The Directory Exists ====#
                                os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]) #==== Create Directories ====#
                                open(SuperMarioMaker2ModMergerOutput+file_path, "wb").write(open(SuperMarioMaker2Mod+file_path, "rb").read()) #==== Create File ====#
                            else:
                                open(SuperMarioMaker2ModMergerOutput+file_path, "wb").write(open(SuperMarioMaker2Mod+file_path, "rb").read()) #==== Create File ====#

                    if file.endswith(".zs"): #==== Check If The File Is A Zstandard Compressed SARC Archive File ====#
                        _new_archive_ = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                        new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress zstandard SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                    elif file.endswith(".szs"): #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                        _new_archive_ = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                        new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress YAZ0 SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                    else:
                        if os.path.splitext(file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#
                            _new_archive_ = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()) #==== Read SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                        else:
                            print(False)

                    for file_name in _new_archive_.list_files(): #==== Compare Data For Each File Inside The Archive
                        print(pathlib.PurePath(file_name))

                        if old_archive[file_name].data == new_archive[file_name].data: #==== Compare The New Archive's File's Data To The Original Archive's File's Data ====#
                            pass
                        else:
                            Replacements.append([file_name, new_archive[file_name].data]) #==== Append The File's Name And Data To The Replacements List For Later Use====#

                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]): #==== Check If Directories Exist ====#
                        os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]) #==== Create Directories ====#
                    else:
                        pass

                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file): #==== Check If File Exists ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "wb").write(open(SuperMarioMaker2+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()) #==== Create File ====#
                    else:
                        pass

                    if (SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file).endswith(".zs"): #==== Check If The Output File Is A Zstandard Compressed SARC Archive File ====#
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                        output_archive.load(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check If The Output File Is A Yaz0 Compressed SARC Archive File ====#
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                        output_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#::
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                        output_archive.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())
                    else:
                        print(False)

                    for Replacement in Replacements:
                        if os.path.split(Replacement[0])[0]:
                            try:
                                output_archive[os.path.split(Replacement[0])[0]].removeFile(output_archive[Replacement[0]]) #==== Remove File(s) From Archive ====#
                            except:
                                pass
                        else:
                            try:
                                output_archive.removeFile(output_archive[Replacement[0]]) #==== Remove File(s) From Archive ====#
                            except:
                                pass

                        output_archive.addFile(SarcLib.File(Replacement[0], Replacement[1], True)) #==== Add File(s) To Archive ====#

                    data, maxAlignment = output_archive.save() #==== Save The Archive To A Bytes Object That Can Be Saved To A File ====#

                    if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".zs": #==== Check If The File Is A Zstandard Compressed SARC Archive File ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(zstandard.compress(data))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(libyaz0.compress(data, maxAlignment, level=3))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#:
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(data)
                    else:
                        print(False)

                else:
                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+file_path):
                        open(SuperMarioMaker2ModMergerOutput+file_path, 'wb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read())
                    else:
                        Replacements = []
                        file = SuperMarioMaker2Mod+file_path
                        if file.endswith(".zs"): #==== Check If The File Is A Zstandard Compressed SARC Archive File ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            old_archive.load(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read())) #==== Read/Decompress zstandard SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                            _new_archive_ = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress zstandard SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress zstandard SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                        elif file.endswith(".szs"): #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            old_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read())) #==== Read/Decompress YAZ0 SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                            _new_archive_ = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                            new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress YAZ0 SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                        else:
                            if os.path.splitext(file) in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#
                                old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                                old_archive.load(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read()) #==== Read SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                                _new_archive_ = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()) #==== Read SARC Archive File And Use It To Create New sarc.SARC Object ====#
                                new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive Object ====#
                                new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()) #==== Read SARC Archive File And Use It To Create New SarcLib.FileArchive.SARC_Archive Object ====#
                            else:
                                open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read())

                        for file_name in _new_archive_.list_files(): #==== Compare Data For Each File Inside The Archive
                            print(pathlib.PurePath(file_name))

                        if old_archive[file_name].data == new_archive[file_name].data: #==== Compare The New Archive's File's Data To The Original Archive's File's Data ====#
                            pass
                        else:
                            Replacements.append([file_name, new_archive[file_name].data]) #==== Append The File's Name And Data To The Replacements List For Later Use====#

                        for Replacement in Replacements:
                            if os.path.split(Replacement[0])[0]:
                                try:
                                    output_archive[os.path.split(Replacement[0])[0]].removeFile(output_archive[Replacement[0]]) #==== Remove File(s) From Archive ====#
                                except:
                                    pass
                            else:
                                try:
                                    output_archive.removeFile(output_archive[Replacement[0]]) #==== Remove File(s) From Archive ====#
                                except:
                                    pass

                        output_archive.addFile(SarcLib.File(Replacement[0], Replacement[1], True)) #==== Add File(s) To Archive ====#

                        data, maxAlignment = output_archive.save() #==== Save The Archive To A Bytes Object That Can Be Saved To A File ====#

                        if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".zs": #==== Check If The File Is A Zstandard Compressed SARC Archive File ====#
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(zstandard.compress(data))
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(libyaz0.compress(data, maxAlignment, level=3))
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Archive File ====#:
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(data)
                        else:
                            print(False)

    print("All Super Mario Maker 2 Mods Successfully Merged...")

if __name__ == "__main__": main()
