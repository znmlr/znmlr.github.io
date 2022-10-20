---
title: "02 Interfacing VPI Applications to Verilog Simulators"
date: 2022-10-16T17:20:04+08:00
draft: false
weight: 2
---

>  This chapter defines the terminology used by the Verilog PLI and how PLI applications which use the VPI library are interfaced to Verilog simulators. 
>
> All remaining chapters in Part One of this book assume the principles covered in this chapter are understood. The general concepts presented are:  
>
> - PLI terms as used with the VPI library  
> - System tasks and system functions
> - How VPI routines work  
> - A complete PLI application example  
> - Interfacing PLI applications to Verilog simulators

## General PLI terms as used in this book

- **`C program`**: A complete software program written in the C or C++ programming language. A `C program` must include a C *`main`* function.

- **`C function`**: A function written in the C or C++ programming language. A `C function` does not include a C *`main`* function.
- **`Verilog function`**: A Verilog HDL function, written in the Verilog Hardware Description Language. Verilog functions can only be called from Verilog source code.
- **`User-defined system task or system function`**: A user-defined system task or system function is a construct that is used in Verilog HDL source code. The name of a user-defined system task or system function must begin with a dollar sign ( **`$`** ), and it is used in the Verilog language in the same way as a Verilog HDL standard system task or system function. When simulation encounters the user-defined system task or system function, the simulator will execute a *PLI routine* associated with the system task/function.
- **`PLI application`**: A *user-defined system task or system function* with an associated set of one or more *`PLI`* routines.
- **`PLI routine`**: A `C function` which is part of a *PLI application.* The PLI routine is executed by the simulator when simulation encounters a user-defined system task or system function. The VPI portion of the PLI standard defines several PLI routine types: **`calltf routines`**, **`compiletf routines`**, **`sizetf routines`** and **`simulation callback routines`.** These terms are defined in more detail later in this chapter.
- **`PLI library`**: A library of `C functions` which are defined in the Verilog PLI standard. PLI library functions are called from *`PLI routines`,* and enable the *`PLI routines`* to interact with a Verilog simulation. The IEEE 1364 standard provides three PLI libraries, referred to as the **`VPI library`,** the **`TF library`** and the **`ACC library`**.
- **`VPI routines`**, **`TF routines`** and **`ACC routines`**: `C functions` contained in the *`PLI library`.* The term *`routine`* is used for these functions, to avoid confusion with *Verilog functions* and *C functions.*

## *System tasks and system functions*

- The Verilog Hardware Description Language provides constructs called **“system tasks”** and **“system functions”.** A system task or system function is not a hardware modeling construct. It is a command that is executed by a Verilog simulator.
- The names of system tasks and system functions always begin with a dollar sign (**$**).
- A **system task** is analogous to a subroutine. When the task is called, the simulator branches to a program that executes the functionality of the task. When the task has completed, the simulation returns to the next statement following the task call. 
- A **system function** returns a value. When the function is called, a simulator executes the program associated with the function, which returns a value into the simulation. The return value becomes part of the statement that called the function. 

### **Built-in system tasks and system functions**

### **User-defined system tasks and system functions**

- The Verilog PLI provides a means for Verilog users to add additional system tasks and system functions. 

- When simulation encounters a user-defined system task or system function, the simulator branches to a user-supplied C function, executes that function, and then returns back to executing the Verilog source at the point where the system task/function was called.
- User-defined system task and system function names must begin with a dollar sign (**$**), and may only use the characters that are legal in Verilog names, which are: a—z A—Z 1—9 _ $

### **Overriding built-in system tasks and system functions**

- A user-defined system task or system function can be given the same name as a system task/function that is built into the simulator. 
- This allows a PLI application developer to override the operation of a built-in system task/function with new functionality. 

### **System tasks are used as procedural programming statements**

- System tasks are procedural programming statements in the Verilog HDL.
- This means a system task may only be called from a Verilog **initial** procedure, an **always** procedure, a Verilog HDL **task** or a Verilog HDL **function.** 
- A system task may not be called outside of a procedure, such as from a continuous assignment statement.

### **System functions are used as expressions**

- System functions are expressions in the Verilog HDL. 
- This means a system function may be called anywhere a logic value may be used. 
- System functions may be called from a Verilog **initial** procedure, an **always** procedure, a Verilog HDL **task,** a Verilog HDL **function,** an **assign** continuous assignment statement, or as an operand in a compound expression.

