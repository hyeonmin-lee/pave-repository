import json

url_dict = {}
path_dict = {}
info_dict = {}

def parse_url():
    global url_dict 

    seen = False
    with open("name_url.txt", "r") as f:
        for line in f:
            l = line.strip().split(", ")
            name = l[0]
            url = l[1]

            if name == "gdb_i686_linux.tgz":
                if "6d01cc5aef9f2dbc90f5ff615088809d05beee9e" in url:
                    name += "-first"
                elif "a9a003c04d06a2ee9f3fbb6223ee31510543bb72" in url:
                    name += "-second"
                else:
                    print("gdb_i686_linux.tgz - wrong")
                    print(l)
                    input()
            if name == "binutils_x86_64_linux.tgz":
                if "21fb83960ec07f8fa35cfb810ff690a2682b4ffa" in url:
                    name += "-first"
                elif "678bfa572286e60b258503dff5933b210c18c01f":
                    name += "-second"
                else:
                    print("binutils_x86_64_linux.tgz - wrong")
                    print(l)
                    input()
            if name == "binutils_x86_x86_64_linux.tgz":
                if "42a61cb3e6f326d7bfb5fd12980fc8cf1419cfd5" in url:
                    name += "-first"
                elif "0fcc27e76ec31a8e346ec5edb1e1b1fe84f44ff9":
                    name += "-second"
                else:
                    print("binutils_x86_x86_64_linux.tgz - wrong")
                    print(l)
                    input()
 

            if name.split(".")[0] not in url:
                print("not match", l)
                input()

            if name in url_dict:
                print("duplicate:", l)
                print(url_dict[name])
                input()

            url_dict[name] = url

def parse_extract_path():
    global path_dict

    with open("extract_path.txt", "r") as f:
        lines = f.read().strip().split("\n")

        for idx, line in enumerate(lines):
            l = line.strip()
            if idx % 2 == 0:
                if not l.startswith("INFO: "):
                    print(idx, l)
                    input()
                l = l.split(" ")
                if len(l) != 4:
                    print(idx, l)
                    input()
                name = l[2]

            else:
                if not l.startswith("## extract_to"):
                    print(idx, l)
                    input()
                l = l.split(" ")
                if len(l) != 4:
                    print(l)
                    input()
                path = l[2]
                path = path.replace("/home/hmlee/test/", "")

                if name == "gdb_i686_linux.tgz":
                    if "nacl_x86_glibc" in path:
                        name += "-first"
                    elif "nacl_x86_newlib" in path:
                        name += "-second"
                    else:
                        print("gdb_i686_linux.tgz - wrong")
                        print(l)
                        input()
                if name == "binutils_x86_64_linux.tgz":
                    if "pnacl_newlib" in path:
                        name += "-first"
                    elif "saigo_newlib" in path:
                        name += "-second"
                    else:
                        print("binutils_x86_64_linux.tgz - wrong")
                        print(l)
                        input()
                if name == "binutils_x86_x86_64_linux.tgz":
                    if "pnacl_newlib" in path:
                        name += "-first"
                    elif "saigo_newlib" in path:
                        name += "-second"
                    else:
                        print("binutils_x86_x86_64_linux.tgz - wrong")
                        print(l)
                        input()



                if name in path_dict:
                    path_dict[name].append(path)
                else:
                    path_dict[name] = [path]


def write_output(data):
    with open("files.json", "w") as f:
        json.dump(data, f, indent=4)

def get_format(name, url, path):
    return {"name": name, "format": name.split(".")[-1], "url": url, "install_path": path}


def gen_output():

    output = []
    url_keys = url_dict.keys()
    path_keys = path_dict.keys()

    if set(url_keys) != set(path_keys):
        print(set(url_keys) - set(path_keys))
        print(set(path_keys) - set(url_keys))

    for name in url_keys:
        curr_format = None
        if name.endswith("-first") or name.endswith("-second"):
            new_name = name.split("-")
            new_name = "-".join(new_name[:-1])
            curr_format = get_format(new_name, url_dict[name], path_dict[name])
        else:
            curr_format = get_format(name, url_dict[name], path_dict[name])
        output.append(curr_format)

        #print(name)
        #print(url_dict[name])
        #print(path_dict[name])
        #input()

    write_output(output)


if __name__ == "__main__":
    parse_url()
    parse_extract_path()

    gen_output()
