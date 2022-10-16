---
title: "01 Creating PLI Applications Using VPI Routines"
date: 2022-10-14T21:01:50+08:00
draft: false
weight: 1
---

## The capabilities of the Verilog PLI

- C language bus-functional models
- Access to programming language libraries
- Reading test vector files
- Delay calculation
- Custom output displays
- Co-simulation
- Design debug utilities
- Simulation analysis

## The general steps to create a PLI application

- Define a **`system task`** or **`system function`** name for the application.
- Write a C language **`calltf routine`** which will be executed by the simulator when ever simulation encounters the system task name or the system function name.

> Optionally, additional C language routines can be written which will be executed by the simulator for special conditions, such as when the simulator compiler or elaborator encounters the system task/function name.

- **`Register`** the system task or system function name and the associated C language routines with the Verilog simulator. This registration tells the simulator about the new system task or system function name, and the name of the *`calltf routine`* associated with that task or system function (along with any other routines).

- **`Compile`** the C source files which contain the PLI application routines, and **`link`** the object files into the Verilog simulator.

## User-defined system tasks and system functions

The IEEE 1364 Verilog standard allows system tasks and system functions to be defined in three ways:

- A standard set of built-in system tasks and system functions.
- Simulator specific system tasks and system functions.
- User-defined system tasks and system functions.

## The $hello PLI application example

### Step One: defining a $hello system task

```systemverilog
module test;
	initial
		$hello();
endmodule
```

### Step Two: writing a calltf routine for $hello

```c
#include <stdlib.h>
#include <stdio.h>
#include “vpi_user.h”
/* ANSI C standard library 				*/
/* ANSI C standard input/output library */
/* IEEE 1364 PLI VPI routine library 	*/
PLI_INT32 PLIbook_hello_calltf(PLI_BYTE8 *user_data)
{
	vpi_printf(“\nHello World!\n\n”);
	return(0);
}
```

### Step Three: Registering the $hello system task

- Create a *`register function`* which specifies the PLI application information in an `s_vpi_register_systf` structure and calls the `vpi_register_systf ()` VPI routine.

- List the name of the register function in a C array called *`vlog_startup_routines`.*

```c
void PLIbook_hello_register()
{
	s_vpi_systf_data tf_data;
	tf_data.type		= vpiSysTask;
	tf_data.sysfunctype	= 0;
	tf_data.tfname		= "$hello";
	tf_data.calltf		= PLIbook_hello_calltf;
	tf_data.compiletf	= NULL;
	tf_data.sizetf		= NULL;
	tf_data.user_data	= NULL;
	vpi_register_systf(&tf_data) ;
}
```

### Step Four: Compiling and linking the $hello system task

The final step in creating a new PLI application is to compile the C source code containing the application and linking the compiled files to the Verilog simulator. Once the application has been linked to the simulator, the simulator can invoke the calltf routine when simulation executes the $hello system task name.  

### Running simulations with the $hello system task

Once a PLI application has been registered with a Verilog simulator, the new system task or system function can be used in a Verilog model, just as with built-in system tasks and system functions.  

```systemverilog
module test;
    initial
        begin
            $hello();
            #10 $stop;
            $finish;
        end
endmodule
```

## The $show_value PLI application example

- The system task $show_value illustrates using the PLI to allow a C routine to read current logic values within a Verilog simulation.   
- The $show_value system task requires one argument, which is the name of a net or reg in the Verilog design.  

```systemverilog
module test;
	reg a, b, ci;
	wire ... sum, co;
	. . .
	initial
    begin ...
    	$show_value(sum);
    end
endmodule
```

- Two user-defined C routines will be associated with $show_value:  

> - A C routine to verify that $show_value has the correct type of argument.  
> - A C routine to print the name and logic value of the signal  

### Writing a compiletf routine for $show_value  

The PLI allows users to provide a C routine to verify that a system task or system function is being used correctly and has the correct types of arguments. This C routine is referred to as a compiletf routine.  

```c
PLI_INT32 PLIbook_ShowVal_compiletf(PLI_BYTE8 *user_data)
{
    vpiHandle systf_handle, arg_iterator, arg_handle;
    PLI_INT32 arg_type;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    if (systf_handle == NULL) {
        vpi_printf("ERROR: $show_value failed to obtain systf handle\n");
        vpi_control(vpiFinish,0); /* abort simulation */
        return(0);
    }
    
    /* obtain handles to system task arguments */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    if (arg_iterator == NULL) {
        vpi_printf("ERROR: $show_value requires 1 argument\n");
        vpi_control(vpiFinish,0); /* abort simulation */
        return(0);
    }
    
    /* check the type of object in system task arguments */
    arg_handle = vpi_scan(arg_iterator);
    arg_type = vpi_get(vpiType, arg_handle);
    if (arg_type != vpiNet && arg_type != vpiReg) {
        vpi_printf("ERROR: $show_value arg must be a net or reg\n");
        vpi_free_object(arg_iterator); /* free iterator memory */
        vpi_control(vpiFinish,0); /* abort simulation */
        return(0);
    }
    
    /* check that there are no more system task arguments */
    arg_handle = vpi_scan(arg_iterator);
    if (arg_handle != NULL) {
        vpi_printf("ERROR: $show_value can only have 1 argument\n");
        vpi_free_object(arg_iterator); /* free iterator memory */
        vpi_control(vpiFinish,0); /* abort simulation */
        return(0);
    }
    
    return(0);
}
```

