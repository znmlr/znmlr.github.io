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

  ![image-20221016204222630](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221016204222630.png)

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

  ![image-20221017231903413](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221017231903413.png)

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

   ![image-20221020221612159](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221020221612159.png)

## *calltf routines*

- The **calltf routine** is executed when simulation is running. For the *$pow* example that follows, at every positive edge of clock the *calltf routine* associated with *$pow* will be executed by the simulator. 

  ![image-20221020221848452](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221020221848452.png)

## *compiletf routines*

- The **compiletf routine** is called by the simulator before simulation starts running—in other words, before simulation time 0. 

- The routine may be called by the simulator’s compiler or elaborator, when the simulator loads and prepares its simulation data structure. The purpose of *compiletf routine* is to verify that a system task/function is being used correctly.

  ![image-20221020222125689](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221020222125689.png)

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

  ![image-20221020223232114](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221020223232114.png)

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

    ![image-20221020225734916](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221020225734916.png)

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

The *compiletf routine, sizetf routine, calltf routine,* and *simulation callback routine* are C functions. These functions may be located in separate files, or they can all be in the same file. Typically, smaller PLI applications place all the routines in a single file, while larger, more complex applications might break them into multiple files.

```c
#include <stdlib.h> 	/* ANSI C standard library 				*/
#include <stdio.h> 		/* ANSI C standard input/output library */
#include <stdarg.h> 	/* ANSI C standard arguments library 	*/
#include "vpi_user.h" 	/* IEEE 1364 PLI VPI routine library 	*/

/* prototypes of PLI application routine names */
PLI_INT32 	PLIbook_PowSizetf(PLI_BYTE8 *user_data),
			PLIbook_PowCalltf(PLI_BYTE8 *user_data),
			PLIbook_PowCompiletf(PLI_BYTE8 *user_data),
			PLIbook_PowStartOfSim(s_cb_data *callback_data);
/********************************************************************/
/*	$pow Registration Data											*/
/*	(add this function name to the vlog_startup_routines array)		*/
/********************************************************************/
void PLIbook_pow_register()
{
	s_vpi_systf_data 	tf_data;
	s_cb_data 			cb_data_s;
	vpiHandle			 callback_handle;
    tf_data.type 		= vpiSysFunc;
    tf_data.sysfunctype = vpiSysFuncSized;
    tf_data.tfname 		= "$pow";
    tf_data.calltf 		= PLIbook_PowCalltf;
    tf_data.compiletf 	= PLIbook_PowCompiletf;
    tf_data.sizetf 		= PLIbook_PowSizetf;
    tf_data.user_data 	= NULL;
    vpi_register_systf(&tf_data);
    cb_data_s.reason 	= cbStartOfSimulation;
    cb_data_s.cb_rtn 	= PLIbook_PowStartOfSim;
    cb_data_s.obj 		= NULL;
    cb_data_s.time 		= NULL;
    cb_data_s.value 	= NULL;
    cb_data_s.user_data = NULL;
    callback_handle 	= vpi_register_cb(&cb_data_s);
    vpi_free_object(callback_handle); /* don’t need callback handle */
}
/********************************************************************/
/*	Sizetf application												*/
/********************************************************************/
PLI_INT32 PLIbook_PowSizetf(PLI_BYTE8 *user_data)
{
	return(32); /* $pow returns 32-bit values */
}
/********************************************************************/
/*	compiletf application to verify valid systf args.				*/
/********************************************************************/
PLI_INT32 PLIbook_PowCompiletf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_itr, arg_handle;
    PLI_INT32 	tfarg_type;
    int 		err_flag = 0;
    do { /* group all tests, so can break out of group on error */
        systf_handle 	= vpi_handle(vpiSysTfCall, NULL);
        arg_itr 		= vpi_iterate(vpiArgument, systf_handle);
        if (arg_itr == NULL) {
            vpi_printf("ERROR: $pow requires 2 arguments; has none\n");
            err_flag = 1;
       	 	break;
    	}
            
        arg_handle = vpi_scan(arg_itr);
        tfarg_type = vpi_get(vpiType, arg_handle);
        if ( 	(tfarg_type != vpiReg) &&
                (tfarg_type != vpiIntegerVar) &&
                (tfarg_type != vpiConstant) ) {
            vpi_printf("ERROR: $pow arg1 must be number, variable or net\n");
            err_flag = 1;
            break;
        }

        arg_handle = vpi_scan(arg_itr);
        if (arg_handle == NULL) {
            vpi_printf("ERROR: $pow requires 2nd argument\n");
            err_flag = 1;
            break;
        }

        tfarg_type = vpi_get(vpiType, arg_handle);
        if ( 	(tfarg_type != vpiReg) &&
                (tfarg_type != vpiIntegerVar) &&
                (tfarg_type != vpiConstant) ) {
            vpi_printf("ERROR: $pow arg2 must be number, variable or net\n");
            err_flag = 1;
            break;
        }

        if (vpi_scan(arg_itr) != NULL) {
            vpi_printf("ERROR: $pow requires 2 arguments; has too many\n");
            vpi_free_object(arg_itr);
            err_flag = 1;
            break;
        }
    } while (0 == 1); /* end of test group; only executed once */
        
    if (err_flag) {
    	vpi_control(vpiFinish, 1); /* abort simulation */
    }
    return(0);
}
/********************************************************************/
/*	calltf to calculate base to power of exponent and return result.*/
/********************************************************************/
#include <math.h>
PLI_INT32 PLIbook_PowCalltf(PLI_BYTE8 *user_data)
{
	s_vpi_value value_s;
	vpiHandle 	systf_handle, arg_itr, arg_handle;
	PLI_INT32 	base, exp;
	double 		result;
	systf_handle 	= vpi_handle(vpiSysTfCall, NULL);
	arg_itr 		= vpi_iterate(vpiArgument, systf_handle);
    if (arg_itr == NULL) {
        vpi_printf("ERROR: $pow failed to obtain systf arg handles\n");
        return(0);
    }
        
    /* read base from systf arg 1 (compiletf has already verified) */
    arg_handle 		= vpi_scan(arg_itr);
    value_s.format 	= vpiIntVal;
    vpi_get_value(arg_handle, &value_s);
    base 			= value_s.value.integer;
    
    /* read exponent from systf arg 2 (compiletf has already verified) */
    arg_handle = vpi_scan(arg_itr);
    vpi_free_object(arg_itr); /* not calling scan until returns null */
    vpi_get_value(arg_handle, &value_s);
    exp = value_s.value.integer;
    
    /* calculate result of base to power of exponent */
    result = pow( (double)base, (double)exp );
    
    /* write result to simulation as return value $pow */
    value_s.value.integer = (PLI_INT32)result;
    vpi_put_value(systf_handle, &value_s, NULL, vpiNoDelay);
    return(0);
}
/********************************************************************/
/*	Start-of-simulation application									*/
/********************************************************************/
PLI_INT32 PLIbook_PowStartOfSim(s_cb_data *callback_data)
{
    vpi_printf("\n$pow PLI application is being used.\n\n");
    return(0);
}
```

