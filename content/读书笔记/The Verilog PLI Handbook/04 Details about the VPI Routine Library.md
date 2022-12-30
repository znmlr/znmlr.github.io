---
title: "04 Details About the VPI Routine Library"
date: 2022-10-29T22:16:59+08:00
draft: false
weight: 4
---

> The VPI routines are a library of 37 C functions that can interact with Verilog simulators.

## *PLI application performance considerations*

- However, a poorly thought out PLI application can actually decrease the run-time performance of a simulation. 
- The following guidelines can help in planning an efficient PLI application:

> - Good C programming practices are essential. 
> - Consider every call to a VPI routine in the VPI library as expensive, and try to minimize the number of calls.
> - VPI routines which obtain object handles using an object’s name are less efficient than VPI routines which obtain object handles based on a relationship to another object.
> - Routines which convert logic values from a simulator’s internal representation to C strings, and vice-versa, are less efficient than using other C data types. Strings are a convenient means of representing 4-state values for printing, but strings should be used prudently.
> - When the same object must be accessed many times during a simulation, the handle can be obtained once and saved in an application-allocated storage area. Using a pointer to the storage area, a PLI application has immediate access to the object handle, without having to call a VPI routine to obtain the handle each time it is needed. 
> - Use the VPI library to access the unique abilities of hardware description languages, such as representing hardware parallelism and hardware propagation times.Simulator vendors have invested a great deal in optimizing a simulator’s algorithms, and that optimization should be utilized, rather than duplicated in a PLI application.

## *The VPI string buffer*

- A number of VPI objects have properties which are strings, such as the name of a net.The routine vpi_get_str () is used to read the value of string properties. This routine returns a pointer to C a character string. The string itself is stored in a temporary string buffer. The buffer will be either freed by the simulator or and may be overwritten by the next call to vpi_get_str(). Therefore, a PLI application should use the string pointer returned by a VPI routine immediately. If a string needs to be preserved, the PLI application should copy the string into its own storage space. 

```c
// Read a string and use it immediately:
PLI_BYTE8 *string_p; 	/* string pointer only, no storage 	*/
string_p = vpi_get_str(vpiName, net_handle);
vpi_printf(“string_p points to %s\n”, string_p);

// Read a string and copy it to application-allocated storage for later use:
PLI_BYTE8 *string_p;	/* string pointer only, no storage 	*/
char *string_keep;		/* another string pointer only 		*/

string_p = vpi_get_str(vpiName, net_handle);
string_keep = malloc(strlen((char *)string_p)+1);
strcpy(string, (char *)string_p); /* save string */
```

## *VPI error handling*

A well written PLI application will perform error checking on the values returned by VPI routines. 

```c
task_handle = vpi_handle(vpiSystfCall, NULL)
if (task_handle = = NULL) {
    vpi_printf(“ERROR: could not obtain task handle\n”);
    return(0);
}
```

Routines which return integer or boolean values will return **0** if an error occurs. Routines which return double-precision values will return **0.0**. Routines which return handles will return NULL. Routines which return string pointer will return NULL (note that NULL is not the same a null string).

For VPI routines which return integer, boolean or double values, the exception value could be a legitimate value. Therefore, it might not be possible to determine if an error occurred based on the exception return value. 

The VPI library provides a useful routine called **vpi_chk_error()**, which is used to check for errors and to report detailed information about an error. This routine returns **0** if the previous call to a VPI routine was successful, and an error severity level code if the call resulted in an error.

```c
PLI_INT32 vpi_chk_error (
	p_vpi_error_info info) 	/* 	pointer to an application-allocated s_vpi_error_info
								structure, or NULL */
```

Every VPI routine except vpi_chk_error() will set or clear an internal VPI error status flag, which is common to all VPI routines. When the flag is set by an error, it will remain set until the next call to a VPI routine changes the flag. vpi_chk_error() only reads the error status flag, and does not modify it.

The input to vpi_chk_error() is a pointer to an **s**_**vpi_error_info** structure. If an error in the previous call to VPI routine occurred, vpi_chk_error() will fill in

