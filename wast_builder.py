# coding=utf-8
import os
import subprocess
import time


def callcmd(args):
    # subprocess.call(args)
    p = subprocess.Popen(args)
    returncode = p.wait()
    if returncode != 0:
        print('ERROR: \"', args, '\" return ', returncode)
    return returncode


def compile_wast(source_files, include_foders, destination_foder, output_name, system_include_foders=[], nowarnings=True):
    '''打印信息
    print('source_files:')
    for file in source_files:
        print('   ', file)
    print('include_foders:')
    for folder in include_foders:
        print('   ', folder)
    print('destination_foder:', destination_foder)
    print('output_name:', output_name)
    '''
    compile_cmd_common = 'clang -emit-llvm -Oz --target=wasm32 -ffreestanding -nostdlib -nostdlibinc -fno-threadsafe-statics -fno-rtti -fno-exceptions'
    if nowarnings:
        compile_cmd_common = compile_cmd_common + ' -Wno-everything'
    else:
        compile_cmd_common = compile_cmd_common + ' -Weverything -Wno-c++98-compat -Wno-old-style-cast -Wno-vla -Wno-vla-extension -Wno-c++98-compat-pedantic -Wno-missing-prototypes -Wno-missing-variable-declarations -Wno-packed -Wno-padded -Wno-c99-extensions -Wno-documentation-unknown-command'
    for folder in include_foders:
        compile_cmd_common = compile_cmd_common + " -I " + folder
    for folder in system_include_foders:
        compile_cmd_common = compile_cmd_common + " -isystem " + folder
    link_cmd = 'llvm-link -o ' + os.path.join(destination_foder, output_name)

    cnt = len(source_files)
    i = 0
    for file in source_files:
        i = i + 1
        print('Compiling file [', i, '/', cnt, ']: ', file, ' ......')
        time.sleep(0)
        clang_cmd = compile_cmd_common
        st = os.path.splitext(file)
        t = os.path.split(st[0])
        name = t[1]
        ext = st[1]
        bcfile = os.path.join(destination_foder, name + '.ll')
        link_cmd = link_cmd + ' ' + bcfile
        if os.path.exists(bcfile):
            time1 = os.path.getmtime(file)
            time2 = os.path.getmtime(bcfile)
            if time2 > time1:
                continue
        if ext == '.c':
            clang_cmd = clang_cmd + ' -D_XOPEN_SOURCE=700'
        else:
            clang_cmd = clang_cmd + ' --std=c++14'
        clang_cmd = clang_cmd + ' -c ' + file + ' -o ' + bcfile
        returncode = callcmd(clang_cmd)
        if returncode != 0:
            return returncode

    print('Linking ', output_name, ' ......')
    returncode = callcmd(link_cmd)
    if returncode != 0:
        return returncode

    print('COMPLETE！')
    return 0