## *Interfacing PLI applications to Verilog simulators*

As the previous sections in this chapter have shown, a PLI application may comprise:

- A system task or system function name

- A *calltf routine*

- A *compiletf routine*

- A *sizetf routine*

- Any number of *simulation callback routines*

The VPI interface mechanism involves three basic steps:

- Create a register function, which associates the system task/function name with the application routines.

- Notify the Verilog simulator about the registration function.

- Link the applications into a Verilog simulator, so the simulator can call the appropriate routine when the system task/function name is encountered.

The VPI Interface Mechanism is defined as part of the IEEE 1364 standard, providing a consistent method for all Verilog simulators to use. The VPI interface is used to specify:

- A system task/function **name.**

- The application **type,** which is a *task, sized function, integer function, time function* or *real function.*

- Pointers to the C functions for a *calltf routine, compiletf routine* and *sizetf routine,* if the routines exist (it is not required—and often not necessary—to provide each class of routine).

- A **user_data** pointer value, which the simulator will pass to the *calltf routine,* *compiletf routine* and *sizetf routine* each time they are called.

The process of specifying the PLI application information is referred to as **registering** the application. To register a PLI application, the information about the application is specified in an **`s_vpi_systf_data`** structure. This structure is defined as part of the VPI standard, in the PLI *`vpi_user.h`* file. The definition is:

```c
typedef struct t_vpi_systf_data {
    PLI_INT32 type; 						/* 	vpiSysTask, vpiSysFunc 		*/
    PLI_INT32 sysfunctype; 					/* 	vpiIntFunc, vpiRealFunc,
    											vpiTimeFunc, vpiSizedFunc,
    											vpiSizedSignedFunc 			*/
    PLI_BYTE8 *tfname; 						/* quoted task/ function name 	*/
    PLI_INT32 (*calltf) (PLI_BYTE8 *); 		/* name of C func 				*/
    PLI_INT32 (*compiletf) (PLI_BYTE8 *); 	/* name of C func 				*/
    PLI_INT32 (*sizetf) (PLI_BYTE8 *); 		/* name of C func 				*/
    PLI_BYTE8 *user_data; 					/* returned with callback 		*/
} s_vpi_systf_data, *p_vpi_systf_data;
```

