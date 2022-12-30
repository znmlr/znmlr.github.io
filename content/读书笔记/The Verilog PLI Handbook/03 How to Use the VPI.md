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

## *Verilog HDL objects*

- The VPI routines treat Verilog HDL constructs as **objects**

```systemverilog
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

### **The vpiHandle data type**

- The VPI routines use a special data type, called a **handle**, to access Verilog HDL and simulation objects. 
- A handle is not a pointer to the actual object, it is a pointer to information about the object. 
- The declaration type for variables to store a handle is **vpiHandle**. 
- The vpiHandle data type is defined in the VPI library (the vpi_user.hfile). 
- An example declaration for two handle variables is:

​		`vpiHandle primitive_handle, net_handle;`

- There are several VPI routines that locate an object within a simulation data structure and return the handle for the object. 
- Other VPI routines are used to access information about the object, using the object’s handle as a reference point. 
- The information that can be accessed depends on the type of the object, but might include the object’s name and current logic value.

### **Object relationships**

The VPI standard documents three types of object relationships:

- **One-to-one relationships** occur when an object is related to only one other object. 

- **One-to-many relationships** occur when an object is related to several other objects of a certain type.
- **Many-to-one relationships** occur when many objects are related to a single other object of a certain type.

## *Obtaining object handles*

### **Obtaining a handle for a one-to-one relationship**

**vpi_handle()** obtains a handle for a target object with a one-to-one relationship from the reference object. The syntax for this routine is:

```verilog
vpiHandle vpi_handle (
	PLI_INT32 type,			/* constant representing an object type */
	vpiHandle reference )	/* handle for an object */
```

The PLI application for *$show_all_nets* will need to read the module instance name listed as the argument of the system task. In order to access the argument, the PLI application must first obtain a handle for the instance of the system task which called the application. The object diagram for a system task call shows the following one-to one relationship

Therefore, the PLI applications can obtain a handle for the system task call using the following C code.

```c
vpiHandle systf_handle;
systf_handle = vpi_handle(vpiSysTfCall, NULL);
```

### **Obtaining a handle for a one-to-many relationship**

- The routines **vpi_iterate()** and **vpi_scan()** are used to obtain handles for all objects when there is a one-to-many relationship.

```c
vpiHandle vpi_iterate (
    PLI_INT32 type,			/* constant representing an object type */
    vpiHandle reference )	/* handle for an object */
```

- The vpi_iterate() routine returns an **iterator object**. The routine uses the type constant to determine the type of object for which handles are to be obtained, and the reference_handle to determine the source point of the one-to-many relationship.

- The **iterator object** returned from vpi_iterate() represents the first of the many target objects in the relationship. As each target object is accessed, the iterator is updated automatically to reference the next target object. 
- Conceptually, the many target objects can be thought of as a list of object handles, and the iterator as a pointer to the next object in the list. 
- Note that the usage of a list is purely conceptual—the VPI standard does not require that a simulator create and store lists of target objects. 
- Since the VPI uses the more abstract iterator object to reference each target object, a simulator can maintain its internal storage in any form.

- A one-to-many relationship indicates a relationship from a reference object to any number of target objects, including none. 
- For example, a module might not have any nets declared within it, a single net declared, or multiple nets. 
- If there are no target objects in a one-to-many relationship, then vpi_iterate() returns a **NULL** as the iterator value.

```c
vpiHandle vpi_scan (
	vpiHandle iterator ) /* handle for an iterator object */
```

- The vpi_scan() routine is provided a single input, the iterator object which was returned fromvpi_iterate(). 
- The vpi_scan() routine returns the handle for the next target object which the iterator references. When are there are no more target objects, the next call to vpi_scan() will return NULL. 
- In order to access all of the objects in a one-to-many relationship, vpi_scan() must be called multiple times, until the return value is NULL.

The following C code fragment uses vpi_iterate() and vpi_scan() to obtain handles for all nets within a module:

```c
vpiHandle module_handle, net_iterator, net_handle;
/* assume a module handle has already been obtained */
net_iterator = vpi_iterate(vpiNet, module_handle);
if (net_iterator == NULL)
	vpi_printf(“ No nets found in this module\n”);
else {
    while ( (net_handle = vpi_scan(net_iterator)) != NULL ) {
    	... /* code to access information about the net object */
    }
}
```

### **Comparing VPI handles**

- A VPI handle is an abstraction used to reference an object within simulation. All VPI routines use this abstraction to access information about the object. 
- When a VPI application obtains a handle to an object, that handle is not a pointer to the actual object, but rather a pointer to information about the object.

- Since the handle for an object is an abstraction, **it is not possible to determine if two handles reference the same object using the C ‘==’ operator**. 
-  The handle values may not be equivalent, even if they reference the same object. Instead, the VPI library provides a special routine to see if two handles reference the same object.

```c
PLI_INT32 vpi_compare_objects (
    vpiHandle object1,	/* handle for an object */
    vpiHandle object2)	/* handle for an object */
```

- vpi_compare_objects() returns a **1** (for true) if two handles reference the same object, and a **0** (for false) if they do not.

## *Accessing the arguments of a system task/function*

- For *$show_all_nets*, the PLI application will need to access the first argument of the system task, which should be a module instance name. For example:

```verilog
$show_all_nets(top.i1);
```

- A system task can have any number of arguments. As shown in the object diagram in this Figure, there is a one-to-many relationship, indicated by the double arrow, between a system task/function call and the arguments of the system task/function.

 ![image-20221028224130684](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221028224130684.png)

- The *$show_all_nets* application can obtain a handle for the module instance that is named in the first system task argument using vpi_iterate() and vpi_scan(), as shown in the following C code fragment:

```c
vpiHandle systf_handle, module_handle,
	net_iterator, net_handle;

