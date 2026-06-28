# Compiler source code for the Kuliuka Programming Language
## About
This was an experimental project, following a YouTube tutorial series found [here](https://youtube.com/playlist?list=PLCJHRjnsxJFoK8e-RaNZUa7R4BaPqczHX) to create a programming language using Python and LLVMlite.  
The grammar, syntax, and name of this project was inspired by another project of mine, where I created [a constructed language (conlang) named Liang](https://super-mctea.github.io/liang-lookup/). The name of the programming language, Kuliuka, is a word in Liang which approximately translates to "writer", and the other language keywords are also taken directly from Liang.  

The compiler itself is very barebones, and is *just* functional enough to work on my machine, so the project itself will remain in alpha until I can verify it works elsewhere; that being said, this project mainly served as a chance at upskilling and trying something different to what I'm used to making.

## How To Use:
**Currently only works on Windows**, and even that is up for debate.  
You can compile and run Kuliuka code programs using the `kuliuka.exe` file under Releases, by `cd`ing into the same folder that the exe is located in, and running:
```bash
./kuliuka.exe /path/to/your/file.klk
```
in the command line.  
Adding `--debug` to the end of that prints out two debug lines, which time how long the Parser and the Compiler take to complete, respectively.

You could add the exe to your PATH as well, which does work as far as I can tell.

## Links
- The Complete Liang dictionary site: https://super-mctea.github.io/liang-lookup/
- Kuliuka syntax highlighting for VSCode: [To Be Completed]