the fields of this structure with the simulator product name and version, and the file name and line number containing the system task/function instance which called the PLI application.

```c
typedef struct t_vpi_error_info {
    PLI_INT32 state; /* vpiCompile, vpiPLI, vpiRun 	*/
    PLI_INT32 level; /* vpiNotice, vpiWarning, vpiError,
    					vpiSystem, vpiInternal 		*/
    PLI_BYTE8 *message;
    PLI_BYTE8 *product;
    PLI_BYTE8 *code;
    PLI_BYTE8 *file;
    PLI_INT32 line;
} s_vpi_error_info, *p_vpi_error_info;
```

However, excessive use of this routine can degrade the run-time performance of simulation. 

```c
#define PLIbookDebug 1		/* set to 0 to omit debug messages 	*/
#if PLIbookDebug
	s_vpi_error_info err;	/* allocate a VPI error structure 	*/
#endif

primitive_handle = vpi_handle(vpiPrimitive, NULL);
#if PLIbookDebug 			/* if error, generate verbose debug message */
if (vpi_chk_error(&err)) {
    vpi_printf(“\Run time error in $list_nets PLI application: \n”);
    vpi_printf(“ Product: %s Code: %s\n”, err.product, err.code);
    vpi_printf(“ Message: %s\n”, err.message);
    if (err.file != NULL)
    	vpi_printf(“ File: %s Line: %d\n\n”, err.file, err.line);
}
#else /* if error, generate basic error message */
if (primitive_handle == NULL)
	vpi_printf(“\nERROR: could not obtain primitive handle\n”);
#endif
```

## *VPI object diagrams*

The IEEE 1364 PLI standard includes an **object diagram** for each object which VPI routines can access. These object diagrams document:

- The **properties** of the object. For example, a net object has *name, vector size,* and *logic value* properties (as well as several other properties).

- The **relationships** of the object. Relationships indicate how an object is connected to or contained within other objects within a Verilog data structure. For example, a net is contained within a module, and may also be connected to other objects, such as a module port or primitive terminal.

The object diagrams use enclosures and arrows. The type of object is listed within each enclosure, and the relationships to other objects are shown as arrows between the enclosures. 

 ![image-20221029225624167](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221029225624167.png)

### **Object diagram symbols**

### **Traversing object relationships**

> 我觉得VPI object diagrams用不到，暂不阅读

## *Obtaining handles for objects*

### **Traversing one-to-one relationships**

**vpi_handle ()** returns a handle for a target object which has a one-to-one relation ship to a reference object. The routine is passed in two inputs:

```c
vpiHandle vpi_handle (
    PLI_INT32 type,			/* constant representing an object type */
    vpiHandle reference)	/* handle for an object 				*/
```

### **Traversing one-to-many relationships**

Many objects in Verilog have a one-to-many relationship with other objects. A 2-step process is used to traverse these types of relationships.

- Obtain a handle for an **iterator object** for the desired target objects.

- Process each object referenced by the iterator object, one-by-one.

**vpi_iterate()** sets up an iterator object which represents the first of the many target objects, and returns a handle for the iterator. If there are no target objects in the Verilog data structure, then vpi_iterate() will return **NULL**. This routine is passed in two inputs:

```c
vpiHandle vpi_iterate (
    PLI_INT32 type,			/* constant representing an object type */
    vpiHandle reference)	/* handle for an object 				*/
```

**vpi_scan()** returns a handle for each target object referenced by the iterator object. The routine is passed in a single input—the handle for the iterator:

```c
vpiHandle vpi_scan (
	vpiHandle Iterator) 	/* handle for an iterator object 		*/
```

vpi_scan () returns the next target handle referenced by the iterator each time it is called. Therefore, the routine must be called repeatedly (typically using a loop) in order to access all of the target objects. When vpi_scan () has returned all objects referenced by the iterator, it will return **NULL** the next time it is called. The NULL return can be used as a flag to exit the loop.

Generally, the memory required for an iterator object is automatically maintained by the simulator. The vpi_iterate() routine will allocate the memory needed for the iterator, and vpi_scan() will automatically free the memory when it returns NULL (which indicates there are no more target objects referenced by the iterator). This automatic memory management relieves the PLI application developer of the need to allocate and de-allocate memory for the iterator object.