systf_handle = vpi_handle(vpiSysTfCall, NULL);
arg_iterator = vpi_iterate(vpiArgument, systf_handle);
module_handle = vpi_scan(arg_iterator);

if (module_handle ! == NULL)
	vpi_free_object(arg_iterator); 	/*free iterator memory */
```

- This memory required to store the iterator object is automatically allocated by the simulator when vpi_iterate() is called, and is automatically freed when vpi_scan() returns NULL after all target objects have been accessed. 
- In the preceding example, however, vpi_scan() was only called one time. If the return from vpi_scan() is not NULL, then a handle to the object listed as the first task/function argument was obtained. 
- The non-NULL value means the memory for the iterator object has not yet been automatically freed. Since the *$show_all_nets* application has obtained a handle for the first system task argument, the application no longer needs the iterator and should therefore notify the simulator to release the memory for the iterator. 
- The application could continue to call vpi_scan() until a NULL is returned, but the VPI library also provides a special routine to release the iterator object memory when an iterator is no longer needed.

```c
PLI_INT32 vpi_free_object (
	vpiHandle handle) /* handle for an object */
```

- The vpi_free_object() routine is used to release memory which the simulator has allocated for an object. 

## *Printing messages from VPI applications*

The VPI library uses a special routine for printing text messages.

```c
PLI_INT32 vpi_printf (
    PLI_BYTE8 * format,	/* character string containing a formatted message */
    …)					/* arguments to the formatted message string */
```

The syntax for this routine is essentially the same as the C printf() routine, but there is one very important difference: vpi_printf() will print the message to the simulation output channel, and to the simulation output log file. 

## *Accessing object properties*

- Every Verilog object has one or more properties which can be accessed by a PLI application. Some properties are the name of a module or net and the logic value of a net. 
- Most properties will be either an integer value or a string value. The VPI identifies these properties using a property constant.

- Two VPI routines are provided to read these types of properties.

```c
PLI_INT32 vpi_get (
    PLI_INT32 property,	/* constant representing an object’s property */
    vpiHandle object)	/* handle for an object */
```

- Returns the value associated with integer and boolean properties of an object. Bool ean properties return 1 for true and 0 for false.

```c
PLI_BYTE8 *vpi_get_str (
    PLI_INT32 property,	/* constant representing an object property */
    vpiHandle object)	/* handle for an object */
```

- Returns a pointer to a string containing the value associated with string properties of an object.

### **Object type properties**

- Every Verilog object has an integer **type** property, which is accessed using:

```c
PLI_INT32 obj_type;
obj_type = vpi_get(vpiType, <object_handle>)
```

- The type property identifies what kind of Verilog object is referenced by a VPI handle. 
- This type property is represented by an integer constant, which is defined in the vpi_user.h file. Some example type constants are:

> - **vpiModule** — the object handle is referencing a Verilog module instance
>
> - **vpiPrimitive** — the object handle is referencing a Verilog primitive instance
>
> - **vpiNet** — the object handle is referencing a Verilog net data type
>
> - **vpiReg** — the object handle is referencing a Verilog reg data type

- The type property can be used many different ways. One common usage is to verify that a handle which was obtained references the type of object expected. 
- For example, the *$show_all_nets* application requires the first task/function argument be a module instance. The following code fragment uses this type property to verify that the argument provided to *$show_all_nets* is correct:

```c
vpiHandle systf_handle, arg_iterator, arg_handle;
PLI_INT32 tfarg_type;

systf_handle = vpi_handle(vpiSysTfCall, NULL);
arg_iterator = vpi_iterate(vpiArgument, systf_handle);
arg_handle = vpi_scan(arg_iterator);
tfarg_type = vpi_get(vpiType, arg_handle);

