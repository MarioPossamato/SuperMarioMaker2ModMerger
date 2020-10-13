#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Super Mario Maker 2 Mod Merger (SMM2MM)
# A Tool For Merging Super Mario Maker 2 Mods
# Version 0.2
# Created By MarioPossamato
#
# This File Is Part Of Super Mario Maker 2 Mod Merger
#
# A copy of Super Mario Maker 2 (01009B90006DC800) v327680 (3.0.1)
# is required for SMM2MM to execute properly.  Since one is not packaged
# with it, due to legal reasons, you will need to acquire one by using
# this tool: https://github.com/DarkMatterCore/nxdumptool/releases
#
# The filesystem should resemble the following:
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
# Also, merging multiple SMM2 mods may take a while, so please be patient! ☺
#
#==== Module and library imports ====#
import sys             # Built-in module
import os              # Built-in module
import io              # Built-in module
import time            # Built-in module
import pathlib         # Built-in library
import json            # Built-in library
import yaml            # Yaml ain't markup language library: https://github.com/yaml/pyyaml
import zstd, zstandard # Zstandard compression libraries: https://github.com/sergey-dryabzhinsky/python-zstd, https://github.com/indygreg/python-zstandard
import sarc, SarcLib   # Sarc archive libraries: https://github.com/zeldamods/sarc/, https://github.com/aboood40091/SarcLib
import libyaz0, syaz0  # Yaz0 compression libraries: https://github.com/aboood40091/libyaz0, https://github.com/zeldamods/syaz0
import byml, oead.byml # Binary yaml libraries: https://github.com/zeldamods/byml-v2, https://github.com/zeldamods/oead
from byml import yaml_util
#====================================#
SMM2MM_Version = 0.2
#====================================#
SuperMarioMaker2 = 'SuperMarioMaker2'
SuperMarioMaker2ModMergerOutput = 'SuperMarioMaker2ModMergerOutput'
SuperMarioMaker2Mods = [ #==== Mods to merge ====#
        'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample1',
        'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample2'
        #==== More mods here ====#
        # 'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample3',
        # 'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample4',
        # 'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample5',
        # 'SuperMarioMaker2Mods\\SuperMarioMaker2ModExample6'
        ]
#====================================#
def exists(sarc, filename):
    try:
        sarc[filename]
    except KeyError:
        return False
    return True
