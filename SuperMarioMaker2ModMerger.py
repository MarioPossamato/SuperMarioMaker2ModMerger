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

    print('Merging Super Mario Maker 2 Mods, Please Wait... ☺')

    _M1_Replacements_ = [] #==== Create a list object ====#
    _M3_Replacements_ = [] #==== Create a list object ====#
    _MW_Replacements_ = [] #==== Create a list object ====#
    _WU_Replacements_ = [] #==== Create a list object ====#
    _3W_Replacements_ = [] #==== Create a list object ====#
    _EnemyDB_game_Replacements_ = [] #==== Create a list object ====#
    _EditDB_common_Replacements_ = [] #==== Create a list object ====#

    for SuperMarioMaker2Mod in SuperMarioMaker2Mods: #==== Loop for each mod ====#
        for path, subdirs, files in os.walk(SuperMarioMaker2Mod):
            Replacements = [] #==== Create a 'Replacements' list object ====#
            for file in files: #==== Loop for every file in the mod ====#
                file_path = path[len(SuperMarioMaker2Mod):]+'\\'+file #==== Path where the archive file is located inside the game files ====#
                if os.path.exists(SuperMarioMaker2+file_path): #==== Check if the file exists in the original Super Mario Maker 2 game files ====#
                    print(SuperMarioMaker2Mod+file_path)
    
                    #==== Original archive ====#
                    original_archive_path = SuperMarioMaker2+file_path
                    if original_archive_path.endswith('.zs'): #==== Check if the original file is a zstandard compressed sarc archive file ====#
                        old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        old_archive.load(zstandard.decompress(open(SuperMarioMaker2+file_path, 'rb').read())) #==== Read/decompress original file and load it ====#
                    elif original_archive_path.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        old_archive.load(libyaz0.decompress(open(SuperMarioMaker2+file_path, 'rb').read())) #==== Read/decompress original file and load it ====#
                    elif os.path.splitext(original_archive_path)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
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
                        _new_archive_ = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Create sarc.sarc.SARC object.  This is later used for _new_archive_.list_files() ====#
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    elif file.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                        _new_archive_ = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Create sarc.sarc.SARC object ====#
                        new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                        new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read())) #==== Read/decompress new file and load it ====#
                    else:
                        if os.path.splitext(file)[1] in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                            _new_archive_ = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Create sarc.sarc.SARC object.  This is later used for _new_archive_.list_files() ====#
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+file, 'rb').read()) #==== Read new file and load it ====#
                        else:
                            print(False)

                    if os.path.split(SuperMarioMaker2Mod+file_path)[1] == 'Static.pack':
                        info = {} #==== Create dict object ====#
                        if exists(old_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                            info['M1_old_info'] = oead.byml.from_binary(old_archive['Mush\\M1_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                            info['M1_new_info'] = oead.byml.from_binary(new_archive['Mush\\M1_SceneDB.byml'].data)
                        for i in range(len(list(info['M1_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['M1_new_info'])[i]) == dict(list(info['M1_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _M1_Replacements_.append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _M1_Replacements_.append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                        if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['M3_old_info'] = oead.byml.from_binary(old_archive['Mush\\M3_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['M3_new_info'] = oead.byml.from_binary(new_archive['Mush\\M3_SceneDB.byml'].data)
                        for i in range(len(list(info['M3_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['M3_new_info'])[i]) == dict(list(info['M3_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _M3_Replacements_.append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _M3_Replacements_.append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                        if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['MW_old_info'] = oead.byml.from_binary(old_archive['Mush\\MW_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                            info['MW_new_info'] = oead.byml.from_binary(new_archive['Mush\\MW_SceneDB.byml'].data)
                        for i in range(len(list(info['MW_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['MW_new_info'])[i]) == dict(list(info['MW_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _MW_Replacements_.append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _MW_Replacements_.append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                        if exists(old_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                            info['WU_old_info'] = oead.byml.from_binary(old_archive['Mush\\WU_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                            info['WU_new_info'] = oead.byml.from_binary(new_archive['Mush\\WU_SceneDB.byml'].data)
                        for i in range(len(list(info['WU_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['WU_new_info'])[i]) == dict(list(info['WU_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _WU_Replacements_.append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _WU_Replacements_.append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                        if exists(old_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                            info['3W_old_info'] = oead.byml.from_binary(old_archive['Mush\\3W_SceneDB.byml'].data)
                        if exists(new_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                            info['3W_new_info'] = oead.byml.from_binary(new_archive['Mush\\3W_SceneDB.byml'].data)
                        for i in range(len(list(info['3W_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['3W_new_info'])[i]) == dict(list(info['3W_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _3W_Replacements_.append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _3W_Replacements_.append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                        if exists(old_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                            info['EnemyDB_game_old_info'] = oead.byml.from_binary(old_archive['Mush\\EnemyDB_game.byml'].data)
                        if exists(new_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                            info['EnemyDB_game_new_info'] = oead.byml.from_binary(new_archive['Mush\\EnemyDB_game.byml'].data)
                        for i in range(len(list(info['EnemyDB_game_new_info']))): #==== Loop for every item in each list ====#
                            try:
                                if dict(list(info['EnemyDB_game_new_info'])[i]) == dict(list(info['EnemyDB_game_old_info'])[i]): #==== Check if both items are equal or not ====#
                                    pass
                                else:
                                    _EditDB_common_Replacements_.append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                            except:
                                _EditDB_common_Replacements_.append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_old_info'] = oead.byml.from_binary(old_archive['Mush\\EditDB_common.byml'].data)
                            if exists(new_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_new_info'] = oead.byml.from_binary(new_archive['Mush\\EditDB_common.byml'].data)
                            for i in range(len(list(info['EditDB_common_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['EditDB_common_new_info'])[i]) == dict(list(info['EditDB_common_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _EditDB_common_Replacements_.append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _EditDB_common_Replacements_.append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            for file_name in _new_archive_.list_files(): #==== Loop for each file inside the archive ====#
                                print(pathlib.PurePath(file_name))
                        else:
                            for file_name in _new_archive_.list_files(): #==== Loop for each file inside the archive ====#
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
                            _new_archive_ = sarc.SARC(zstandard.decompress(open(SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Create sarc.sarc.SARC object.  This is later used for _new_archive_.list_files() ====#
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(zstandard.decompress(open(SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                        elif file.endswith('.szs'): #==== Check if the original file is a yaz0 compressed sarc archive file ====#
                            old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            old_archive.load(libyaz0.decompress(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                            _new_archive_ = sarc.SARC(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()))
                            new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                            new_archive.load(libyaz0.decompress(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read())) #==== Read/decompress new file and load it ====#
                        else:
                            if os.path.splitext(file) in ['.sarc', '.pack', '.arc']: #==== Check if the file extension is that of an uncompressed sarc archive ====#
                                old_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                old_archive.load(open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').read()) #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                _new_archive_ = sarc.SARC(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Create sarc.sarc.SARC object.  This is later used for _new_archive_.list_files() ====#
                                new_archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
                                new_archive.load(open(SuperMarioMaker2Mod+path[len(SuperMarioMaker2Mod):]+'\\'+SuperMarioMaker2Mod+file_path, 'rb').read()) #==== Read new file and load it ====#
                            else:
                                open(SuperMarioMaker2ModMergerOutput+file_path, 'rb').write(open(SuperMarioMaker2Mod+file_path, 'rb').read())

                        if os.path.split(SuperMarioMaker2Mod+file_path)[1] == 'Static.pack':
                            info = {} #==== Create dict object ====#
                            if exists(old_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                                info['M1_old_info'] = oead.byml.from_binary(old_archive['Mush\\M1_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
                                info['M1_new_info'] = oead.byml.from_binary(new_archive['Mush\\M1_SceneDB.byml'].data)
                            for i in range(len(list(info['M1_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['M1_new_info'])[i]) == dict(list(info['M1_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _M1_Replacements_.append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _M1_Replacements_.append([i, list(info['M1_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['M3_old_info'] = oead.byml.from_binary(old_archive['Mush\\M3_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['M3_new_info'] = oead.byml.from_binary(new_archive['Mush\\M3_SceneDB.byml'].data)
                            for i in range(len(list(info['M3_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['M3_new_info'])[i]) == dict(list(info['M3_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _M3_Replacements_.append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _M3_Replacements_.append([i, list(info['M3_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['MW_old_info'] = oead.byml.from_binary(old_archive['Mush\\MW_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
                                info['MW_new_info'] = oead.byml.from_binary(new_archive['Mush\\MW_SceneDB.byml'].data)
                            for i in range(len(list(info['MW_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['MW_new_info'])[i]) == dict(list(info['MW_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _MW_Replacements_.append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _MW_Replacements_.append([i, list(info['MW_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                                info['WU_old_info'] = oead.byml.from_binary(old_archive['Mush\\WU_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
                                info['WU_new_info'] = oead.byml.from_binary(new_archive['Mush\\WU_SceneDB.byml'].data)
                            for i in range(len(list(info['WU_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['WU_new_info'])[i]) == dict(list(info['WU_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _WU_Replacements_.append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _WU_Replacements_.append([i, list(info['WU_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                                info['3W_old_info'] = oead.byml.from_binary(old_archive['Mush\\3W_SceneDB.byml'].data)
                            if exists(new_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
                                info['3W_new_info'] = oead.byml.from_binary(new_archive['Mush\\3W_SceneDB.byml'].data)
                            for i in range(len(list(info['3W_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['3W_new_info'])[i]) == dict(list(info['3W_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _3W_Replacements_.append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _3W_Replacements_.append([i, list(info['3W_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                                info['EnemyDB_game_old_info'] = oead.byml.from_binary(old_archive['Mush\\EnemyDB_game.byml'].data)
                            if exists(new_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
                                info['EnemyDB_game_new_info'] = oead.byml.from_binary(new_archive['Mush\\EnemyDB_game.byml'].data)
                            for i in range(len(list(info['EnemyDB_game_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['EnemyDB_game_new_info'])[i]) == dict(list(info['EnemyDB_game_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _EditDB_common_Replacements_.append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _EditDB_common_Replacements_.append([i, list(info['EnemyDB_game_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                            if exists(old_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_old_info'] = oead.byml.from_binary(old_archive['Mush\\EditDB_common.byml'].data)
                            if exists(new_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
                                info['EditDB_common_new_info'] = oead.byml.from_binary(new_archive['Mush\\EditDB_common.byml'].data)
                            for i in range(len(list(info['EditDB_common_new_info']))): #==== Loop for every item in each list ====#
                                try:
                                    if dict(list(info['EditDB_common_new_info'])[i]) == dict(list(info['EditDB_common_old_info'])[i]): #==== Check if both items are equal or not ====#
                                        pass
                                    else:
                                        _EditDB_common_Replacements_.append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#
                                except:
                                    _EditDB_common_Replacements_.append([i, list(info['EditDB_common_new_info'])[i]]) #==== Add replacement to the '_Replacements_' list ====#

                                for file_name in _new_archive_.list_files(): #==== Loop for each file inside the archive ====#
                                    print(pathlib.PurePath(file_name))
                            else:
                                for file_name in _new_archive_.list_files(): #==== Loop for each file inside the archive ====#
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
        _archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
        _archive.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'rb').read()) #==== Read new file and load it ====#
    else:
        _archive = SarcLib.SARC_Archive() #==== Create SarcLib.FileArchive.SARC_Archive object ====#
        _archive.load(open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'rb').read()) #==== Read new file and load it ====#

    info = {} #==== Create dict object ====#
    if exists(_archive, 'Mush\\M1_SceneDB.byml'): #==== Check if file exists ====#
        info['M1_new_info'] = oead.byml.from_binary(_archive['Mush\\M1_SceneDB.byml'].data)
    if exists(_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
        info['M3_new_info'] = oead.byml.from_binary(_archive['Mush\\M3_SceneDB.byml'].data)
    if exists(_archive, 'Mush\\M3_SceneDB.byml'): #==== Check if file exists ====#
        info['MW_new_info'] = oead.byml.from_binary(_archive['Mush\\MW_SceneDB.byml'].data)
    if exists(_archive, 'Mush\\MW_SceneDB.byml'): #==== Check if file exists ====#
        info['WU_new_info'] = oead.byml.from_binary(_archive['Mush\\WU_SceneDB.byml'].data)
    if exists(_archive, 'Mush\\WU_SceneDB.byml'): #==== Check if file exists ====#
        info['3W_new_info'] = oead.byml.from_binary(_archive['Mush\\3W_SceneDB.byml'].data)
    if exists(_archive, 'Mush\\EnemyDB_game.byml'): #==== Check if file exists ====#
        info['EnemyDB_game_new_info'] = oead.byml.from_binary(_archive['Mush\\EnemyDB_game.byml'].data)
    if exists(_archive, 'Mush\\EditDB_common.byml'): #==== Check if file exists ====#
        info['EditDB_common_new_info'] = oead.byml.from_binary(_archive['Mush\\EditDB_common.byml'].data)

    #==== M1 ====#
    for _M1_Replacement_ in _M1_Replacements_:
        info['M1_new_info'][_M1_Replacement_[0]] = _M1_Replacement_[1]

    #==== M3 ====#
    for _M3_Replacement_ in _M3_Replacements_:
        info['M3_new_info'][_M3_Replacement_[0]] = _M3_Replacement_[1]

    #==== MW ====#
    for _MW_Replacement_ in _MW_Replacements_:
        info['MW_new_info'][_MW_Replacement_[0]] = _MW_Replacement_[1]

    #==== WU ====#
    for _WU_Replacement_ in _WU_Replacements_:
        info['WU_new_info'][_WU_Replacement_[0]] = _WU_Replacement_[1]

    #==== 3W ====#
    for _3W_Replacement_ in _3W_Replacements_:
        print()
        info['3W_new_info'][_3W_Replacement_[0]] = _3W_Replacement_[1]

    #==== EnemyDB_game ====#
    for _EnemyDB_game_Replacement_ in _EnemyDB_game_Replacements_:
        print()
        info['EnemyDB_game_new_info'][_EnemyDB_game_Replacement_[0]] = _EnemyDB_game_Replacement_[1]

    #==== EditDB_common ====#
    for _EditDB_common_Replacement_ in _EditDB_common_Replacements_:
        print()
        info['EditDB_common_new_info'][_EditDB_common_Replacement_[0]] = _EditDB_common_Replacement_[1]

    yaml_util.add_constructors(yaml.CLoader)

    #==== M1 ====#
    _M1_text_ = oead.byml.to_text(info['M1_new_info'])
    _M1_text_ = yaml.load(_M1_text_, Loader=yaml.CLoader)
    _M1_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_M1_text_).write(_M1_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== M3 ====#
    _M3_text_ = oead.byml.to_text(info['M3_new_info'])
    _M3_text_ = yaml.load(_M3_text_, Loader=yaml.CLoader)
    _M3_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_M3_text_).write(_M3_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== MW ====#
    _MW_text_ = oead.byml.to_text(info['MW_new_info'])
    _MW_text_ = yaml.load(_MW_text_, Loader=yaml.CLoader)
    _MW_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_MW_text_).write(_MW_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== WU ====#
    _WU_text_ = oead.byml.to_text(info['WU_new_info'])
    _WU_text_ = yaml.load(_WU_text_, Loader=yaml.CLoader)
    _WU_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_WU_text_).write(_WU_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== 3W ====#
    _3W_text_ = oead.byml.to_text(info['3W_new_info'])
    _3W_text_ = yaml.load(_3W_text_, Loader=yaml.CLoader)
    _3W_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_3W_text_).write(_3W_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== EnemyDB_game ====#
    _EnemyDB_game_text_ = oead.byml.to_text(info['EnemyDB_game_new_info'])
    _EnemyDB_game_text_ = yaml.load(_EnemyDB_game_text_, Loader=yaml.CLoader)
    _EnemyDB_game_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_EnemyDB_game_text_).write(_EnemyDB_game_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    #==== EditDB_common ====#
    _EditDB_common_text_ = oead.byml.to_text(info['EditDB_common_new_info'])
    _EditDB_common_text_ = yaml.load(_EditDB_common_text_, Loader=yaml.CLoader)
    _EditDB_common_buf_ = io.BytesIO() #==== Create _io.BytesIO object ====#
    byml.Writer(_EditDB_common_text_).write(_EditDB_common_buf_) #==== Convert to byml and write to _io.BytesIO object ====#

    _archive['Mush/M1_SceneDB.byml'].data = (_M1_buf_.getbuffer()) #==== M1 ====#
    _archive['Mush/M3_SceneDB.byml'].data = (_M3_buf_.getbuffer()) #==== M3 ====#
    _archive['Mush/MW_SceneDB.byml'].data = (_MW_buf_.getbuffer()) #==== MW ====#
    _archive['Mush/WU_SceneDB.byml'].data = (_WU_buf_.getbuffer()) #==== WU ====#
    _archive['Mush/3W_SceneDB.byml'].data = (_3W_buf_.getbuffer()) #==== 3W ====#
    _archive['Mush/EnemyDB_game.byml'].data = (_EnemyDB_game_buf_.getbuffer()) #==== EnemyDB_game ====#
    _archive['Mush/EditDB_common.byml'].data = (_EditDB_common_buf_.getbuffer()) #==== EditDB_common ====#

    open(SuperMarioMaker2ModMergerOutput+path[len(SuperMarioMaker2Mod):]+'\\Static.pack', 'wb').write(_archive.save()[0]) #==== Save to file ====#

    print('All Super Mario Maker 2 Mods Successfully Merged...') #==== Let user know that the script has finished merging their mods ====#

if __name__ == '__main__': merge() #==== Call merge function ====#