if (tfarg_type != vpiModule) {
	/* report error that argument is not correct */
```

- The vpiType property is both an integer and a string property. Using vpi_get( vpiType, <object_handle>) will return the integer value of the

  type constant. Using vpi_get_str(vpiType, <object_handle>) will return a pointer to a string containing the name of the type constant.

### **Object name properties**

Many Verilog objects have one or more **name** properties.

- The property represented by the property constant **vpiName** is the local name of an object. For objects such as nets and variables, the local name is the *declaration name* of the object. For a module or primitive, the local name is the *instance name* within the module in which the module or primitive is used.
- The property represented by the property constant **vpiFullName** is the full hierarchical path name of an object.
- The property represented by the property constant **vpiDefName** is the definition name of a module or primitive.

 ![image-20221029113532413](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221029113532413.png)

## *Reading the logic values of Verilog objects*

- The VPI library provides a routine to read the logic value of any Verilog object which can contain a value, such as a net or variable.

```c
void vpi_get_value(
    vpiHandle object,	/* handle for an object */
    p_vpi_value value)	/* pointer to application-allocated s_vpi_value structure */
```

- The Verilog language uses 4-state logic values, comprising logic 0, 1, Z and X. The vpi_get_value() routine automatically converts Verilog 4-state logic into various C data types for use in PLI applications. 
- A simple way to represent 4-state logic in C is to use character strings, and this is the method used in the *$show_all_nets* application. 

- The PLI application must allocate an s_vpi_value structure prior to calling vpi_get_value().

```c
typedef struct t_vpi_value {
	PLI_INT32 format;		/* 	vpiBinStrVal,	vpiOctStrVal,
                                vpiDecStrVal,	vpiHexStrVal,
                                vpiScalarVal,	vpiIntVal,
                                vpiRealVal,		vpiStringVal,
                                vpiVectorVal,	vpiTimeVal,
                                vpiStrengthVal,	vpiSuppressVal,
                                vpiObjTypeVal 						*/
    union {
        PLI_BYTE8 *str;		/*	if any string format 				*/
        PLI_INT32 scalar;	/*	if vpiScalarVal: one of vpi0, vpi1,
        						vpiX,vpiZ,vpiH,vpiL,vpiDontCare 	*/
        PLI_INT32 integer;	/*	if vpiIntVal format 				*/
        double real;		/*	if vpiRealVal format 				*/
        struct t_vpi_time 			*time; 		/* if vpiTimeVal 	*/
        struct t_vpi_vecval 		*vector; 	/* if vpiVectorVal 	*/
        struct t_vpi_strengthval 	*strength; 	/* if vpiStrengthVal*/
        PLI_BYTE8 					*misc; 		/* not used 		*/
	} value;
} s_vpi_value, *p_vpi_value;
```

The s_vpi_value structure contains two primary fields:

- The **format** field controls how the Verilog logic value should be represented in C. The format is a VPI constant. 
- The **value** field receives the logic value. This field is a union of C data types, and the format constant determines which field within this union that will be used. 

The following example retrieves the logic value of a net as a C string:

```c
vpiHandle net_handle;
s_vpi_value current_value;
current_value.format = vpiBinStrVal; /* read as a string */
vpi_get_value(net_handle, &current_value);
vpi_printf(“ net %s value is %s (binary)\n”, vpi_get_str(vpiName, net_handle), current_value.value.str);
```

- vpi_get_value() automatically allocates storage for the string which contains the logic value. This storage is temporary, and will automatically be freed when another call is made to vpi_get_value() or when the PLI application exits.

## *Reading the current simulation time*

```c
void vpi_get_time (
    vpiHandle object,	/* handle for an object, or NULL */
    p_vpi_time time )	/* pointer to application-allocated s_vpi_time structure */
```

- The**<object_handle>** is a handle for any object in a design. When simulation time is retrieved in the time scale of a module, the module that is used will be the one containing the object.

- The **<time_structure_pointer>** is a pointer to an **s_vpi_time** structure to receive the current simulation time.

- The PLI application does not define the structure. The application only allocates memory for the structure. The structure definition is:

```c
typedef struct t_vpi_time {
	PLI_INT32 	type;	/* vpiScaledRealTime or vpiSimTime 	*/
	PLI_UINT32 	high;	/* when using vpiSimTime 			*/
	PLI_UINT32 	low;	/* when using vpiSimTime 			*/
	double 		real;	/* when using vpiScaledRealTime 	*/
} s_vpi_time, *p_vpi_time;
```

- The **type** field controls how the Verilog simulation time will be received. The format is set using a constant which is defined in the VPI library.

> - A format of **vpiScaledRealTime** indicates the simulation time will be retrieved as a floating point number and that the time will be scaled to the time units of the module containing the object specified in the call to vpi_get_time(). The **real** field receives the simulation time value when the format field is vpiScaledRealTime.
> - A format of **vpiSimTime** indicates the simulation time should be retrieved as a 64-bit integer and that the time will be in the internal simulation time units.Since not all computer platforms and operating systems have a 64-bit integer data type, the 64-bit value is split into two 32-bit unsigned C integers, as shown in the following diagram:
>
>  ![image-20221029172248872](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221029172248872.png)

- The *$show_all_nets* application retrieves and prints the current simulation time using vpi_get_time() as follows:

```c
vpiHandle module_handle;
s_vpi_time current_time;

current_time.type = vpiscaledRealTime;
vpi_get_time(module_handle, &current_time);
vpi_printf(“\nAt time %2.2f, nets in module %s (%s):\n”,
    current_time.real,
    vpi_get_str(vpiFullName, module_handle),
    vpi_get_str(vpiDefName, module_handle));
```

## *Controlling simulation from PLI applications*

- There are occasions when a PLI application needs to control what a Verilog simulator is doing. 
- In the *$show_all_nets* application, a *compiletf routine* will be provided to perform syntax checking. 
- If a serious error is detected, such as the argument provided to *$show_all_nets* is not a module instance name, then the PLI application needs to abort simulation execution. 
- That is, to treat the error as a fatal error. The routine vpi_control() is used to abort simulation.

```c
PLI_INT32 vpi_control (
    PLI_INT32 operation,	/* constant representing the operation to perform 				*/
    ...)					/* variable number of arguments, as required by the operation 	*/
```

- The vpi_control() routine allows a PLI application to control certain aspects of simulation. Returns **1** if successful and **0** if an error occurred. Several operation constants are defined in the IEEE 1364 standard (simulators may add additional flags specific to that product):

> - **vpiStop** causes the *$stop( )* built-in Verilog system task to be executed upon return of the PLI application. Requires one additional argument of type PLI_INT32, which is the same as the diagnostic message level argument passed to *$stop( ).*
> - **vpiFinish** causes the *$finish( )* built-in Verilog system task to be executed upon return of the PLI application. Requires one additional argument of type PLI_INT32, which is the same as the diagnostic message level argument passed to *$finish( ).*
> - **vpiReset** causes the *$reset( )* built-in Verilog system task to be executed upon return of the PLI application Requires three additional arguments of type PLI_INT32: **stop_value**, **reset_value** and **diagnostic_level**, which are the same values passed to the *$reset( )* system task.
> - **vpiSetInteractiveScope** causes a simulator’s interactive debug scope to be immediately changed to a new scope. Requires one additional argument of type vpi Handle, which is a handle to an object in the scope class.

## *A complete PLI application using VPI routines*

###  **PLI application source code for $show_all_nets**

```c
#include <stdlib.h>		/* ANSI C standard library 				*/
#include <stdio.h>		/* ANSI C standard input/output library */
#include <stdarg.h>		/* ANSI C standard arguments library 	*/
#include "vpi_user.h"	/* IEEE 1364 PLI VPI routine library 	*/

/* prototypes of the PLI application routines */
PLI_INT32 	PLIbook_ShowNets_compiletf(PLI_BYTE8 *user_data),
			PLIbook_ShowNets_calltf(PLI_BYTE8 *user_data);
/****************************************************************/
/* $show_all_nets Registration Data 							*/
/****************************************************************/
void PLIbook_ShowNets_register()
{
    s_vpi_systf_data tf_data;
    tf_data.type = vpiSysTask;
    tf_data.sysfunctype = 0;
    tf_data.tfname = "$show_all_nets";
    tf_data.calltf = PLIbook_ShowNets_calltf;
    tf_data.compiletf = PLIbook_ShowNets_compiletf;
    tf_data.sizetf = NULL;
    tf_data.user_data = NULL;
    vpi_register_systf(&tf_data);
    return;
}
/****************************************************************/
/*  compiletf routine 											*/
/****************************************************************/   
PLI_INT32 PLIbook_ShowNets_compiletf(PLI_BYTE8 *user_data)
{
    vpiHandle systf_handle, arg_iterator, arg_handle;
    PLI_INT32 tfarg_type;
    int err_flag = 0;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handles to system task arguments */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    if (arg_iterator == NULL) {
        vpi_printf("ERROR: $show_all_nets requires 1 argument\n");
        err_flag = 1;
    }
    else {
    	/* check the type of object in system task arguments */
        arg_handle = vpi_scan(arg_iterator);
        tfarg_type = vpi_get(vpiType, arg_handle);
        if (tfarg_type != vpiModule) {
            vpi_printf("ERROR: $show_all_nets arg must be module instance\n");
            vpi_free_object(arg_iterator); /* free iterator memory */
            err_flag = 1;
    	}
    	else {
    		/* check that there is only 1 system task argument */
    		arg_handle = vpi_scan(arg_iterator);
    		if (arg_handle != NULL) {
                vpi_printf("ERROR: $show_all_nets can only have 1 argument\n");
                vpi_free_object(arg_iterator); /* free iterator memory */
                err_flag = 1;
    		} 
        } 
    } /* end of if-else-if-else-if sequence */
    if (err_flag) {
    	vpi_control(vpiFinish, 1); /* abort simulation */
    }
    return(0);
}
/****************************************************************/
/*  calltf routine 												*/
/****************************************************************/   
PLI_INT32 PLIbook_ShowNets_calltf(PLI_BYTE8 *user_data)
{
    vpiHandle	systf_handle, arg_iterator, module_handle,
    			net_iterator, net_handle;
    s_vpi_time current_time;
    s_vpi_value current_value;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handle to system task argument */
    /* compiletf has already verified only 1 arg with correct type */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    module_handle = vpi_scan(arg_iterator);
    vpi_free_object(arg_iterator); /* free iterator memory */
    
    /* read current simulation time */
    current_time.type = vpiScaledRealTime;
    vpi_get_time (systf_handle, &current_time);
    vpi_printf("\nAt time %2.2f, ", current_time.real);
    vpi_printf("nets in module %s ", vpi_get_str(vpiFullName, module_handle));
    vpi_printf("(%s):\n", vpi_get_str(vpiDefName, module_handle));
    
    /* obtain handles to nets in module and read current value */
    net_iterator = vpi_iterate(vpiNet, module_handle);
    if (net_iterator == NULL)
    	vpi_printf(" no nets found in this module\n");
    else {
        current_value.format = vpiBinStrVal; /* read values as a string */
        while ( (net_handle = vpi_scan(net_iterator)) != NULL ) {
            vpi_get_value(net_handle, &current_value);
            vpi_printf(" net %-10s value is %s (binary)\n", vpi_get_str(vpiName, net_handle), current_value.value.str);
        }
    }
    return(0);
}
```

### **A test bench for $show_all_nets**

```verilog
`timescale 1ns / 1ns
module top;
    reg [2:0] test;
    tri [1:0] results;

    addbit i1 (test[0], test[1], test[2], results[0], results[1]);
    
    initial
        begin
            test = 3’b000;
            #10 test = 3'b011;
            #10 $show_all_nets(top);
            #10 $show_all_nets(i1);
            #10 $stop;
            #10 $finish;
        end
endmodule

/*** A gate level 1 bit adder model ***/
`timescale 1ns / 1ns
module addbit (a, b, ci, sum, co);
    input a, b, ci;
    output sum, co;
    wire a, b, ci, sum, co, n1, n2, n3;
    xor (n1, a, b);
    xor #2 (sum, n1, ci);
    and (n2, a, b);
    and (n3, n1, ci);
    or #2 (co, n2, n3);
endmodule
```

###  **Simulation results for $show_all_nets**

```shell
At time 20.00, nets in module top (top):
  net results value is 10 (binary)
  
At time 30.00, nets in module top.i1 (addbit):
  net a		value is 1 (binary)
  net b		value is 1 (binary)
  net ci	value is 0 (binary)
  net sum	value is 0 (binary)
  net co	value is 1 (binary)
  net n1	value is 0 (binary)
  net n2	value is 1 (binary)
  net n3	value is 0 (binary)
```

## *Obtaining handles for reg and variable data types*

The Verilog HDL defines two general data type groups, **nets** and **variables**. The variable data type group includes the Verilog keywords **reg**, **integer**, **time** and **real**.The PLI treats the reg data type as a unique object, and groups the integer, time and real data types into an object class called **variables**.

Only minor changes are needed to enhance the *$show_all_nets* application so that it can display all the signals of all data types within a module. All that is required is to add additional vpi_iterate() and vpi_scan () statements to access the other signal data types.

The vpi_get_value() is used to read the values of any Verilog data type. The for mat field in the s_vpi_value structure establishes the C language data type to be used to represent the value. This gives the PLI application developer complete control over how values are represented in the application.

For the *$show_all_signals* application illustrated in this chapter, the following for mats will be used:

- For Verilog net data types, values will be represented as a C string, using a binary format.

- For Verilog reg data types, values will be represented as a C string, using a binary format.

- For Verilog integer data types, values will be represented as a 32-bit C integer.

- For Verilog real data types, values will be represented as a C double.

- For Verilog time data types, values will be represented as a pair of 32-bit unsigned integers.

```c
typedef struct t_vpi_time {
    PLI_INT32  	type; 	/* not used by vpi_get_value ( )	*/
    PLI_UINT32 	high; 	/* upper 32-bits of time value 		*/
    PLI_UINT32 	low; 	/* lower 32-bits of time value 		*/
    double 		real; 	/* not used by vpi_get_value ( ) 	*/
} s_vpi_time, *p_vpi_time;
```

The following C code fragment illustrates the steps required to read the value of a Verilog time variable and print the value in hexadecimal.

```c
vpiHandle signal_handle;
s_vpi_value current_value;

current_value.format = vpiTimeVal;
vpi_get_value(signal_handle, &current_value);
vpi_printf(“ time %-10s value is %x%x\n”,
	vpi_get_str(vpiName, signal_handle),
	current_value.value.time->high,
	current_value.value.time->low);
```

### **A complete PLI application for $show_all_signals**

```c
#include <stdlib.h> 	/* ANSI C standard library 				*/
#include <stdio.h> 		/* ANSI C standard input/output library */
#include <stdarg.h> 	/* ANSI C standard arguments library 	*/
#include "vpi_user.h" 	/* IEEE 1364 PLI VPI routine library 	*/

/* prototypes of the PLI application routines */
PLI_INT32 	PLIbook_ShowSighals_compiletf (PLI_BYTE8 *user_data),
			PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data);