- `vpiHandle` is a special data type defined in the VPI library. This data type is used to store pointers to information about objects in a Verilog simulation data structure.  
- The `vpi_handle()` function returns a handle, which is a form of pointer, to a specific object in a Verilog simulation data structure. In this example, handles are  obtained for the instance of the $show_value system task which called the PLI application, and for the object listed as the first argument of the system task.  
- The `vpi_iterate()` function obtains an iterator for all of a specific type of object. An iterator is essentially a pointer to the next object in a series of objects. The iterator object is stored in a `vpiHandle` data type. In the above example, an iterator is obtained for all of the arguments to the $show_value system task.  
- The `vpi_scan()` obtains a handle for the next object that is referenced by an iterator. In the above example, each object returned by `vpi_scan()` is the next argument of the $show_value system task.  
- The `vpi_get()` function returns the value of integer properties of a specific object in the simulation data structure. The first input to this function is a constant that defines the property to be obtained. The `vpiType` property used in this example identifies the type of object passed as the argument to $show_value. In this example, the test is checking that the argument is a Verilog net or reg data type.  
- The `vpi_free_object()` function releases memory allocated by the `vpi_iterate()` routine. Refer to section 4.5.3 on page 108 in Chapter 4 for more details `onwhenvpi_free_object()` needs to be used in a PLI application.  
- The `vpi_printf()` function writes a message to the simulator’s output channel.  
- The `vpi_control()` function allows a PLI application to control certain aspects of a simulation. In this compiletf routine, this function is used to abort simulation if there is a usage error with the $show_value system task.  

### Writing the calltf routine for $show_value  

The calltf routine is the C routine which will be executed when simulation encounters the $show_value system task during simulation.  

```c
PLI_INT32 PLIbook_ShowVal_calltf(PLI_BYTE8 *user_data)
{
    vpiHandle systf_handle, arg_iterator, arg_handle, net_handle;
    s_vpi_value current_value;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handle to system task argument
    compiletf has already verified only 1 arg with correct type */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    net_handle = vpi_scan(arg_iterator);
    vpi_free_object(arg_iterator); /* free iterator memory */
    
    /* read current value */
    current_value.format = vpiBinStrVal; /* read value as a string */
    vpi_get_value(net_handle, &current_value);
    vpi_printf("Signal %s ", vpi_get_str(vpiFullName, net_handle));
    vpi_printf("has the value %s\n", current_value.value.str);
    
    return(0);
}
```

- The `vpi_get_str()` function returns the value of string properties of a specific object in the simulation data structure. The first input to this function is a constant that defines the property to be obtained. The `vpiFullName` property used in this example is the Verilog hierarchical path name of the net listed as an argument to $show_value.  
- The `vpi_get_value()` function obtains the logic value of a Verilog object. The value is returned into an `s_vpi_value` structure, which is defined as part of the VPI standard. The `vpi_get_value()` function allows the value to be obtained in a variety of formats. In this example, the value is obtained as a string, with a binary representation of the value.  

### Registering the $show_value PLI application  

The register function is used to inform the Verilog simulator about the PLI application. The information about the application is specified in a `s_vpi_register_systf` structure.  

```c
void PLIbook_ShowVal_register()
{
    s_vpi_systf_data tf_data;
    tf_data.type = vpiSysTask;
    tf_data.sysfunctype = 0;
    tf_data.tfname = "$show_value";
    tf_data.calltf = PLIbook_ShowVal_calltf;
    tf_data.compiletf = PLIbook_ShowVal_compiletf;
    tf_data.sizetf = NULL;
    tf_data.user_data = NULL;
    vpi_register_systf(&tf_data);
    return;
}
```

### A test case for $show_value  

The following Verilog HDL source code is a small test case for the $show_value application.  

```systemverilog
`timescale 1ns / 1ns
module test;
    reg a, b, ci, clk;
    wire sum, co;
    addbit i1 (a, b, ci, sum, co);
    initial
        begin
            clk = 0;
            a = 0;
            b = 0;
            ci = 0;
            #10 a = 1;
            #10 b = 1;
            $show_value(sum);
            $show_value(co);
            $show_value(i1.n3);
            #10 $stop;
            $finish;
    	end
endmodule
```

```systemverilog
/*** A gate level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co);
    input a, b, ci;
    output sum, co;
    wire a, b, ci, sum, co, n1, n2, n3;
    xor (n1, a, b);
    xor #2 (sum, n1, ci);
    and (n2, a, b) ;
    and (n3, n1, ci);
    or #2 (co, n2, n3);
endmodule
```

