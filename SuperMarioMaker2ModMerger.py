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
# The Filesystem Should Resemble The Following
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
#==== Imports ====#
import os, pathlib, time
import zstd # Zstandard Compression Library
import zstandard # Zstandard Compression Library
import libyaz0 # Yaz0 Compression Library
import sarc # Archive File Library
import byml # Binary YML File Module
# from msbt import MSBT # Message File Module
#============================================#
#
# New Additions In SuperMarioMaker2ModMerger v0.2:
# ├───Added Decompression/Compression For Yaz0 Compressed SARC Archives
# └───Fixed Some Errors With Creating sarc.sarc.SARCWriter Objects

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

def main():
    print("Merging Super Mario Maker 2 Mods, Please Wait...")
    for SuperMarioMaker2Mod in SuperMarioMaker2Mods: #==== Loop For Every Mod To Merge ====#
        for path, subdirs, files in os.walk(SuperMarioMaker2Mod):
            Replacements = [] #==== Create A List Of Replacements ====#

            for file in files: #==== Loop For Every File In The Mod ====#

                file_path = path[len(SuperMarioMaker2Mod):]+"\\"+file #==== Path Where The Archive File Is Located Inside The Game Files ====#

                print(SuperMarioMaker2Mod+file_path)

                #==== Check If File Exists In Original Game Dump ====#
                if os.path.exists(SuperMarioMaker2+file_path):

                    #==== Create Old And New Archive Objects For Data Comparison ====#
                    original_archive = SuperMarioMaker2+file_path
                    if original_archive.endswith(".zs"): #==== Check If The Original File Is A Zstandard Compressed SARC Archive File ====#
                        old_archive = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2+file_path, "rb").read())) #==== Read/Decompress Original zstandard SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                    elif original_archive.endswith(".szs"): #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                        old_archive = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2+file_path, "rb").read())) #==== Read/Decompress Original YAZ0 SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                    elif os.path.splitext(original_archive)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Arhive File ====#:
                        old_archive = sarc.SARC(open(SuperMarioMaker2+file_path, "rb").read()) #==== Original Super Mario Maker 2 Archive ====#
                    else:
                        if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]): #==== Check If The Directory Exists ====#
                            os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]) #==== Create Directories ====#
                            open(SuperMarioMaker2ModMergerOutput+file_path, "wb").write(open(SuperMarioMaker2Mod+file_path, "rb").read()) #==== Create File ====#
                        else:
                            open(SuperMarioMaker2ModMergerOutput+file_path, "wb").write(open(SuperMarioMaker2Mod+file_path, "rb").read()) #==== Create File ====#

                if file.endswith(".zs"): #==== Check If The File Is A Zstandard Compressed SARC Archive File ====#
                    new_archive = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress zstandard SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                elif file.endswith(".szs"): #==== Check If The File Is A Yaz0 Compressed SARC Archive File ====#
                    new_archive = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())) #==== Read/Decompress YAZ0 SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                else:
                    if os.path.splitext(file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Arhive File ====#
                        new_archive = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()) #==== Read SARC Archive File And Use It To Create New sarc.sarc.SARC Object ====#
                    else:
                        print(False)

                file_names = [] #==== List To Store A List Of All Files In Archive ====#

                for file_name in new_archive.list_files(): #==== Compare Data For Each File Inside The Archive

                    file_names.append(file_name) #==== Add File To List ====#

                    #==== Show Files In A File Tree ====#
                    if file_names.index(file_name)+1 == len(new_archive.list_files()):
                        print("└───"+str(pathlib.PurePath(file_name)))
                    else:
                        print("├───"+str(pathlib.PurePath(file_name)))

                    if old_archive.get_file_data(file_name) == new_archive.get_file_data(file_name):
                        pass
                    else:
                        Replacements.append([file_name, new_archive.get_file_data(file_name)]) #==== Append The File's Name And Data To The Replacements List ====#

                if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]):
                    os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):])
                else:
                    pass
                if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file):
                    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "wb").write(open(SuperMarioMaker2+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())
                else:
                    pass

                if (SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file).endswith(".zs"): #==== Check If The Output File Is A Zstandard Compressed SARC Archive File ====#
                    output_archive = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check If The Output File Is A Yaz0 Compressed SARC Archive File ====#
                    output_archive = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Arhive File ====#::
                    output_archive = sarc.SARC(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())
                else:
                    print(False)

                for Replacement in Replacements:
                    if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".zs": #==== Check Again If The File Is A Zstandard Compressed SARC Archive File ====#
                        output_data = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check Again If The File Is A Yaz0 Compressed SARC Archive File ====#
                        output_data = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read()))
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Arhive File ====#::
                        output_data = sarc.SARC(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file, "rb").read())
                    else:
                        print(False)
                    writer = sarc.make_writer_from_sarc(output_data)
                    writer.add_file(Replacement[0], Replacement[1])

                if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".zs": #==== Check One More Time If The File Is A Zstandard Compressed SARC Archive File ====#
                    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(zstandard.compress(writer.get_bytes()))
                elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] == ".szs": #==== Check One More Time If The File Is A Yaz0 Compressed SARC Archive File ====#
                    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(libyaz0.compress(writer.get_bytes(), level=3))
                elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file)[1] in [".sarc", ".pack", ".arc"]: #==== Check If File Is Still A Valid SARC Arhive File ====#:
                    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+"\\"+file,"wb").write(writer.get_bytes())
                else:
                    print(False)

    print("All Super Mario Maker 2 Mods Successfully Merged...")
if __name__ == "__main__":main()