void 		PLIbook_PrintSignalValues(vpiHandle signal_iterator);

/****************************************************************/
/* $show_all_signals Reg										*/
/****************************************************************/   
void PLIbook_ShowSignals_register()
{
    s_vpi_systf_data tf_data;
    tf_data.type 		= vpiSysTask;
    tf_data.sysfunctype = 0;
    tf_data.tfname 		= "$show_all_signals",-
    tf_data.calltf 		= PLIbook_ShowSignals_calltf;
    tf_data.compiletf 	= PLIbook_ShowSignals_compiletf;
    tf_data.sizetf 		= NULL;
    tf_data.user_data 	= NULL;
    vpi_register_systf(&tf_data);
    return;
}
/****************************************************************/
/* compiletf routine											*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_compiletf(PLI_BYTE8 *user_data)
{
    vpiHandle systf_handle, arg_iterator, arg_handle;
    PLI_INT32 tfarg_type;
    int err_flag = 0;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handles to system task arguments */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    if (arg_iterator == NULL) {
        vpi_printf("ERROR: $show_all_signals requires 1 argument\n");
        err_flag = 1;
    }
    else {
        /* check the type of object in system task arguments */
        arg_handle = vpi_scan(arg_iterator);
        tfarg_type = vpi_get(vpiType, arg_handle);
        if (tfarg_type != vpiModule) {
            vpi_printf("ERROR: $show_all_signals arg 1");
            vpi_printf(" must be a module instance\n");
            vpi_free_object(arg_iterator); /* free iterator memory */
            err_flag = 1;
        }
    	else {
            /* check that there is only 1 system task argument */
            arg_handle = vpi_scan(arg_iterator);
            if (arg_handle != NULL) {
                vpi_printf("ERROR: $show_all_signals can only have 1 argument\n");
                vpi_free_object(arg_iterator); /* free iterator memory */
                err_flag = 1;
    		} 
        } 
    } /* end of if-else-if-else-if sequence */
    if (err_flag) {
    	vpi_control(vpiFinish, 1); /* abort simulation */
    }
    return(0);
}
/****************************************************************/
/* calltf routine												*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_iterator, module_handle,
    			signal_iterator;
    PLI_INT32 format;
    s_vpi_time current_time;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handle to system task argument compiletf has already verified only 1 arg with correct type */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    module_handle = vpi_scan(arg_iterator);
    vpi_free_object(arg_iterator); /* free iterator memory */
    
    /* read current simulation time */
    current_time.type = vpiScaledRealTime;
    vpi_get_time(systf_handle, &current_time);
    vpi_printf("\nAt time %2.2f, ", current_time.real);
    vpi_printf("signals in module %s ", vpi_get_str(vpiFullName, module_handle));
    vpi_printf("(%s):\n", vpi_get_str(vpiDefName, module_handle));
    
    /* obtain handles to nets in module and read current value */
    signal_iterator = vpi_iterate(vpiNet, module_handle);
    if (signal_iterator != NULL)
    	PLIbook_PrintSignalValues(signal_iterator);
    
    /* obtain handles to regs in module and read current value */
    signal_iterator = vpi_iterate(vpiReg, module_handle);
    if (signal_iterator != NULL)
        PLIbook_PrintSignalValues(signal_iterator);
    
    /* obtain handles to variables in module and read current value */
    signal_iterator = vpi_iterate(vpiVariables, module_handle);
    if (signal_iterator != NULL)
    	PLIbook_PrintSignalValues(signal_iterator);
    vpi_printf("\n"); /* add some white space to output */
    return(0);
}
void PLIbook_PrintSignalValues(vpiHandle signal_iterator)
{
    vpiHandle signal_handle;
    PLI_INT32 signal_type;
    s_vpi_value current_value;
    
    while ( (signal_handle = vpi_scan(signal_iterator)) !=NULL ) {
        signal_type = vpi_get(vpiType, signal_handle);
        switch (signal_type) {
        case vpiNet:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" net %-10s value is %s (binary)\n",
                vpi_get_str(vpiName, signal_handle),
                current_value.value.str);
            break;
        case vpiReg:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" reg %-10s value is %s (binary)\n",
                vpi_get_str(vpiName, signal_handle),
                current_value.value.str);
            break;
        case vpiIntegerVar:
                current_value.format = vpilntval;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" integer %-10s value is %d (decimal)\n",
                vpi_get_str(vpiName, signal_handle),
                current_value.value.integer);
            break;
        case vpiRealVar:
                current_value.format = vpiRealVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" real %-10s value is %0.2f\n",
                vpi_get_str(vpiName, signal_handle),
                current_value.value.real);
            break;
        case vpiTimeVar:
                current_value.format = vpiTimeVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" time %-10s value is %x%x\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.time->high,
                	current_value.value.time->low);
            break;
        }
    }
    return;
}
```

```verilog
‘timescale 1ns / 1ns
module top;
    tri [1:0] results;
    integer test;
    real foo;
    time bar;
    addbit i1 (test[0], test[1], test[2], results[0], results[1]);
    
    initial
        begin
            test = 3’b000;
            foo = 3.14;
            bar = 0;
            bar[63:60] = 4’hF;
            bar[35:32] = 4’hA;
            bar[31:28] = 4’hC;
            bar[03:00] = 4’hE;
            #10 test = 3’b011;
            #10 $show_all_signals(top);
            #10 $show_all_signals(i1);
            #10 $stop;
            #10 $finish;
        end
