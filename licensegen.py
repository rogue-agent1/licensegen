#!/usr/bin/env python3
"""licensegen - Generate LICENSE files for open source projects. Zero deps."""
import sys, os, time

YEAR = time.strftime("%Y")

LICENSES = {
"mit": f"""MIT License

Copyright (c) {YEAR} [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",

"apache": f"""                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   Copyright {YEAR} [fullname]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.""",

"gpl3": f"""                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) {YEAR} [fullname]

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.""",

"bsd2": f"""BSD 2-Clause License

Copyright (c) {YEAR}, [fullname]

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""",

"unlicense": """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>""",

"isc": f"""ISC License

Copyright (c) {YEAR} [fullname]

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.""",
}

def cmd_generate(args):
    if not args:
        print("Usage: licensegen generate <type> [--name 'Your Name']")
        print(f"Types: {', '.join(sorted(LICENSES))}")
        sys.exit(0)
    
    license_type = args[0].lower()
    name = "Your Name"
    for i, a in enumerate(args):
        if a == "--name" and i+1 < len(args): name = args[i+1]
    
    if license_type not in LICENSES:
        print(f"❌ Unknown: {license_type}. Available: {', '.join(sorted(LICENSES))}"); sys.exit(1)
    
    text = LICENSES[license_type].replace("[fullname]", name)
    
    if "--stdout" in args:
        print(text)
    else:
        if os.path.exists("LICENSE") and "--force" not in args:
            print("⚠️ LICENSE exists. Use --force to overwrite."); sys.exit(1)
        with open("LICENSE", "w") as f: f.write(text + "\n")
        print(f"✅ Generated LICENSE ({license_type.upper()}) for {name}")

def cmd_list(args):
    descs = {"mit":"Permissive, simple","apache":"Permissive + patent grant",
             "gpl3":"Copyleft, share-alike","bsd2":"Permissive, minimal",
             "unlicense":"Public domain","isc":"Permissive, ISC-style"}
    for t in sorted(LICENSES):
        print(f"  • {t:12s} — {descs.get(t,'')}")

def cmd_detect(args):
    if not os.path.exists("LICENSE"):
        print("❌ No LICENSE file found"); sys.exit(1)
    with open("LICENSE") as f: content = f.read(500).lower()
    if "mit license" in content: print("📄 MIT License")
    elif "apache" in content: print("📄 Apache License 2.0")
    elif "gnu general public" in content: print("📄 GPL")
    elif "bsd" in content: print("📄 BSD License")
    elif "unlicense" in content: print("📄 Unlicense")
    elif "isc" in content: print("📄 ISC License")
    else: print("📄 Unknown license type")

CMDS = {"generate":cmd_generate,"gen":cmd_generate,"list":cmd_list,"ls":cmd_list,"detect":cmd_detect}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("licensegen - Generate LICENSE files")
        print("Commands: generate <type> [--name N], list, detect")
        sys.exit(0)
    cmd = args[0]
    if cmd not in CMDS: print(f"Unknown: {cmd}"); sys.exit(1)
    CMDS[cmd](args[1:])