### **System task/function arguments**

- A system task or system function may have any number of arguments, including none. 
- The user-supplied PLI application can read the values of the arguments of a system task/function. 
- If the argument is a Verilog reg or variable (integer, real and time), then the PLI application can also write values into the task/function argument.

  ![image-20221016204222630](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221016204222630.png)

## *Instantiated Verilog designs*

- In a Verilog HDL module, a reference to another module is referred to as a **module instance.** In the following Verilog source code, module **top** contains two *instances* of module **bottom.**

```systemverilog
module top;
    reg [7:0] in1 ;
    wire [7:0] out1;
    bottom b1 (in1[7:4], out1[7:4]);
    bottom b2 (in2[3:0], out2[3:0]);
endmodule

module bottom (in, out);
    ...
endmodule
```

### **Multiple instances of a system task or system function**

```systemverilog
module top;
	...
	middle m1 (...);				//module instance
	middle m2 (...);				//module instance
	
    initial
		$my_app_1(in1, out1);		//system task instance
    
	always @(posedge clock)
		$my_app_1(in2, out2);		//system task instance
endmodule

module middle (...);
    ...
    bottom b1 (...);				//module instance
    bottom b2 (...);				//module instance
endmodule

module bottom (...);
    ...
	initial
		$my_app_2(in3, out3);		//system task instance

    always @(posedge clock)
		$my_app_2(in4, out4);		//system task instance
endmodule
```

In the preceding example, four different conditions are shown that can exist in a Verilog simulation.

- A single instance of a system task that is invoked one time.

>  In module **top**, the first *instance* of *$my_app_1* is in a Verilog initial procedure, which will be called once at the beginning of a simulation.

- A single instance of a system task that is invoked many times

> In module **top**, the second *instance* of *$my_app_1* is in a Verilog always procedure, which will be called every positive edge of the clock signal.

- Multiple instances of a system task that are each invoked one time

> In module **bottom**, the first *instance* of *$my_app_2* is in a Verilog initial procedure, which will be called once at the beginning of a simulation.

- Multiple instances of a system task that are each invoked many times

> In module **bottom**, the second *instance* of *$my_app_2* is in a Verilog always procedure, which will be called every positive edge of the clock signal.

Each of these system task instances will have unique logic values for the inputs and outputs. 

One of the requirements of a PLI application is to allow for multiple unique instances of the application. 

## *How PLI applications work*

  ![image-20221017231903413](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221017231903413.png)

### **The types of PLI routines**

- The VPI portion of PLI standard defines several types of PLI routines which can be associated with a system task or system function. 
- The type of the routine determines **when** the simulator will execute the routine. 
- Some types of routines are run-time routines, which are invoked during simulation, and some types are elaboration or linking time routines, which are invoked prior to simulation. 
- The types of PLI routines are:

> - **calltf routines**
>
> - **compiletf routines**
>
> - **sizetf routines**
>
> - **simulation callback routines**

### **Associating routine types with system task/functions**

- *calltf routine*
- *compiletf routine*
- *sizetf routine*
- *simulation callback routine*

### **Special PLI data types for portability**

- The VPI library defines several fixed-width data types, which are used by the routines in the VPI library.

   ![image-20221020221612159](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221020221612159.png)

## *calltf routines*

- The **calltf routine** is executed when simulation is running. For the *$pow* example that follows, at every positive edge of clock the *calltf routine* associated with *$pow* will be executed by the simulator. 

  ![image-20221020221848452](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221020221848452.png)

## *compiletf routines*

- The **compiletf routine** is called by the simulator before simulation starts running—in other words, before simulation time 0. 

- The routine may be called by the simulator’s compiler or elaborator, when the simulator loads and prepares its simulation data structure. The purpose of *compiletf routine* is to verify that a system task/function is being used correctly.

  ![image-20221020222125689](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221020222125689.png)

- Use a *compiletf routine* to improve the performance of PLI programs. Since this routine is only called one time prior to simulation time 0, the code to check the correctness of arguments is only executed once. The *calltf routine,* which may be invoked millions of times during a simulation, does not need to repeat the syntax checking, and therefore can execute more efficiently.
- The *compiletf routine* will be called one time for each instance of a user-defined system task/function. If a design used the *$pow* user-defined system function in three different places, the *compiletf routine* for *$pow* would be called three times. If a simulator allows system tasks and system functions to be invoked from the simulator’s debug command line, then the *compiletf routine* will be called prior to execution of the *calltf routine* for each interactive usage.