endmodule

/*** An RTL level 1 bit adder model ***/
‘timescale 1ns / 1ns
    module addbit (a, b, ci, sum, co);
    input a, b, ci;
    output sum, co;
    wire a, b, ci;
    reg sum, co;
        
    always @(a or b or ci)
    	{co, sum) = a + b + ci;
endmodule
```

```shell
At time 20.00, signals in module top (top):
  net		results	value is 10 (binary)
  integer	test	value is 3 (decimal)
  real		foo		value is 3.14
  time		bar		value is f000000ac000000e

At time 30.00, signals in module top.i1 (addbit):
  net		a		value is 1 (binary)
  net		b		value is 1 (binary)
  net		b		value is 0 (binary)
  reg		sum		value is 0 (binary)
  reg		co		value is 1 (binary)
```

## *Obtaining a handle to the current hierarchy scope*

The Verilog language allows a system task or system function to be invoked from any hierarchy scope. A *scope* in the Verilog HDL is a level of design hierarchy and can be represented by several constructs:

- Module instances

- Named statement groups

- Verilog HDL tasks

- Verilog HDL function

The difference between no argument and a null argument is shown in the following two examples.

```verilog
// No system task/function arguments:
$show_all_signals;
// A null system task/function argument:
$show_all_signals();
```

The following Verilog source code shows the enhanced usage possibilities for the *$show_all_signals* example:

```verilog
module top;
    ...
	addbit i1 (a, b, ci, sum, co); 	// instance of an adder
    ...
    always @(sum or co)
        $show_all_signals; 			// list signals in this module
    always @(posedge clock)
        begin: local
            integer i;
            reg local_bus;
            ...
            $show_all_signals; 		// list signals in this block
        end