### **When to use vpi_free_object() on iterator handles**

Occasionally, a PLI application might call vpi_iterate() to set up an iterator object, but then the application does not call vpi_scan() at all, or does not call vpi_scan() until the routine returns NULL. In this circumstance, the memory allocated by vpi_iterate() will not be de-allocated automatically. 

In order to prevent a memory leak in a PLI application, the application must manually free the iterator object memory by calling the routine **vpi_free_object().** The vpi_free_object() routine returns 1 (for true) if successful, and 0 (for false) if unsuccessful. The syntax for this routine is:

```c
PLI_INT32 vpi_free_object (
	vpiHandle handle) /* handle for an object */
```

It is a good practice to always check that the last call to vpi_scan() did not return NULL before calling vpi_free_object() on an iterator handle. 

### **Obtaining intermodule path object handles**

- In the Verilog language, the output port of one module can be connected to one or more input ports of other modules, using a net data type. The connection from an out put to an input is referred to as an **intermodule path.** 

- In actual hardware, this inter connection will have a real delay, but, within the Verilog language, there is no construct to accurately represent that delay.
-  The PLI, however, can add, read and modify intermodule path delays. A module input port can be driven by any number of module output ports. 

**vpi_handle_multi()** is used to obtain a handle for an intermodule path. Other VPI routines can then annotate delays to the path. This routine requires three inputs:

```c
vpiHandle vpi_handle_multi (
    PLI_INT32 type,			/* constant of vpiInterModPath 			*/
    vpiHandle reference1,	/* handle for an output or inout port 	*/
    vpiHandle reference2)	/* handle for an input or inout port 	*/
```

The constant **vpiInterModPath** is the only type constant supported by vpi_handle_multi ( ). The ports specified must be the same vector size, but they

do not need to be in the same level of Verilog hierarchy. If no interconnecting net exists between the two ports, then vpi_handle_multi( ) will return NULL. An example of using this routine is:

```c
inter_mod_path_h = vpi_handle_multi(vpiInterModPath, 
                                    in_port_handle, 
                                    out_port_handle);
if (inter_mod_path_h != NULL)
	/* inter connection path not found -- process an error 	*/
else
	/* read or modify the inter-connect delay values 		*/
```

### **Obtaining object handles using an object’s name**

**vpi_handle_by_name()** obtains a handle for an object using the name of the object. The handle for any Verilog object with a vpiFullName property in the object diagrams can be obtained using this routine. The routine requires two inputs:

```c
vpiHandle vpi_handle_by_name (
    PLI_BYTE8 *name,	/* name of an object */
    vpiHandle scope)	/* handle for a scope object, or **NULL** */
```

The name provided can be the local name of the object, a relative hierarchical path name, or a full hierarchical path name. If a name without a full hierarchy path is specified, the routine will only search for the object in the scope specified. If a NULL is specified for the scope handle, the object will be searched for in the first top level module found by the routine. If the object cannot be found, then vpi_handle_by_name() will return NULL.

vpi_handle_by_name() is an expensive routine in terms of simulation performance, and should be used judiciously. It is much more efficient to obtain a handle for an object based on its relationship to some other object.

### **Obtaining object handles using an object’s index number**

**vpi_handle_by_index()** is used to obtain a handle for an object using the object’s index position. This routine requires two inputs:

```c
vpiHandle vpi_handle_by_index (
    vpiHandle parent,	/* handle for an object with a vpiIndex relationship */
    PLI_INT32 index )	/* index number of an object */
```

- If an index is out of range, a NULL is returned. 
- Note that vpi_handle_by_index() requires the object have an index *relationship.* Some Verilog objects have an index *property,* which is not the same as an index relation ship. 

### **Obtaining handles for reg, variable and net arrays**

The following statement in the Verilog HDL declares a 3-dimensional array of 16-bit wide nets (each element in the array is 16 bits wide):

```verilog
wire [15:0] foo [0:127][0:127] [0:7] ; // 3-D array
```