#====================================#
def merge(): #==== Main function ====#

    print('Merging Super Mario Maker 2 Mods, Please Wait...')

    Pack = {} #==== Create a dict object ====#
    Pack['M1'] = []
    Pack['M3'] = []
    Pack['MW'] = []
    Pack['WU'] = []
    Pack['3W'] = []
    Pack['Enemy'] = []
    Pack['Edit'] = []

    for SuperMarioMaker2Mod in SuperMarioMaker2Mods: #==== Loop for each mod ====#
        for path, subdirs, files in os.walk(SuperMarioMaker2Mod):
            Replacements = [] #==== Create a 'Replacements' list object ====#
            for file in files: #==== Loop for every file in the mod ====#
                file_path = path[len(SuperMarioMaker2Mod):]+'\\'+file #==== Path where the archive file is located inside the game files ====#
                if os.path.exists(SuperMarioMaker2+file_path): #==== Check if the file exists in the original Super Mario Maker 2 game files ====#
                    print(SuperMarioMaker2Mod+file_path)
    
                    #==== Original archive ====#
                    originalarcpath = SuperMarioMaker2+file_path
                    if originalarcpath.endswith('.zs'): #==== Check if the original file is a zstandard compressed sarc archive file ====#
                        old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        old_archive.load(zstandard.decompress(open(SuperMarioMaker2+file_path, 'rb').read())) #==== Read/decompress original file and load it ====#
                    elif originalarcpath.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        old_archive.load(libyaz0.decompress(open(SuperMarioMaker2+file_path, 'rb').read())) #==== Read/decompress original file and load it ====#
                    elif os.path.splitext(originalarcpath)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                        old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        old_archive.load(open(SuperMarioMaker2+file_path, 'rb').read()) #==== Read original file and load it ====#
                    else:
                        if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]): #==== Check If The Directory Exists ====#
                            os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):], mode=511, exist_ok=True) #==== Create Directories ====#
                            open(SuperMarioMaker2ModMergerOutput+file_path, 'wb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Create File ====#
                        else:
                                open(SuperMarioMaker2ModMergerOutput+file_path, 'wb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Create File ====#

                    #==== New archive ====#
                    if file.endswith('.zs'): #==== Check if the original file is a zstandard compressed sarc archive file ====#
                        _newarc = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Create sarc.sarc.SARC object.  This is later used for _newarc.list_files() ====#
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    elif file.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        _newarc = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Create sarc.sarc.SARC object ====#
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    else:
                        if os.path.splitext(file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                            _newarc = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Create sarc.sarc.SARC object.  This is later used for _newarc.list_files() ====#
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Read new file and load it ====#
                        else:
                            print(False)

                    if os.path.split(SuperMarioMaker2Mod+file_path)[1] == 'Static.pack':
                        info = {} #==== Create dict object ====#

                        #==== M1 ====#
                        if exists(old_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                            info['M1_old_info'] = oead.byml.from_binary(old_archive['Mush\\M1_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                            info['M1_new_info'] = oead.byml.from_binary(new_archive['Mush\\M1_SceneDB.byml'].data)
                        for i in range(len(list(info['M1_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['M1_new_info'])[i]) == dict(list(info['M1_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    Pack['M1'].append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                            except:
                                Pack['M1'].append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== M3 ====#
                        if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['M3_old_info'] = oead.byml.from_binary(old_archive['Mush\\M3_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['M3_new_info'] = oead.byml.from_binary(new_archive['Mush\\M3_SceneDB.byml'].data)
                            for i in range(len(list(info['M3_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['M3_new_info'])[i]) == dict(list(info['M3_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['M3'].append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['M3'].append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== MW ====#
                        if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['MW_old_info'] = oead.byml.from_binary(old_archive['Mush\\MW_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['MW_new_info'] = oead.byml.from_binary(new_archive['Mush\\MW_SceneDB.byml'].data)
                            for i in range(len(list(info['MW_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['MW_new_info'])[i]) == dict(list(info['MW_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['MW'].append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['MW'].append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== WU ====#
                        if exists(old_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                            info['WU_old_info'] = oead.byml.from_binary(old_archive['Mush\\WU_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                            info['WU_new_info'] = oead.byml.from_binary(new_archive['Mush\\WU_SceneDB.byml'].data)
                            for i in range(len(list(info['WU_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['WU_new_info'])[i]) == dict(list(info['WU_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['WU'].append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['WU'].append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== 3W ====#
                        if exists(old_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                            info['3W_old_info'] = oead.byml.from_binary(old_archive['Mush\\3W_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                            info['3W_new_info'] = oead.byml.from_binary(new_archive['Mush\\3W_SceneDB.byml'].data)
                            for i in range(len(list(info['3W_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['3W_new_info'])[i]) == dict(list(info['3W_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['3W'].append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['3W'].append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== EnemyDB_game ====#
                        if exists(old_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                            info['EnemyDB_game_old_info'] = oead.byml.from_binary(old_archive['Mush\\EnemyDB_game.byml'].data)
                        if exists(new_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                            info['EnemyDB_game_new_info'] = oead.byml.from_binary(new_archive['Mush\\EnemyDB_game.byml'].data)
                            for i in range(len(list(info['EnemyDB_game_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['EnemyDB_game_new_info'])[i]) == dict(list(info['EnemyDB_game_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['Enemy'].append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['Enemy'].append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                        #==== EditDB_common ====#
                        if exists(old_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                            info['EditDB_common_old_info'] = oead.byml.from_binary(old_archive['Mush\\EditDB_common.byml'].data)
                        if exists(new_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                            info['EditDB_common_new_info'] = oead.byml.from_binary(new_archive['Mush\\EditDB_common.byml'].data)
                            for i in range(len(list(info['EditDB_common_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['EditDB_common_new_info'])[i]) == dict(list(info['EditDB_common_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['Edit'].append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['Edit'].append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            for file_name in _newarc.list_files(): #==== Loop for each file inside the archive ====#
                                print(pathlib.PurePath(file_name))
                        else:
                            for file_name in _newarc.list_files(): #==== Loop for each file inside the archive ====#
                                print(pathlib.PurePath(file_name))

                                if old_archive[file_name].data == new_archive[file_name].data: #==== Compare the data of the file in the new archive to that of the file in the old archive ====#
                                    pass
                                else:
                                    Replacements.append([file_name, new_archive[file_name].data]) #==== Append the file's name and data in a list object to the 'Replacements' list ====#

                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]): #==== Check if directories exist ====#
                        os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):], mode=511, exist_ok=True) #==== Create directories ====#
                    else:
                        pass

                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file): #==== Check if file exists ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'wb').write(open(SuperMarioMaker2+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Create file ====#
                    else:
                        pass

                    #==== Output archive ====#
                    if (SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file).endswith('.zs'): #==== Check if the output file is a zstandard compressed sarc archive file ====#
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        output_archive.load(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.szs': #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        output_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                        output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        output_archive.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Read new file and load it ====#
                    else:
                        print(False)

                    #==== Apply changes to the file using the 'Replacements' list object ====#
                    for Replacement in Replacements: #==== Loop for each replacement ====#
                        if os.path.split(Replacement[0])[0]: #==== Check if file exists ====#
                            try:
                                output_archive[os.path.split(Replacement[0])[0]].removeFile(output_archive[Replacement[0]]) #==== Remove file from archive ====#
                            except:
                                pass
                        else:
                            try:
                                output_archive.removeFile(output_archive[Replacement[0]]) #==== Remove file from archive ====#
                            except:
                                pass

                        output_archive.addFile(SarcLib.File(Replacement[0], Replacement[1], True)) #==== Add file to archive ====#

                    data, maxAlignment = output_archive.save() #==== Save the archive to a bytes object that can be saved to a file ====#

                    if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.zs': #==== Check if the file is a zstandard compressed sarc archive file ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(zstandard.compress(data)) #==== Write data to file ====#
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.szs': #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(libyaz0.compress(data, maxAlignment, level=3)) #==== Write data to file ====#
                    elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(data) #==== Write data to file ====#
                    else:
                        print(False)

                else:
                    if not os.path.exists(SuperMarioMaker2ModMergerOutput+file_path): #==== Check if the file exists in the SMM2MM output folder ====#
                        os.makedirs(os.path.split(SuperMarioMaker2ModMergerOutput+file_path)[0], mode=511, exist_ok=True) #==== Create directories ====#
                        open(SuperMarioMaker2ModMergerOutput+file_path, 'wb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Create file ====#
                    else:
                        Replacements = []
                        if file.endswith('.zs'): #==== Check if the file is a zstandard compressed sarc archive file ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            old_archive.load(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                            _newarc = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Create sarc.sarc.SARC object.  This is later used for _newarc.list_files() ====#
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                        elif file.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            old_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                            _newarc = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()))
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                        else:
                            if os.path.splitext(file) in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                                old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                old_archive.load(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read()) #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                _newarc = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Create sarc.sarc.SARC object.  This is later used for _newarc.list_files() ====#
                                new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Read new file and load it ====#
                            else:
                                open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read())

                        if os.path.split(SuperMarioMaker2Mod+file_path)[1] == 'Static.pack':

                            info = {} #==== Create dict object ====#

                            #==== M1 ====#
                            if exists(old_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                                info['M1_old_info'] = oead.byml.from_binary(old_archive['Mush\\M1_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                                info['M1_new_info'] = oead.byml.from_binary(new_archive['Mush\\M1_SceneDB.byml'].data)
                            for i in range(len(list(info['M1_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['M1_new_info'])[i]) == dict(list(info['M1_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        Pack['M1'].append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                except:
                                    Pack['M1'].append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== M3 ====#
                            if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['M3_old_info'] = oead.byml.from_binary(old_archive['Mush\\M3_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['M3_new_info'] = oead.byml.from_binary(new_archive['Mush\\M3_SceneDB.byml'].data)
                                for i in range(len(list(info['M3_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['M3_new_info'])[i]) == dict(list(info['M3_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['M3'].append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['M3'].append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== MW ====#
                            if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['MW_old_info'] = oead.byml.from_binary(old_archive['Mush\\MW_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['MW_new_info'] = oead.byml.from_binary(new_archive['Mush\\MW_SceneDB.byml'].data)
                                for i in range(len(list(info['MW_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['MW_new_info'])[i]) == dict(list(info['MW_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['MW'].append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['MW'].append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== WU ====#
                            if exists(old_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                                info['WU_old_info'] = oead.byml.from_binary(old_archive['Mush\\WU_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                                info['WU_new_info'] = oead.byml.from_binary(new_archive['Mush\\WU_SceneDB.byml'].data)
                                for i in range(len(list(info['WU_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['WU_new_info'])[i]) == dict(list(info['WU_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['WU'].append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['WU'].append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== 3W ====#
                            if exists(old_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                                info['3W_old_info'] = oead.byml.from_binary(old_archive['Mush\\3W_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                                info['3W_new_info'] = oead.byml.from_binary(new_archive['Mush\\3W_SceneDB.byml'].data)
                                for i in range(len(list(info['3W_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['3W_new_info'])[i]) == dict(list(info['3W_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['3W'].append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['3W'].append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== EnemyDB_game ====#
                            if exists(old_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                                info['EnemyDB_game_old_info'] = oead.byml.from_binary(old_archive['Mush\\EnemyDB_game.byml'].data)
                            if exists(new_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                                info['EnemyDB_game_new_info'] = oead.byml.from_binary(new_archive['Mush\\EnemyDB_game.byml'].data)
                                for i in range(len(list(info['EnemyDB_game_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['EnemyDB_game_new_info'])[i]) == dict(list(info['EnemyDB_game_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['Enemy'].append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['Enemy'].append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                            #==== EditDB_common ====#
                            if exists(old_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_old_info'] = oead.byml.from_binary(old_archive['Mush\\EditDB_common.byml'].data)
                            if exists(new_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_new_info'] = oead.byml.from_binary(new_archive['Mush\\EditDB_common.byml'].data)
                                for i in range(len(list(info['EditDB_common_new_info']))): #==== Loop for every item in each list ====#
                                    try:
                                        if dict(list(info['EditDB_common_new_info'])[i]) == dict(list(info['EditDB_common_old_info'])[i]): #==== Check if both items are equal or not ====#
                                            pass
                                        else:
                                            Pack['Edit'].append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#
                                    except:
                                        Pack['Edit'].append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the 'Pack' dict object ====#

                                for file_name in _newarc.list_files(): #==== Loop for each file inside the archive ====#
                                    print(pathlib.PurePath(file_name))
                            else:
                                for file_name in _newarc.list_files(): #==== Loop for each file inside the archive ====#
                                    print(pathlib.PurePath(file_name))

                                    if old_archive[file_name].data == new_archive[file_name].data: #==== Compare the data of the file in the new archive to that of the file in the old archive ====#
                                        pass
                                    else:
                                        Replacements.append([file_name, new_archive[file_name].data]) #==== Append the file's name and data in a list object to the 'Replacements' list ====#

                        #==== Output archive ====#
                        if (SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file).endswith('.zs'): #==== Check if the output file is a zstandard compressed sarc archive file ====#
                            output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            output_archive.load(zstandard.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.szs': #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                            output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            output_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                            output_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            output_archive.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Read new file and load it ====#
                        else:
                            print(False)

                        #==== Apply changes to the file using the 'Replacements' list object ====#
                        for Replacement in Replacements: #==== Loop for each replacement ====#
                            if os.path.split(Replacement[0])[0]: #==== Check if file exists ====#
                                try:
                                    output_archive[os.path.split(Replacement[0])[0]].removeFile(output_archive[Replacement[0]]) #==== Remove file from archive ====#
                                except:
                                    pass
                            else:
                                try:
                                    output_archive.removeFile(output_archive[Replacement[0]]) #==== Remove file from archive ====#
                                except:
                                    pass

                            output_archive.addFile(SarcLib.File(Replacement[0], Replacement[1], True)) #==== Add file to archive ====#

                        data, maxAlignment = output_archive.save() #==== Save the archive to a bytes object that can be saved to a file ====#

                        if os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.zs': #==== Check if the file is a zstandard compressed sarc archive file ====#
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(zstandard.compress(data)) #==== Write data to file ====#
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] == '.szs': #==== Check if the file is a yaz0 compressed sarc archive file ====#
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(libyaz0.compress(data, maxAlignment, level=3)) #==== Write data to file ====#
                        elif os.path.splitext(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                            open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file,'wb').write(data) #==== Write data to file ====#
                        else:
                            print(False)

    if not os.path.exists(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack'): #==== Check if file exists ====#
        os.makedirs(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):], mode=511, exist_ok=True) #==== Create directories ====#
        open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'wb').write(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', "rb").read()) #==== Create file ====#
        arc = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
        arc.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'rb').read()) #==== Read new file and load it ====#
    else:
        arc = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
        arc.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'rb').read()) #==== Read new file and load it ====#

    info = {} #==== Create dict object ====#

    #==== M1 ====#
    if exists(arc, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
        info['M1_new_info'] = oead.byml.from_binary(arc['Mush\\M1_SceneDB.byml'].data)
        for r in Pack['M1']:
            info['M1_new_info'][Pack['M1'][0]] = Pack['M1'][1]

    #==== M3 ====#
    if exists(arc, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
        info['M3_new_info'] = oead.byml.from_binary(arc['Mush\\M3_SceneDB.byml'].data)
        for r in Pack['M3']:
            info['M3_new_info'][Pack['M3'][0]] = Pack['M3'][1]

    #==== MW ====#
    if exists(arc, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
        info['MW_new_info'] = oead.byml.from_binary(arc['Mush\\MW_SceneDB.byml'].data)
        for r in Pack['MW']:
            info['MW_new_info'][Pack['MW'][0]] = Pack['MW'][1]

    #==== WU ====#
    if exists(arc, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
        info['WU_new_info'] = oead.byml.from_binary(arc['Mush\\WU_SceneDB.byml'].data)
        for r in Pack['WU']:
            info['WU_new_info'][Pack['WU'][0]] = Pack['WU'][1]

    #==== 3W ====#
    if exists(arc, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
        info['3W_new_info'] = oead.byml.from_binary(arc['Mush\\3W_SceneDB.byml'].data)
        for r in Pack['3W']:
            info['3W_new_info'][Pack['3W'][0]] = Pack['3W'][1]

    #==== EnemyDB_game ====#
    if exists(arc, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
        info['EnemyDB_game_new_info'] = oead.byml.from_binary(arc['Mush\\EnemyDB_game.byml'].data)
        for r in Pack['Enemy']:
            info['EnemyDB_game_new_info'][Pack['Enemy'][0]] = Pack['Enemy'][1]

    #==== EditDB_common ====#
    if exists(arc, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
        info['EditDB_common_new_info'] = oead.byml.from_binary(arc['Mush\\EditDB_common.byml'].data)
        for r in Pack['Edit']:
            info['EditDB_common_new_info'][Pack['Edit'][0]] = Pack['Edit'][1]

    yaml_util.add_constructors(yaml.CLoader)

    #==== M1 ====#
    text_M1 = oead.byml.to_text(info['M1_new_info'])
    text_M1 = yaml.load(text_M1, Loader=yaml.CLoader)
    buf_M1 = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_M1).write(buf_M1) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== M3 ====#
    text_M3 = oead.byml.to_text(info['M3_new_info'])
    text_M3 = yaml.load(text_M3, Loader=yaml.CLoader)
    buf_M3 = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_M3).write(buf_M3) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== MW ====#
    text_MW = oead.byml.to_text(info['MW_new_info'])
    text_MW = yaml.load(text_MW, Loader=yaml.CLoader)
    buf_MW = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_MW).write(buf_MW) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== WU ====#
    text_WU = oead.byml.to_text(info['WU_new_info'])
    text_WU = yaml.load(text_WU, Loader=yaml.CLoader)
    buf_WU = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_WU).write(buf_WU) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== 3W ====#
    text_3W = oead.byml.to_text(info['3W_new_info'])
    text_3W = yaml.load(text_3W, Loader=yaml.CLoader)
    buf_3W = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_3W).write(buf_3W) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== EnemyDB_game ====#
    text_Enemy = oead.byml.to_text(info['EnemyDB_game_new_info'])
    text_Enemy = yaml.load(text_Enemy, Loader=yaml.CLoader)
    buf_Enemy = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_Enemy).write(buf_Enemy) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== EditDB_common ====#
    text_Edit = oead.byml.to_text(info['EditDB_common_new_info'])
    text_Edit = yaml.load(text_Edit, Loader=yaml.CLoader)
    buf_Edit = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(text_Edit).write(buf_Edit) #==== Convert to byml and write to _io.BytesIO object ====#

    arc['Mush/M1_SceneDB.byml'].data = (buf_M1.getbuffer()) #==== M1 ====#
    arc['Mush/M3_SceneDB.byml'].data = (buf_M3.getbuffer()) #==== M3 ====#
    arc['Mush/MW_SceneDB.byml'].data = (buf_MW.getbuffer()) #==== MW ====#
    arc['Mush/WU_SceneDB.byml'].data = (buf_WU.getbuffer()) #==== WU ====#
    arc['Mush/3W_SceneDB.byml'].data = (buf_3W.getbuffer()) #==== 3W ====#
    arc['Mush/EnemyDB_game.byml'].data = (buf_Enemy.getbuffer()) #==== EnemyDB_game ====#
    arc['Mush/EditDB_common.byml'].data = (buf_Edit.getbuffer()) #==== EditDB_common ====#

    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'wb').write(arc.save()[0]) #==== Save to file ====#

    print('All Super Mario Maker 2 Mods Successfully Merged...') #==== Let user know that the script has finished merging their mods ====#

if __name__ == '__main__': merge() #==== Call merge function ====#