endmodule

module addbit (a, b, ci, sum, co) ;
    ...
    always @(sum or co)
    	$Show_all_aignals(); 		// list signals in this instance
endmodule
```

```c
#include <stdlib.h> 	/* ANSI C standard library 				*/
#include <stdio.h> 		/* ANSI C standard input/output library */
#include <stdarg.h> 	/* ANSI C standard arguments library 	*/
#include "vpi_user.h" 	/* IEEE 1364 PLI VPI routine library 	*/

/* prototypes of the PLI application routines */
PLI_INT32 	PLIbook_ShowSignals_compiletf(PLI_BYTE8 *user_data),
			PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data);
void 		PLIbook_PrintSignalValues(vpiHandle signal_iterator);
/****************************************************************/
/* $show_all_signals Registration Data							*/
/****************************************************************/ 
void PLIbook_ShowSignals_register()
{
    s_vpi_systf_data tf_data;
    tf_data.type 		= vpiSysTask;
    tf_data.sysfunctype = 0;
    tf_data.tfname 		= "$show_all_signals";
    tf_data.calltf 		= PLIbook_ShowSignals_calltf;
    tf_data.compiletf 	= PLIbook_ShowSignals_compiletf;
    tf_data.sizetf 		= NULL;
    tf_data.user_data 	= NULL;
    vpi_register_systf(&tf_data);
    return;
}
/****************************************************************/
/* compiletf routine											*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_compiletf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_iterator, arg_handle;
    PLI_INT32 	tfarg_type;
    int 		err_flag = 0;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handles to system task arguments */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    if (arg_iterator == NULL) {
    	return(0); /* no arguments OK; skip remaining checks */
    }
    
    /* check the type of object in system task arguments */
    arg_handle = vpi_scan(arg_iterator) ;
    tfarg_type = vpi_get(vpiType, arg_handle);
    switch (tfarg_type) {
        case vpiModule:
        case vpiTask:
        case vpiFunction:
        case vpiNamedBegin:
        case vpiNamedFork:
        	break; /* arg is a scope instance; continue to next check */
        case vpiOperation:
       	 	if (vpi_get(vpiOpType, arg_handle) == vpiNullOp)
        		break; /* null argument OK; continue to next check */
        default:
            /* wrong type specified for an argument */
            vpi_printf("ERROR: $show_all_signals arg 1");
            vpi_printf(" must be a scope instance or null\n");
            vpi_free_object(arg_iterator); /* free iterator memory */
        	err_flag = 1;
        }
        if (err_flag ==0) {
            /* check that there is only 1 system task argument */
            arg_handle = vpi_scan(arg_iterator);
            if (arg_handle != NULL) {
            vpi_printf("ERROR: $show_all_signals can only have 1 argument\n");
            vpi_free_object(arg_iterator); /* free iterator memory */
            err_flag = 1;
        } 
    } /* end of tests */
    if (err_flag) {
    	vpi_control(vpiFinish, 1); /* abort simulation */
    }
    return(0);
}
/****************************************************************/
/* calltf routine												*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_iterator, scope_handle,
    			signal_iterator;
    PLI_INT32 	format;
    s_vpi_time 	current_time;
    
    /* obtain a handle to the system task instance */
    systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handle to system task argument */
    arg_iterator = vpi_iterate(vpiArgument, systf_handle) ;
    if (arg_iterator == NULL) {
        /* no arguments -- use scope that called this application */
        scope_handle = vpi_handle(vpiScope, systf_handle);
    }
    else {
        /* compiletf has already verified arg is scope instance or null */
        scope_handle = vpi_scan(arg_iterator);
        vpi_free_object(arg_iterator); /* free iterator memory */
        if (vpi_get(vpiType, scope_handle) != vpiModule)
            /* arg isn’t a module instance; assume it is null */
            scope_handle = vpi_handle(vpiScope, systf_handle);
    }
    
    /* read current simulation time */
    current_time.type = vpiScaledRealTime;
    vpi_get_time(systf_handle, &current_time);
    vpi_printf("\nAt time %2.2f, signals in scope %s:\n", current_time.real, vpi_get_str(vpiFullName, scope_handle));
    /* obtain handles to nets in module and read current value */
    /* nets can only exist if scope is a module */
    if (vpi_get(vpiType, scope_handle) == vpiModule) {
        signal_iterator = vpi_iterate(vpiNet, scope_handle);
        if (signal_iterator != NULL)
            PLIbook_PrintSignalValues(signal_iterator);
    }

    /* obtain handles to regs in scope and read current value */
    signal_iterator = vpi_iterate(vpiReg, scope_handle);
    if (signal_iterator != NULL)
        PLIbook_PrintSignalValues(signal_iterator);
    
   	/* obtain handles to variables in scope and read current value */
    signal_iterator = vpi_iterate(vpiVariables, scope_handle);
    if (signal_iterator != NULL)
    	PLIbook_PrintSignalValues(signal_iterator);
    vpi_printf ("\n"); /* add some white space to output */
    return(0) ;
}

