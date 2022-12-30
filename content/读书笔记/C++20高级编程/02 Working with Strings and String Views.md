---
title: "02 Working With Strings and String Views"
date: 2022-12-17T20:26:30+08:00
draft: false
weight: 2
---

## DYNAMIC STRINGS

### C-Style Strings

- This null character is officially known as `NUL`, spelled with one `L`, not two. 
- `NUL` is not the same as the `NULL` pointer.
- The `sizeof()` operator in C and C++ can be used to get the size of a certain data type or variable. 

- If it is stored as a `char[]`, then `sizeof()` returns the actual memory used by the string, including the \0 character, as in this example:

```c++
char text1[] { "abcdef" };
size_t s1 { sizeof(text1) }; // is 7
size_t s2 { strlen(text1) }; // is 6
```

- However, if the C-style string is stored as a `char*`, then `sizeof()` returns the size of a pointer!

```c++
const char* text2 { "abcdef" };
size_t s3 { sizeof(text2) }; // is platform-dependent
size_t s4 { strlen(text2) }; // is 6
```

- A complete list of functions to operate on C-style strings can be found in the `<cstring>` header file.

### String Literals

-  String literals are actually stored in a read-only part of memory. 
- This allows the compiler to optimize memory usage by reusing references to equivalent string literals. This is called *literal pooling*.

- String literals can be *assigned* to variables, but because string literals are in a read-only part of memory and because of the possibility of literal pooling, assigning them to variables can be risky. 

```c++
char* ptr { "hello" }; 	// Assign the string literal to a variable.
ptr[1] = 'a'; 			// Undefined behavior!
```

- A much safer way to code is to use a pointer to const characters when referring to string literals. 

```c++
const char* ptr { "hello" }; 	// Assign the string literal to a variable.
ptr[1] = 'a'; 					// Error! Attempts to write to read-only memory
```

```c++
char arr[] { "hello" }; // Compiler takes care of creating appropriate sized
 						// character array arr.
arr[1] = 'a'; 			// The contents can be modified.
```

#### Raw String Literals

- *Raw string literals* are string literals that can span multiple lines of code, they don’t require escaping of embedded double quotes, and escape sequences like \t and \n are processed as normal text and not as escape sequences. 

```c++
const char* str { "Hello "World"!" }; 		// Error!
const char* str { "Hello \"World\"!" };
const char* str { R"(Hello "World"!)" };

const char* str { "Line 1\nLine 2" };
const char* str { R"(Line 1
Line 2)" };
```

- Because a raw string literal ends with )", you cannot embed a )" in your string using this syntax. 

```c++
const char* str { R"(Embedded )" characters)" }; // Error!
```

- If you need embedded )" characters, you need to use the extended raw string literal syntax, which is as follows:

```c++
R"d-char-sequence(r-char-sequence)d-char-sequence"
```

### The C++ std::string Class

#### What Is Wrong with C-Style Strings?

#### Using the string Class

- C++20 improves all this with the three-way comparison operator.

```c++
auto result { a <=> b };
if (is_lt(result)) { cout << "less" << endl; }
if (is_gt(result)) { cout << "greater" << endl; }
if (is_eq(result)) { cout << "equal" << endl; }
```

##### Memory Handling

##### Compatibility with C-Style Strings

- For compatibility, you can use the `c_str()` method on a string to get a const char pointer, representing a C-style string.

- However, the returned const pointer becomes invalid whenever the string has to perform any memory reallocation or when the string object is destroyed. 

##### Operations on strings

#### std::string Literals

- A string literal in source code is usually interpreted as a const char*. You can use the standard user defined literal s to interpret a string literal as an std::string instead.

```c++
auto string1 { "Hello World" }; 	// string1 is a const char*.
auto string2 { "Hello World"s }; 	// string2 is an std::string.
```

- The standard user-defined literal s is defined in the std::literals::string_literals namespace. 

#### CTAD with std::vector and Strings

```c++
// The deduced type will be vector<const char*>, not vector<string>!
vector names { "John", "Sam", "Joe" };

// If you want a vector<string>, then use std::string literals as explained in the previous section.
vector names { "John"s, "Sam"s, "Joe"s };
```

### Numeric Conversions

- The C++ Standard Library provides both high-level and low-level numeric conversion functions.

#### High-Level Numeric Conversions

- The std namespace includes a number of helper functions, defined in `<string>`, that make it easy to convert numerical values into strings or strings into numerical values.

##### Converting to Strings

- The following functions are available to convert numerical values into strings, where *`T`* can be `(unsigned) int`, `(unsigned) long`, `(unsigned) long long`, `float`, `double`, or `long double`. 

```c++
string to_string(T val);
```

##### Converting from Strings

- In these prototypes, `str` is the string that you want to convert, `idx` is a pointer that receives the index of the first non-converted character, and base is the mathematical base that should be used during conversion. 
- The `idx` pointer can be a null pointer, in which case it will be ignored. 
- These functions ignore leading whitespace, throw `invalid_argument` if no conversion could be performed, and throw `out_of_range` if the converted value is outside the range of the return type.

```c++
int stoi(const string& str, size_t *idx=0, int base=10);
long stol(const string& str, size_t *idx=0, int base=10);
unsigned long stoul(const string& str, size_t *idx=0, int base=10);
long long stoll(const string& str, size_t *idx=0, int base=10);
unsigned long long stoull(const string& str, size_t *idx=0, int base=10);
float stof(const string& str, size_t *idx=0);
double stod(const string& str, size_t *idx=0);
long double stold(const string& str, size_t *idx=0);
```

- A base of 10, the default, assumes the usual decimal numbers, `0–9`, while a base of 16 assumes hexadecimal numbers. 

- If the base is set to 0, the function automatically figures out the base of the given number as follows:

  ➤ If the number starts with 0x or 0X, it is parsed as a hexadecimal number.

  ➤ If the number starts with 0, it is parsed as an octal number.

  ➤ Otherwise, it is parsed as a decimal number.

#### Low-Level Numeric Conversions

- The standard also provides a number of lower-level numerical conversion functions, all defined in `<charconv>`.

##### Converting to Strings

- For converting integers to characters, the following set of functions is available:

```c++
to_chars_result to_chars(char* first, char* last, IntegerT value, int base = 10);
```

- Here, *`IntegerT`* can be any signed or unsigned integer type or char. The result is of type `to_chars_result`, a type defined as follows:

```c++
struct to_chars_result {
 	char* ptr;
 	errc ec;
};
```