Examples of a word-select and a bit-select within the preceding array are:

```verilog
vector = foo[25][0][100]; //select full word from array
bit = foo[25][0][100][5]; //select bit 5 from an array word
```

A handle to a multi-dimensional array of nets, regs or named events can be obtained in several ways using the VPI library:

- Pass the name of the array as a task/function argument.

- Iterate on all net, reg or named event array objects, for example using vpi_iterate(vpiNetArray, module_handle).

- Iterate on all memory array objects using vpi_iterate(vpiMemory, module_or_scope_handle); note that this will only obtain one-dimensional reg arrays, and not reg arrays with more than one dimension.

A handle to a word within an array can be obtained:

- As a handle to an expression, when a word-select from an array is used in a Verilog expression.

- With a handle to an array with any number of dimensions, iterate on each word within the array.

- Directly access a specific word by its index in a one-dimensional reg array, using vpi_handle_by_index(memory_handle, index_number).

- Directly access a specific word by its index in a multi-dimensional array of any type, using vpi_handle_by_multi_index(array_handle, array_size, index_array).

**vpi_handle_by_multi_index()** is used to obtain a handle for a word within an array, or bit-select of a word out of an array object. This routine was added with the IEEE 1364-2001 standard. The routine requires three inputs:

```c
vpiHandle vpi_handle_by_multi_index (
    vpiHandle object,			/* handle for an array object 			*/
    PLI_INT32 array_size,		/* number or elements in the index array*/
    PLI_INT32 * index_array)	/* pointer to an array of indices 		*/
```

The following statement in the Verilog HDL declares a 3-dimensional array of 16-bit wide nets (each element in the array is 16 bits wide):

```verilog
wire [15:0] foo [0:127][0:127][0:7]; // 3-D array
```

Assuming a handle for the array had already been obtained, the following example would obtain a handle for a specific 16-bit net within the array, specifically `foo[25][0][100]`:

```c
vpiHandle array_handle, net_handle;
PLI_INT32 indices[10]; /* up to a 10-dimensional array */

/* add code to obtain handle for the array */
indices[0] = 25; indices[1] = 0; indices[2] = 100;
net_handle = vpi_handle_by_multi_index(array_handle, 3, indices);
```

#### Variable arrays

A object is represented a differently than a reg array, net array or named event array. A variables object may represent a single variable or it may be an

array of variables (whereas a net, reg or named event object is always a single object, and never an array).

A handle for a variable or variable array is obtained the same way, by using vpi_iterate (vpiVariables, module_or_scope_handle). Once the handle is obtained, the boolean property **vpiArray** is used to determine if a variable object is an array.

- If the **vpiArray** property is false, then the variable object is a single variable. The **vpiSize** property will be the number of bits in the variable, and the expressions accessed by **vpiLeftRange** and **vpiRightRange** will indicate the most-significant and least-significant bit numbers, respectively.

- If the **vpiArray** property is true, then the variable object is an array of variables. The**vpiSize** property will be the number of elements in the array, and the expressions accessed by**vpiLeftRange** and **vpiRightRange** will indicate the first address and last address of the array, respectively.

### **System task/function arguments**

