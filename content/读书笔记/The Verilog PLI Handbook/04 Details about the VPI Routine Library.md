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