### **Limitations on compiletf callbacks**

- **The compiletf routine should only be used for syntax checking!** 

- To ensure that a PLI application will be portable, only the following activities should be performed in a *compiletf routine:*

> - Accessing the arguments of an instance of a system task/function. 
> - Using VPI routines such as `vpi_printf()`, which do not access objects in simulation. 
> - Registering *simulation callback routines* using `vpi_register_cb()` for the end of elaboration/linking or the start of simulation. 

## *sizetf routines*

- The **sizetf routine** is only used with system functions that are registered with the `sys-functype` as **vpiSizedFunc** or **vpiSizedSignedFunc**. These types indicate that the system function returns scalar or vector values.

-  Because these function types return a user-specified number of bits, the simulator compiler or elaborator may need to know how many bits to expect from the return, in order to correctly compile the statement from which the system function is called. 

- A *sizetf routine* is called one time, before simulation time 0. The *sizetf routine* returns to the simulator how many bits wide the return value of system function will be.

- In the *$pow* example, the *calltf routine* will return a 32-bit value. Therefore, the *sizetf* *routine* associated with *$pow* needs to return a value of 32 to the simulator.

  ![image-20221020223232114](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221020223232114.png)

### **Limitations on sizetf callbacks**

- The intent of the *sizetf routine* is to notify the simulator compiler or elaborator of the return size for system functions. 
- The simulator may invoke the *sizetf routine* very early in the elaboration/linking phase of a Verilog design, and, at this early stage, the Verilog hierarchy may not have been generated. 
- In addition, the *sizetf routine* is only called one time for a system function name, and the return size applied to all instances of the system function. 
- For these reasons, only standard C language statements and functions should be used in a *sizetf routine.* 
- An error may result if any VPI routines are called from a *sizetf routine.* Any memory or static variables allocated by a *sizetf* *routine* may not remain in effect for when simulation starts running.

## *VPI Simulation callback routines*

- The VPI provides a means for PLI applications to be called for specific simulation events. 
- The VPI portion of the PLI standard refers to these types of routines as **simulation callback routines.** 
- Some examples of simulation related callbacks are:

> - The beginning of Verilog simulation (just before the start of simulation time 0).
> - Entering debug mode (such as when the *$stop* built-in system task is executed).
> - End of simulation (such as when the *$finish* built-in system task is executed).
> - Change of value of a signal.
> - Execution of a Verilog procedural statement.

- A common usage of *simulation callback routines* is to perform tasks at the very beginning and the very end of a simulation. For example, a PLI application to read test vectors might need to open a test vector file at the start of simulation, and close the file at the end of simulation.

  ![image-20221020225734916](http://nas.znmlr.cn:15900/markdown/2022/10/image-20221020225734916.png)

## *PLI routine inputs and outputs*

- All types of PLI routines are C functions, and a Verilog simulator will utilize the inputs and return values of the functions when the simulator calls the functions. 
- The input that is passed to the *compiletf routine, calltf routine* and *sizetf routine* is a pointer, which points to the user_data value that was specified when the system task/function was registered. 
- The *compiletf routine, calltf routine, sizetf routine* and *simulation callback routine* are expected to be integer functions in the PLI standard. 
- However, the only return value which is used by the simulator is the return of the *sizetf routine,* which represents the bit-width of the system function return value. 
- The return value from the *compiletf* *routine, calltf routine* and *simulation callback routine* are not used, and are ignored by the simulator.

## *A complete system function example* — *$pow*

The following example illustrates all the parts of a complete system function, with the user-defined name of **$pow.**

- The system function will return a 32-bit value.

- The system function requires two arguments, a base value and an exponent value. Both arguments must be numeric integer values.

To implement the *$pow* functionality, four user-defined PLI routines are used:

- A **sizetf routine** to establish the return size of *$pow.*

- A VPI **compiletf routine** to verify that the *$pow* arguments are valid values.

- A **calltf routine** to calculate the base to the power of the exponent each time *$pow* is executed by the simulator.

- A VPI **simulation callback routine** to print a message when simulation firsts starts running (immediately prior to simulation time 0).