A user-defined system task or system function can have any number of arguments, including none. The VPI standard does not specify an index number for task/function arguments, but the TF and ACC libraries number the arguments from left to right, starting with 1. For convenience in describing PLI applications, this book uses the same numbering scheme in the VPI chapters. In the following example:

 ![image-20221030102510627](https://nas.znmlr.cn:15900/markdown/2022/10/image-20221030102510627.png)

### **Multiple instances of system tasks and system functions**

Each instance of a system task/function is unique, and has unique argument values. However, each instance is associated with the same *calltf routine.* For example:

```c
always @(posedge clock)
	$read_test_vector(“A.dat”, data_bus);
always @(negedge clock)
	$read_test_vector(“B.dat”, data_bus);
```

### **Obtaining a handle for a system task/function instance**

An instance of a system task or system function is an object, and the VPI routines can obtain a handle for this object. This handle will be unique for each instance of the system task/function. 

### **Accessing the arguments of system tasks and system functions**

Once a handle for an instance of a system task or system function is obtained, the arguments to the system task/function can be accessed by obtaining handles for the arguments. In the Verilog HDL, many different values and data types can be used as a task/function argument—an integer number, a variable name, a net name, a module instance name, or a literal string are just a few of the legal arguments. 

```c
int PLIbook_count_args_vpi()
{
    vpiHandle systf_h, arg_itr, arg_h;
    int tfnum = 0;
    s_vpi_error_info err; /* structure for error handling */
    
    systf_h = vpi_handle(vpiSysTfCall, NULL);
#if PLIbookDebug /* if error, generate verbose debug message */
    if (vpi_chk_error(&err)) {
    	vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain handle to systf call\n");
    	vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
    }
#else /* if error, generate brief error message */
    if (systf_h == NULL)
    	vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain handle to systf call\n");
#endif
    arg_itr = vpi_iterate(vpiArgument, systf_h);
#if PLIbookDebug /* if error, generate verbose debug message */
    if (vpi_chk_error(&err)) {
    	vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain iterator to systf args\n");
    	vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
    }
#else /* if error, generate brief error message */
    if (arg_itr == NULL)
    	vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain iterator to systf args\n");
#endif
    while (arg_h = vpi_scan(arg_itr) ) {
    	tfnum++;
    }
    return(tfnum);
}
```

```c
vpiHandle PLIbook_get_arg_handle_vpi(int argNum)
{
	vpiHandle systf_h, arg_itr, arg_h;
	int i;
	s_vpi_error_info err; /* structure for error handling */

    if (argNum < 1) {
#if PLIbookDebug /* if error, generate verbose debug message */
		vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() arg index of %d is invalid\n", argNum);
#endif
		return(NULL);
	}
    
	systf_h = vpi_handle(vpiSysTfCall, NULL);
#if PLIbookDebug /* if error, generate verbose debug message */
	if (vpi_chk_error(&err)) {
		vpi_printf( "ERROR: PLIbook_get_arg_handle_vpi () could not obtain handle to systf call\n");
        vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
	}
#else /* if error, generate brief error message */
	if (systf_h == NULL) {
		vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain handle to systf call\n");
		return(NULL);
	}
#endif

    arg_itr = vpi_iterate(vpiArgument, systf_h);
#if PLIbookDebug /* if error, generate verbose debug message */
	if (vpi_chk_error(&err)) {
		vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain iterator to systf args\n");
		vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
	}
#else /* if error, generate brief error message */
	if (systf_h == NULL) {
		vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain iterator to systf args\n");
		return(NULL);
	}
#endif
	for (i=1; i<=argNum; i++) {
		arg_h = vpi_scan(arg_itr);
#if PLIbookDebug /* if error, generate verbose debug message */
        if (vpi_chk_error(&err)) {
        	vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain handle to systf arg %d\n", i);
        	vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
        }
#endif
		if (arg_h == NULL) {
#if PLIbookDebug /* if error, generate verbose debug message */
			vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() arg index of %d is out-of-range\n", argNum);
#endif
			return(NULL);
		}
	}
	if (arg_h != NULL)
		vpi_free_object(arg_itr); /* free iterator--didn’t scan all args */
	return(arg_h);
}
```

## *Storing data for each instance of a system task/junction*

- There are many circumstances where a PLI application may need to preserve information from one call to a PLI application to another call to the same application. 
- In order to store the system task/function arguments, unique storage must be allocated for each instance of a system task or function

- A PLI application is a C function, which is called by the Verilog simulator. Local variables within a C function are automatic, which means any variables (such as an array to store the argument handles) do not remain allocated from one call of the function to another call.

- A common solution in the C programming language to preserve data is to declare a static variables, instead of automatic variables. Another method is to use global vari ables instead of local variables. **These C programming techniques can cause serious problems in PLI applications!** 

- The Verilog HDL allows a system task/function to be used multiple times in the Verilog source code, and each module which uses the task/function can be instantiated multiple times. Each occurrence in each instance of a module becomes a unique **instance** of the system task/function. However, in the PLI application, the same C function will be called by the simulator for each instance. A static or global variable cannot hold different values for each instance of the system task/function. 

- **Using static or global vari ables is a sure way to have problems when there are multiple instances of a system task or system function.** Therefore, a PLI application must allocate storage that is unique to each instance of a system task/function.

- The VPI standard provides a special storage location for each instance of a system task or system function. This instance-specific storage is allocated automatically by the simulator, and is available for use by a PLI application whenever needed. Special VPI routines are provided to read and write values in the instance-specific storage area. The storage area is shared by all routines which are associated with the systemtask/function, which are the *calltf, compiletf* and *sizetf routines.*

```c
PLI_INT32 vpi_put_userdata (
    vpiHandle tfcall,	/*handle for a system task or system function call 	*/
    void *data)			/*pointer to application-allocated storage 			*/

void *vpi_get_userdata (
	vpiHandle tfcall) 	/*handle for a system task or system function call	*/
```

- vpi_put_userdata () stores a pointer to application-allocated storage into simulator-allocated storage for an instance of a system task or function. The routine returns 1 if successful and 0 if an error occurred. The simulation-allocated storage will persist throughout simulation. vpi_get_userdata () retrieves a pointer to the data that was stored using vpi_put_userdata(). The routine returns NULL if no data has been stored.

### **Storing a single value in the VPI instance-specific storage area**

- The instance-specific storage area is defined to be a pointer, which can store a single value. The value to be stored should be cast to a void pointer. An example of storing a single integer value in the work area is:

```c
int arg_count;
/* add code to count number of task/function arguments */
vpi_put_userdata(systf_handle, (void *)arg_count);
```

### **Storing multiple values in the VPI instance-specific storage area**

- Multiple values can be stored by allocating a block of memory and storing a pointer to the memory in the storage area.

```verilog
always @(posedge clock)
	$ALU(a_bus, b_bus, opcode, result_bus, overflow);
	
always @(negedge clock)
	$ALU(in1, in2, control, out1);
```

- The first time a PLI application for one of the instances of $ALU calls either *PLIbook_count_args_vpi()* or *PLIbook_get_arg_handle_vpi(),* the function can allocate an array to store both the count and all the handles to the task/function arguments. A pointer to the array can be stored in the instance-specific storage area for that system task/function instance.

```c
vpiHandle *arg_array; /* array pointer */

/* count number of task/function arguments */
arg_array = (vpiHandle *)malloc(sizeof(vpiHandle)*(args+1));

/* put argument count into arg_array[0] */
/* fill rest of array with argument handles */

vpi_put_userdata(systf_h, (void *)arg_array);
```

- Example shows a more efficient version of the *PLIbook_count_args_vpi()* and *PLIbook_get_arg_handle_vpi()* applications. The first time either of these functions is called, it will call a sub function to allocate an array, save the argument count and argument handles, and save a pointer to the array in the instance-specific storage area. Since the storage is associated with the system task/function instance, both *PLIbook_count_args_vpi()* and *PLIbook_get_arg_handle_vpi()* will have access to the pointer stored in the storage area.

```c
/****************************************************************/
/* PLIbook_count_args_vpi() -- Efficient Version				*/
/****************************************************************/ 
int PLIbook_count_args_vpi()
{
    vpiHandle systf_h, arg_itr, arg_h;
    int tfnum = 0;
    vpiHandle *arg_array; /* array pointer to store arg handles */
#if PLIbookDebug
	s_vpi_error_info err; /* structure for error handling */
#endif
	systf_h = vpi_handle(vpiSysTfCall, NULL);
#if PLIbookDebug /* if error, generate verbose debug message */
    if (vpi_chk_error(&err)) {
        vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain handle to systf call\n");
        vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
    }
#else /* if error, generate brief error message */
    if (systf_h == NULL)
    	vpi_printf("ERROR: PLIbook_count_args_vpi() could not obtain handle to systf call\n");
#endif

    /* retrieve pointer to array with all argument handles */
	arg_array = (vpiHandle *)vpi_get_userdata(systf_h);
	if (arg_array == NULL) {
		/* array with all argument handles doesn’t exist, create it */
		arg_array = create_arg_array(systf_h);
	}
	return((int)arg_array[0]);
}
/****************************************************************/
/* PLIbook_get_arg_handle_vpi() -- Efficient Version			*/
/****************************************************************/ 
vpiHandle PLIbook_get_arg_handle_vpi(int argNum)
{
	vpiHandle systf_h, arg_h;
	vpiHandle *arg_array; /* array pointer to store arg handles */
#if PLIbookDebug
	s_vpi_error_info err; /* structure for error handling */
#endif
    if (argNum < 1) {
#if PLIbookDebug /* if error, generate verbose debug message */
        vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() arg index of %d is invalid\n", argNum);
#endif
	    return(NULL);
    }
	
    systf_h = vpi_handle(vpiSysTfCall, NULL);
#if PLIbookDebug /* if error, generate verbose debug message */
    if (vpi_chk_error(&err)) {
        vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain handle to systf call\n");
        vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
    }
#else /* if error, generate brief error message */
    if (systf_h == NULL) {
        vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain handle to systf call\n");
        return(NULL);
    }
#endif

    /* retrieve pointer to array with all argument handles */
	arg_array = (vpiHandle *)vpi_get_userdata(systf_h);
    if (arg_array == NULL) {
        /* array with all argument handles doesn’t exist, create it */
        arg_array = create_arg_array(systf_h);
    }
	if (argNum > (int)arg_array[0]) {
#if PLIbookDebug /* if error, generate verbose debug message */
    	vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() arg index of %d is out-of-range\n", argNum);
#endif
		return(NULL);
	}

    /* get requested tfarg handle from array */
    arg_h = (vpiHandle)arg_array[argNum];
    return (arg_h);
}
/****************************************************************/
/* Subroutine to allocate an array and store the number of 		*/
/*	arguments and all argument handles in the array.			*/
/****************************************************************/            
vpiHandle *create_arg_array(vpiHandle systf_h)
{
    vpiHandle arg_itr, arg_h;
    vpiHandle *arg_array; /* array pointer to store arg handles */
    int i, tfnum = 0;
#if PLIbookDebug
	s_vpi_error_info err; /* structure for error handling */
#endif

    /* allocate array based on the number of task/function arguments */
    arg_itr = vpi_iterate(vpiArgument, systf_h);
    if (arg_itr == NULL) {
        vpi_printf("ERROR: PLIbook_numargs_vpi() could not obtain iterator to systf args\n");
        return(NULL);
    }
    
    while (arg_h = vpi_scan(arg_itr) ) { /* count number of args */
    	tfnum++;
    }

    arg_array = (vpiHandle *)malloc(sizeof(vpiHandle) * (tfnum +1));
    /* store pointer to array in simulator-allocated user_data storage that is unique for each task/func instance */
	vpi_put_userdata(systf_h, (void *)arg_array);
	
    /* store number of arguments in first address in array */
	arg_array[0] = (vpiHandle)tfnum;

    /* fill the array with handles to each task/function argument */
	arg_itr = vpi_iterate(vpiArgument, systf_h);
#if PLIbookDebug /* if error, generate verbose debug message */
    if (vpi_chk_error(&err)) {
        vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain iterator to systf args\n");
        vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
    }
#else /* if error, generate brief error message */
    if (systf_h == NULL) {
        vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain iterator to systf args\n");
        return(NULL);
    }
#endif

    for (i=1; i<=tfnum; i++) {
		arg_h = vpi_scan(arg_itr);
#if PLIbookDebug /* if error, generate verbose debug message */
        if (vpi_chk_error(&err)) {
            vpi_printf("ERROR: PLIbook_get_arg_handle_vpi() could not obtain handle to systf arg %d\n", i);
            vpi_printf("File %s, Line %d: %s\n", err.file, err.line, err.message);
        }
#endif
		arg_array[i] = arg_h;
	}

    if (arg_h != NULL)
		vpi_free_object(arg_itr); /* free iterator--didn’t scan all args */
	return(arg_array);
}
```