void PLIbook_PrintSignalValues(vpiHandle signal_iterator)
{
    vpiHandle	signal_handle;
    int 		signal_type;
    s_vpi_value current_value;
    
    while ( (signal_handle = vpi_scan(signal_iterator)) != NULL ) {
        signal_type = vpi_get(vpiType, signal_handle);
        switch (signal_type) {
        	case vpiNet:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" net %-10s value is %s (binary)\n",
                	vpi_get_str(vpiName, signal_handle),
                    current_value.value.str);
            break;
        case vpiReg:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" reg %-10s value is %s (binary)\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.str);
            break;
        case vpiIntegerVar:
                current_value.format = vpiIntVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" integer %-10s value is %d (decimal)\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.integer);
            break;
        case vpiRealVar:
                current_value.format = vpiRealVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" real %-10s value is %0.2f\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.real);
            break;
        case vpiTimeVar:
                current_value.format = vpiTimeVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" time %-10s value is %x%x\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.time->high,
                	current_value.value.time->low);
            break;
        }
    }
    return;
}
```

```c
#include <stdlib.h> 	/* ANSI C standard library 				*/
#include <stdio.h> 		/* ANSI C standard input/output library */
#include <stdarg.h> 	/* ANSI C standard arguments library 	*/
#include "vpi_user.h" 	/* IEEE 1364 PLI VPI routine library 	*/

/* prototypes of the PLI application routines */
PLI_INT32 	PLIbook_ShowSignals_compiletf(PLI_BYTE8 *user_data),
			PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data);
void 		PLIbook_GetAllSignals(vpiHandle scope_handle, p_vpi_time current_time),
			PLIbook_PrintSignalValues(vpiHandle signal_iterator);