The table explains the fields of the `s_vpi_systf_data` structure:

​    ![image-20221023102225437](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221023102225437.png )

### **The steps required to register a PLI application**

- Create a C function to register the system task/function. The C function name is user-defined and can be any legal C name.

- Allocate an `s_vpi_systf_data` C structure.

- Fill in the fields of the structure with the information about the system task or system function.

- Register the system task/function by calling the VPI routine **vpi_register_systf().**

- Notify the simulator about the name of the register function.

The register function can be located in any C source file, but is typically located in the same file as the PLI application C functions.

```c
/* prototypes of PLI application routine names */
PLI_INT32 	PLIbook_PowSizetf(),
			PLIbook_PowCalltf(),
			PLIbook_PowCompiletf(),
void PLIbook_pow_register()
{
    s_vpi_systf_data 	tf_data;
    s_cb_data 			cb_data_s;
    s_vpi_time 			time_s;
    tf_data.type			= vpiSysFunc;
    tf_data.sys functype	= vpiSizedFunc;
    tf_data.tfname			= “$pow”;
    tf_data.calltf			= PLIbook_PowCalltf;
    tf_data.compiletf		= PLIbook_PowCompiletf;
    tf_data.sizet£			= PLIbook_PowSizetf;
    tf_data.user_data		= NULL;
    vpi_register_systf(&tf_data) ;
}
```

### **Notifying Verilog simulators about PLI applications**

Once the register function has been defined, a Verilog simulator must be notified of the name of the register function, so that the simulator can call the functions and register the PLI applications. 

Some common methods are:

- Invocation options which specify the names of the register functions.
- Invocation options which specify a file containing the names of the register functions.
- A special array, called **vlog_startup_routines,** which contains the names of the register functions.

```c
/* prototypes of the PLI application routines */
extern void PLIbook_pow_register(), PLIbook_ShowVal_register();
void (*vlog_startup_routines[])() =
{
    /*** add user entries here ***/
    PLIbook_pow_register,
    PLIbook_ShowVal_register,
    0 /*** final entry must be 0 ***/
};
```

**Do not place the vlog_startup_routines array in the same C source file as the PLI** **application!**

In a typical design environment, PLI applications will come from several sources, such as internally developed applications and 3rd party applications. If the *vlog_startup_routines* array and a PLI application and are in the same file, then the source code for the application must be available whenever another PLI application needs to be added to the start-up array.

The register functions are executed by the simulator before simulation time 0, possibly before the creation of the simulation data structure is complete. This limits what operations can be performed within register functions. The VPI routines which can be used in a register function are:

- **vpi_register_systf()**
- **vpi_register_cb()**
- VPI routines which do not access objects in simulation, such as **`vpi_printf()`**. It is an error to attempt obtain a handle for an object or any object properties.

## *Using the VPI user_data field*

When a system task or system function is registered, a **user_data** value can be specified. The **user_data** is a pointer, which can point to a block of application-allocated data. This **user_data** value is passed to the *calltf routine, compiletf routine* and *sizetf* *routine* as a C function input each time the simulator calls one of these routines.

In the following example, two different system tasks, *$get_vector_bin* and *$get_vector_hex,* are associated with the same *calltf routine.* The registration function for these system tasks is:

```c
void PLlbook_test_user_data_register()
{
    s_vpi_systf_data tf_data;
    char *id1 = malloc(sizeof(int)); /* allocate storage */
    char *id2 = malloc(sizeof(int)); /* allocate storage */
    *id1= 1;
    *id2 = 2;
    tf_data.type = vpiSysFunc;
    tf_data.sysfunctype = vpiSysFuncSized;
    tf_data.tfname = "$get_vector_bin";
    tf_data.calltf = PLIbook_GetVectorCalltf;
    tf_data.compiletf = NULL;
    tf_data.sizetf = NULL;
    tf_data.user_data = (PLI_BYTE8 *)id1;
    vpi_register_systf(&tf_data);
    tf_data.type = vpiSysFunc;
    tf_data.sysfunctype = vpiSysFuncSized;
    tf_data.tfname = "$get_vector_hex";
    tf_data.calltf = PLIbook_GetVectorCalltf;
    tf_data.compiletf = NULL;
    tf_data.sizetf = NULL;
    tf_data.user_data = (PLI_BYTE8 *)id2;
    vpi_register_systf(&tf_data);
}
```

Both system tasks invoke the same *calltf routine,* but the **user_data** value for the two system task names is a pointer to a different block of application-allocated storage. Therefore, the *calltf routine* can check the **user_data** value to determine which system task name was used to call the routine.
