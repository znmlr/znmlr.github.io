---
title: "03 How to Use the VPI"
date: 2022-10-25T17:41:45+08:00
draft: false
weight: 3
---

## *Specification of `$show_all_nets` and `$show_all_signals`*

## *The VPI routine library*

- `VPI` stands for `Verilog Procedural Interface`

- The VPI routines are the third of the three generations of the Verilog PLI routines (the TF routines were the first generation, and the ACC routines were the second).
- The primary purpose of the VPI routines is to provide a PLI application access to the internal data structures of a simulation.

The VPI library can be divided into five basic groups of routines:

- A **handle** routine obtains a handle for one specific Verilog HDL object.

- An **iterate** routine and a **scan** routine obtain handles for all of a specific type of Verilog object.

- **get** routines access information about an object.

- **set** routines modify information about an object.

- A few **miscellaneous** routines perform a variety of operations

The library of VPI routines is defined in a C header file called **vpi_user.h**, which is part of the IEEE 1364 standard. This header file also defines a number of C constants and C structures used by the VPI routines. All PLI applications which use VPI routines must include the vpi_user.h file.

The VPI library is designed to work with the standard ANSI C libraries, such as **stdlib.h**, **stdio.h** and **stdarg.h.** 

## *Advantages of the VPI library*

- The VPI library is a concise set of 37 routines. These routines have a very simple and consistent syntax, and are easy to learn and use.

## *Verilog HDL objects*

- The VPI routines treat Verilog HDL constructs as **objects,** and several of the VPI routines provide ways to locate any specific object or type of object within a simulation data structure. 
- Other VPI routines can then read and modify information about each object. The simple Verilog HDL example which follows has several objects which can be accessed by the library of VPI routines.

```verilog
module test;
    reg [1:0] test_in;
    wire [1:0] test_out;
    buf2 u1 (test_in, test_out);
    initial
        begin
            test_in = 3;
            #50 $display(“in-%d, out=5d”, test_in, test_out);
        end
endmodule

module buf2 (in, out);
    input [1:0] in;
    output [1:0] out;
    wire [1:0] in, out;
    buf #5 n0 (out[0], in[0]);
    buf #7 n1 (out[1], in[1]);
endmodule
```

