# Greek++ Compiler

This repository contains an implementation of a compiler for **Greek++**, a small educational programming language developed as part of my **Compilers course**.  
The project includes all major phases of a typical compiler: lexical analysis, syntax analysis, semantic actions, symbol table management and generation of intermediate code.

## Contributors
- **Georgios Kefalas**
- **Dimitrios Papadopoulos**

## Project Documentation
A detailed explanation of the compiler’s architecture, implementation decisions and examples is included in:
 **`Report.pdf`**

## Test Files
The `test_files/` directory contains all the Greek++ programs used to test the compiler.  
It includes both **valid programs** that should compile successfully and **intentionally incorrect programs** designed to verify that the compiler properly handles and reports errors.


## How to Run the Compiler
python compiler.py <your_program>.gr --debug

## Output Files
For each input `.gr` file, the compiler generates **three output files**:
<your_program>.int: Intermediate code (quadruples)
<your_program>.sym: Symbol table dump
<your_program>.asm: Final **RISC-V assembly** code