/****************************************************************/
/* $show_all_signals Registration Data							*/
/****************************************************************/ 
void PLIbook_ShowSignals_register()
{
    s_vpi_systf_data tf_data;
    tf_data.type 		= vpiSysTask;
    tf_data.sysfunctype = 0;
    tf_data.tfname 		= "$show_all_signals";
    tf_data.calltf 		= PLIbook_ShowSignals_calltf;
    tf_data.compiletf 	= PLIbook_ShowSignals_compiletf;
    tf_data.sizetf 		= NULL;
    tf_data.user_data 	= NULL;
    vpi_register_systf(&tf_data);
    return;
}
/****************************************************************/
/* compiletf routine											*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_compiletf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_iterator, arg_handle;
    PLI_INT32 	tfarg_type;
    int 		err_flag = 0, tfarg_num = 0;

    /* obtain a handle to the system task instance */
	systf_handle = vpi_handle(vpiSysTfCall, NULL);
    
    /* obtain handles to system task arguments */
	arg_iterator = vpi_iterate(vpiArgument, systf_handle);
    if (arg_iterator == NULL) {
    	return(0); /* no arguments OK; skip remaining checks */
    }

    /* check each argument */
    while ( (arg_handle = vpi_scan(arg_iterator)) != NULL ) {
    	tfarg_num++;
    	/* check the type of object in system task arguments */
    	tfarg_type = vpi_get(vpiType, arg_handle);
    	switch (tfarg_type) {
            case vpiModule:
            case vpiTask:
            case vpiFunction:
            case vpiNamedBegin:
            case vpiNamedFork:
    			break; /* arg is a scope instance; continue to next check */
    		case vpiOperation:
                if (vpi_get(vpiOpType, arg_handle) == vpiNullOp) {
                	break; /* null argument OK; continue to next check */
                }
    		default:
    			/* wrong type specified for an argument */
                vpi_printf("ERROR: $show_all_signals arg %d", tfarg_num);
                vpi_printf(" must be a scope instance or null\n");
                vpi_free_object(arg_iterator); /* free iterator memory */
                err_flag = 1;
    	}
    } /* end of tests */
    if (err_flag) {
    	vpi_control(vpiFinish, 1); /* abort simulation */
    }
    return(0);
}
/****************************************************************/
/* calltf routine												*/
/****************************************************************/ 
PLI_INT32 PLIbook_ShowSignals_calltf(PLI_BYTE8 *user_data)
{
    vpiHandle 	systf_handle, arg_iterator, scope_handle;
    PLI_INT32 	format;
    s_vpi_time 	current_time;

    /* obtain a handle to the system task instance */
	systf_handle = vpi_handle(vpiSysTfCall, NULL);

    /* read current simulation time */
    current_time.type = vpiScaledRealTime;
    vpi_get_time(systf_handle, &current_time);
    
    /* obtain handle to system task argument */
	arg_iterator = vpi_iterate(vpiArgument, systf_handle);
	if (arg_iterator == NULL) {
        /* no arguments -- use scope that called this application */
        scope_handle = vpi_handle(vpiScope, systf_handle);
        PLIbook_GetAllSignals(scope_handle, &current_time);
    }
	else {
        /* compiletf has already verified arg is scope instance or null */
        while ( (scope_handle = vpi_scan(arg_iterator)) != NULL ) {
        	if (vpi_get(vpiType, scope_handle) != vpiModule) {
                /* arg isn’t a module instance; assume it is null */
                scope_handle = vpi_handle(vpiScope, systf_handle);
        	}
			PLIbook_GetAllSignals(scope_handle, &current_time);
		}
	}
	return(0);
}
void PLIbook_GetAllSignals(vpiHandle scope_handle, p_vpi_time current_time)
{
    vpiHandle signal_iterator;
    
    vpi_printf("\nAt time %2.2f, ", current_time->real);
    vpi_printf("signals in scope %s ", vpi_get_str(vpiFullName, scope_handle));
    vpi_printf("(%s):\n", vpi_get_str(vpiDefName, scope_handle));
    
    /* obtain handles to nets in module and read current value */
    /* nets can only exist if scope is a module */
    if (vpi_get(vpiType, scope_handle) == vpiModule) {
    	signal_iterator = vpi_iterate(vpiNet, scope_handle);
    	if (signal_iterator != NULL)
    		PLIbook_PrintSignalValues(signal_iterator);
    }
    
    /* obtain handles to regs in scope and read current value */
    signal_iterator = vpi_iterate(vpiReg, scope_handle);
    if (signal_iterator != NULL)
    	PLIbook_PrintSignalValues(signal_iterator);
    
    /* obtain handles to variables in scope and read current value */
    signal_iterator = vpi_iterate(vpiVariables, scope_handle);
    if (signal_iterator != NULL)
    	PLIbook_PrintSignalValues(signal_iterator);
    vpi_printf("\n"); /* add some white space to output */
    return;
}

void PLIbook_PrintSignalValues(vpiHandle signal_iterator)
{
    vpiHandle 	signal_handle;
    int 		signal_type;
    s_vpi_value current_value;
    while ( (signal_handle = vpi_scan(signal_iterator)) != NULL ) {
        signal_type = vpi_get(vpiType, signal_handle);
        switch (signal_type) {
            case vpiNet:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" net %-10s value is %s (binary)\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.str);
            break;
        case vpiReg:
                current_value.format = vpiBinStrVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf (" reg %-10s value is %s (binary)\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.str);
            break;
        case vpiIntegerVar:
                current_value.format = vpiIntVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" integer %-10s value is %d (decimal)\n",
                	vpi_get_str(vpiName, sighal_handle),
                	current_value.value.integer);
            break;
        case vpiRealVar:
                current_value.format = vpiRealVal;
                vpi_get_value (signal_handle, &current_value) ;
                vpi_printf(" real %-10s value is %0.2f\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.real);
            break;
        case vpiTimeVar:
                current_value.format = vpiTimeVal;
                vpi_get_value(signal_handle, &current_value);
                vpi_printf(" time %-10s value is %x%x\n",
                	vpi_get_str(vpiName, signal_handle),
                	current_value.value.time->high,
                	current_value.value.time->low);
            break;
        }
    }
    return;
}
```

## *Summary*

- The VPI routines in the PLI standard provide complete access to the internal data structures of a Verilog simulation. 

- This access is done using an object oriented method, where Verilog HDL constructs within the simulation data structure are treated as objects. 
- The VPI routines use *handles* to reference these objects.
