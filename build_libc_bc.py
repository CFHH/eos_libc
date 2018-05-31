# coding=utf-8
import os
import shutil
import wast_builder


base_path = os.path.abspath(os.curdir)
# print(base_path)


'''
需要编译的源文件
file(GLOB CRYPT_SOURCES  "upstream/src/crypt/*.c")
file(GLOB CTYPE_SOURCES  "upstream/src/ctype/*.c")
file(GLOB ENV_SOURCES  "upstream/src/env/*.c")
file(GLOB ERRNO_SOURCES  "upstream/src/errno/*.c")
file(GLOB EXIT_SOURCES  "upstream/src/exit/*.c")
file(GLOB LOCALE_SOURCES "upstream/src/locale/*.c")
file(GLOB MATH_SOURCES  "upstream/src/math/*.c")
file(GLOB MBYTE_SOURCES  "upstream/src/multibyte/*.c")
file(GLOB MISC_SOURCES "upstream/src/misc/*.c")
file(GLOB SEARCH_SOURCES "upstream/src/search/*.c")
file(GLOB STDIO_SOURCES "upstream/src/stdio/*.c")
file(GLOB STDLIB_SOURCES "upstream/src/stdlib/*.c")
file(GLOB STRING_SOURCES "upstream/src/string/*.c")
file(GLOB TIME_SOURCES "upstream/src/time/*.c")
file(GLOB THREAD_SOURCES "upstream/src/thread/*.c")
set(INTERNAL_SOURCES upstream/src/internal/floatscan.c
                     upstream/src/internal/intscan.c
                     upstream/src/internal/shgetc.c
                     upstream/src/internal/libc.c)
'''
source_folders = []
source_folders.append(os.path.join(base_path, r"src\crypt"))
source_folders.append(os.path.join(base_path, r"src\ctype"))
source_folders.append(os.path.join(base_path, r"src\env"))
source_folders.append(os.path.join(base_path, r"src\errno"))
source_folders.append(os.path.join(base_path, r"src\exit"))
source_folders.append(os.path.join(base_path, r"src\locale"))
source_folders.append(os.path.join(base_path, r"src\math"))
source_folders.append(os.path.join(base_path, r"src\misc"))
source_folders.append(os.path.join(base_path, r"src\multibyte"))
source_folders.append(os.path.join(base_path, r"src\search"))
source_folders.append(os.path.join(base_path, r"src\stdio"))
source_folders.append(os.path.join(base_path, r"src\stdlib"))
source_folders.append(os.path.join(base_path, r"src\string"))
source_folders.append(os.path.join(base_path, r"src\thread"))
source_folders.append(os.path.join(base_path, r"src\time"))
source_files = []
'''不需要遍历子目录
for folder in source_folders:
    c = os.walk(folder)
    for root, dirs, files in c:
        for file_name in files:
            source_files.append(os.path.join(root, file_name))
'''
for folder in source_folders:
    files = os.listdir(folder)
    for file in files:
        if os.path.splitext(file)[1] == '.c':
            source_files.append(os.path.join(folder, file))

source_files.append(os.path.join(base_path, r'src\internal\floatscan.c'))
source_files.append(os.path.join(base_path, r'src\internal\intscan.c'))
source_files.append(os.path.join(base_path, r'src\internal\shgetc.c'))
source_files.append(os.path.join(base_path, r'src\internal\libc.c'))


'''
需要包含的头文件目录
INCLUDE_FOLDERS ${CMAKE_SOURCE_DIR}/contracts/musl/upstream/include
                  ${CMAKE_SOURCE_DIR}/contracts/musl/upstream/src/internal
                  ${CMAKE_SOURCE_DIR}/contracts/musl/upstream/arch/eos
                  ${CMAKE_SOURCE_DIR}/contracts/
'''
include_foders = []
include_foders.append(os.path.join(base_path, r"include"))
include_foders.append(os.path.join(base_path, r"src\internal"))
include_foders.append(os.path.join(base_path, r"arch\wasm"))
system_include_foders = []
system_include_foders.append(os.path.join(base_path, r"include"))


'''
输出文件夹
'''
destination_foder = os.path.join(base_path, r"build_bc")
if os.path.exists(destination_foder):
    '''
    shutil.rmtree(destination_foder)  # 删除后不能立即创建
    os.mkdir(destination_foder)
    '''
    '''
    files = os.listdir(destination_foder)
    for file in files:
        pathname = os.path.join(destination_foder, file)
        if os.path.isdir(pathname):
            shutil.rmtree(pathname)
        else:
            os.remove(pathname)
    '''
else:
    os.mkdir(destination_foder)


wast_builder.compile_wast(source_files, include_foders, destination_foder, 'libc.bc', system_include_foders)
