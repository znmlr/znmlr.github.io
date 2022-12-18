---
title: "01 a Crash Course in C++ and the Standard Library"
date: 2022-12-17T20:24:10+08:00
draft: false
weight: 1
---

## Namespace

### Nested Namespace

```c++
namespace MyLibraries::Networking::FTP 
{
     /* ... */
}
```

- This compact syntax was not available before C++17 and you had to resort to the following:

```c++
namespace MyLibraries {
	namespace Networking {
    	namespace FTP {
 			/* ... */
 		}
 	}
}
```

### Namespace Alias

- A *namespace alias* can be used to give a new and possibly shorter name to another namespace. Here’s an example:

```c++
namespace MyFTP = MyLibraries::Networking::FTP;
```

## Literals

- It is also possible to define your own type of literals
- Digits separators can be used in numeric literals. A digits separator is a single quote character.

```c++
23'456'789
0.123'456f
```

### Numerical Limits

- In C, you could access `#defines`, such as `INT_MAX`.
- In C++, it’s recommended to use the `std::numeric_limits` class template defined in`<limits>`

```c++
cout << "int:\n";
cout << format("Max int value: {}\n", numeric_limits<int>::max());
cout << format("Min int value: {}\n", numeric_limits<int>::min());
cout << format("Lowest int value: {}\n", numeric_limits<int>::lowest());
cout << "\ndouble:\n";
cout << format("Max double value: {}\n", numeric_limits<double>::max());
cout << format("Min double value: {}\n", numeric_limits<double>::min());
cout << format("Lowest double value: {}\n", numeric_limits<double>::lowest());
```

```shell
int:
Max int value: 2147483647
Min int value: -2147483648
Lowest int value: -2147483648
double:
Max double value: 1.79769e+308
Min double value: 2.22507e-308
Lowest double value: -1.79769e+308
```

- Note the differences between `min()` and `lowest()`. For an integer, the minimum value equals the lowest value. However, for floating-point types, the minimum value is the smallest positive value that can be represented, while the lowest value is the most negative value representable, which equals `-max()`.

### Zero Initialization

- Zero initialization initializes primitive integer types (such as char, int, and so on) to zero, primitive floating-point types to 0.0,  pointer types to `nullptr`, and constructs objects with the default constructor (discussed later).

```c++
float myFloat {};
int myInt {};
```

### Casting

- C++ provides three ways to *explicitly* change the type of a variable.

```c++
float myFloat { 3.14f };
int i1 { (int)myFloat }; // method 1
int i2 { int(myFloat) }; // method 2
int i3 { static_cast<int>(myFloat) }; // method 3
```

### Floating-Point Numbers

- To check whether a given floating-point number is not-a-number, use `std::isnan()`. To check for infinity, use `std::isinf()`. Both functions are defined in `<cmath>`.

- To obtain one of these special floating-point values, use numeric_limits, for example `numeric_limits<double>::infinity`.

## Enumerated Types

- By default, the underlying type of an enumeration value is an integer, but this can be changed as follows:

```c++
enum class PieceType : unsigned long
{
    King = 1,
    Queen,
    Rook = 10,
    Pawn
};
```

- Starting with C++20, you can use a `using enum` declaration to avoid having to fully qualify enumeration values. Here’s an example:

```C++
using enum PieceType;
PieceType piece { King };
```

## Structs

## Conditional Statements

### Initializers for if Statements

- C++ allows you to include an initializer inside an if statement using the following syntax:

```c++
if (<initializer>; <conditional_expression>) {
 	<if_body>
} else if (<else_if_expression>) {
 	<else_if_body>
} else {
 	<else_body>
}
```

- Any variable introduced in the `<initializer>` is available only in the `<conditional_expression>`,  in the `<if_body>`, in all `<else_if_expression>`s and `<else_if_body>`s, and in the `<else_body>`.

### switch Statements

- This code snippet also shows a nice example of using a properly scoped `using enum` declaration to avoid having to write `Mode::Custom`, 

  `Mode::Standard`, and `Mode::Default` for the different case labels.

```c++
enum class Mode { Default, Custom, Standard };

int value { 42 };
Mode mode { /* ... */ };
switch (mode) {
 	using enum Mode;
 	case Custom:
 		value = 84;
 	case Standard:
 	case Default:
 		// Do something with value ...
 	break;
}
```

- To prevent this warning, you can tell the compiler that a `fallthrough` is intentional using the `[[fallthrough]] `attribute as follows:

```c++
switch (mode) {
 	using enum Mode;
 	case Custom:
 		value = 84;
 		[[fallthrough]];
 	case Standard:
 	case Default:
 		// Do something with value ...
 	break;
}
```

### Initializers for switch Statements

- Just as for if statements, you can use initializers with switch statements. The syntax is as follows:

```c++
switch (<initializer>; <expression>) { <body> }
```

- Any variables introduced in the `<initializer>` are available only in the `<expression>` and in the` <body>`. They are not available outside the switch statement.

## Logical Evaluation Operators

### Three-Way Comparisons

- The *three-way comparison operator* can be used to determine the order of two values. 
- With a single expression, it tells you whether a value is equal, less than, or greater than another value. 
- If the operands are integral types, the result is a so-called *strong ordering* and can be one of the following:

```python
strong_ordering::less: First operand less than second
strong_ordering::greater: First operand greater than second
strong_ordering::equal: Equal operands
```

- If the operands are floating-point types, the result is a *partial ordering*:

```
partial_ordering::less: First operand less than second
partial_ordering::greater: First operand greater than second
partial_ordering::equivalent: Equal operands
partial_ordering::unordered: If one or both of the operands is not-a-number
```

```c++
int i { 11 };
std::strong_ordering result { i <=> 0 };
if (result == std::strong_ordering::less) { std::cout << "less" << std::endl; }
if (result == std::strong_ordering::greater) { std::cout << "greater" << std::endl; }
if (result == std::strong_ordering::equal) { std::cout << "equal" << std::endl; }
```

- There is also a *weak ordering*, which is an additional ordering type that you can choose from to implement three-way comparisons for your own types.

```
weak_ordering::less: First operand less than second
weak_ordering::greater: First operand greater than second
weak_ordering::equivalent: Equal operands
```

- Finally, `<compare>` provides *named comparison functions* to interpret the result of an ordering. These functions are `std::is_eq()`, `is_neq()`, `is_lt()`, `is_lteq()`, `is_gt()`, and `is_gteq()`returning true if an ordering represents ==, !=, <, <=, >, or >= respectively, false otherwise. Here is an example:

## Functions

### Function Return Type Deduction

- You can ask the compiler to figure out the return type of a function automatically. To make use of this functionality, just specify auto as the return type.

```c++
auto addNumbers(int number1, int number2)
{
     return number1 + number2;
}
```

- There can be multiple return statements, but they must all resolve to the same type. 
- Such a function can even include recursive calls (calls to itself), but the first return statement in the function must be a non-recursive call.

## Attributes

- Before attributes were standardized in C++, vendors decided how to specify such information. Examples are `__attribute__`, `__declspec`, and so on. Since C++11, there is standardized support for attributes by using the double square brackets syntax `[[attribute]]`.

### [[nodiscard]]

- The `[[nodiscard]]` attribute can be used on a function returning a value to let the compiler issue a warning when that function is called without doing something with the returned value. Here is an example:

```
[[nodiscard]] int func()
{
	return 42;
}
int main()
{
	func();
}
```

- More general, the `[[nodiscard]]` attribute can be used on classes, functions, and enumerations.

- Starting with C++20, a reason can be provided for the `[[nodiscard]] `attribute in the form of a string, for example:

```c++
[[nodiscard("Some explanation")]] int func();
```

### [[maybe_unused]]

- The `[[maybe_unused]]` attribute can be used to suppress the compiler from issuing a warning when something is unused, as in this example:

```c++
int func(int param1, int param2)
{
	return 42;
}
```

- If the compiler warning level is set high enough, this function definition might result in two compiler warnings. 
- By using the `[[maybe_unused]]` attribute, you can suppress such warnings:

```c++
int func(int param1, [[maybe_unused]] int param2)
{
	return 42;
}
```

- The [[maybe_unused]] attribute can be used on classes and structs, non-static data members, unions, typedefs, type aliases, variables, functions, enumerations, and enumeration values. 

### [[noreturn]]

- Adding a `[[noreturn]]` attribute to a function means that it never returns control to the call site.

- With this attribute, the compiler can avoid giving certain warnings or errors because it now knows more about the intent of the function. Here is an example:

```c++
[[noreturn]] void forceProgramTermination()
{
	std::exit(1); // Defined in <cstdlib>
}
bool isDongleAvailable()
{
	bool isAvailable { false };
 	// Check whether a licensing dongle is available...
 	return isAvailable;
}
bool isFeatureLicensed(int featureId)
{
 	if (!isDongleAvailable()) {
 		// No licensing dongle found, abort program execution!
 		forceProgramTermination();
 	} else {
 		bool isLicensed { featureId == 42 };
 		// Dongle available, perform license check of the given feature...
 		return isLicensed;
 	}
}
int main()
{
 	bool isLicensed { isFeatureLicensed(42) };
}
```

### [[deprecated]]

- `[[deprecated]]` can be used to mark something as deprecated, which means you can still use it, but its use is discouraged. This attribute accepts an optional argument that can be used to explain the reason for the deprecation, as in this example:

```c++
[[deprecated("Unsafe method, please use xyz")]] void func();
```

- If you use this deprecated function, you’ll get a compilation error or warning. For example, GCC gives the following warning:

```c++
warning: 'void func()' is deprecated: Unsafe method, please use xyz
```

### [linkely] [unlikely]

- These likelihood attributes can be used to help the compiler in optimizing the code. 
- These attributes can, for example, be used to mark branches of if and switch statements according to how likely it is that a branch will be taken. 
- Note that these attributes are rarely required. 

## C-Style Arrays

- An array can be initialized with an initializer list, in which case the compiler deduces the size of the array automatically. Here’s an example:

```c++
  int myArray[] { 1, 2, 3, 4 }; // The compiler creates an array of 4 elements.
```

- If you do specify the size of the array and the initializer list has fewer elements than the given size,  the remaining elements are set to 0. 
- For example, the following code sets only the first element in the array to the value 2 and sets all others to 0:

```c++
int myArray[3] { 2 };
```

- To get the size of a stack-based C-style array, you can use the `std::size()` function (requires `<array>`). It returns a size_t, which is an unsigned integer type defined in `<cstddef>`. Here is an example:

```c++
size_t arraySize { std::size(myArray) };
```

## std::array

## std::vector

## std::pair

## std::optional

- `std::optional`, defined in `<optional>`, holds a value of a specific type, or nothing. 

- Here is an example of a function returning an optional:

```c++
optional<int> getData(bool giveIt)
{
	if (giveIt) {
 		return 42;
 	}
 	return nullopt; // or simply return {};
}
```

- You can call this function as follows:

```c++
optional<int> data1 { getData(true) };
optional<int> data2 { getData(false) };
```

- To determine whether an optional has a value, use the has_value() method, or simply use the  optional in an if statement:

```c++
cout << "data1.has_value = " << data1.has_value() << endl;
if (data2) {
 	cout << "data2 has a value." << endl;
}
```

- If an optional has a value, you can retrieve it with value() or with the dereferencing operator:

```c++
cout << "data1.value = " << data1.value() << endl;
cout << "data1.value = " << *data1 << endl;
```

- If you call `value()` on an empty optional, an `std::bad_optional_access` exception is thrown.
- `value_or()` can be used to return either the value of an optional or another value when the optional is empty:

```c++
cout << "data2.value = " << data2.value_or(0) << endl;
```

- Note that you cannot store a reference in an optional, so `optional<T&>` does not work. Instead, you can store a pointer in an optional.

## Structured Bindings

- *`Structured bindings`* allow you to declare multiple variables that are initialized with elements from, for example, an `array`, `struct`, or `pair`.

```c++
array values { 11, 22, 33 };
auto [x, y, z] { values };

struct Point { double m_x, m_y, m_z; };
Point point;
point.m_x = 1.0; point.m_y = 2.0; point.m_z = 3.0;
auto [x, y, z] { point };

pair myPair { "hello", 5 };
auto [theString, theInt] { myPair }; // Decompose using structured bindings.
cout << format("theString: {}", theString) << endl;
cout << format("theInt: {}", theInt) << endl;
```

- It is also possible to create a set of references-to-non-const or references-to-const using the structured bindings syntax, by using auto& or const auto& instead of auto. 

## Loops

- C++ provides four looping mechanisms: the while loop, do/while loop, for loop, and *range-based* for loop.

### The Range-Based for Loop

-  It allows for easy iteration over elements of a container. This type of loop works for C-style arrays, initializer lists , and any type that has `begin()` and `end()` methods returning `iterators`, such as `std::array`, `vector`, and all other Standard Library containers.

#### Initializers for Range-Based for Loops

- Starting with C++20, you can use initializers with range-based for loops, similar to initializers for if and switch statements. The syntax is as follows:

```c++
for (<initializer>; <for-range-declaration> : <for-range-initializer>) 
{ 
    <body> 
}
```

- Any variables introduced in the `<initializer>` are available only in the `<for-range-initializer>` and in the `<body>`. They are not available outside the range-based for loop. Here is an example:

```c++
for (array arr { 1, 2, 3, 4 }; int i : arr) { cout << i << endl; }
```

## Initializer Lists

- Initializer lists are defined in <initializer_list> and make it easy to write functions that can accept a variable number of arguments. 
- Initializer lists are type safe. All elements in such a list must be of the same type.

## Uniform Initialization

- A benefit of using uniform initialization is that it prevents *narrowing*. When using the old-style assignment syntax to initialize variables, C++ implicitly performs narrowing, as shown here:

```c++
void func(int i) { /* ... */ }
int main()
{
 	int x = 3.14;
 	func(3.14);
}
```

- For both lines in main(), C++ automatically truncates 3.14 to 3 before assigning it to x or calling `func()`. Note that some compilers *might* issue a arning about this narrowing, while others won’t. 

- With uniform initialization, both the assignment to x and the call to func() *must* generate a compilation error if your compiler fully conforms to the C++11 standard:

```c++
int x { 3.14 }; // Error because narrowing
func({ 3.14 }); // Error because narrowing
```

- Uniform initialization can be used to initialize dynamically allocated arrays, as shown here:

```c++
int* myArray = new int[4] { 0, 1, 2, 3 };
```

- And since C++20, you can drop the size of the array, 4, as follows:

```c++
int* myArray = new int[] { 0, 1, 2, 3 };
```

## Designated Initializers

- C++20 introduces *`designated initializers`* to initialize data members of so-called aggregates using their name. 

- An *aggregate type* is an object of an array type, or an object of a structure or class that satisfies the following restrictions: 

> - only public data members
> - no user-declared or inherited constructors
> - no virtual functions
> - no virtual, private, or protected base classes

- A designated initializer starts with a dot followed by the name of a data member. Designated initializers must be in the same order as the declaration order of the data members. Mixing designated initializers and non-designated initializers is not allowed. 
- Any data members that are not initialized using a designated initializer are initialized with their default values, which means the following:

> - Data members that have an in-class initializer will get that value.
> - Data members that do not have an in-class initializer are zero initialized.

```c++
struct Employee {
 	char firstInitial;
 	char lastInitial;
 	int employeeNumber;
 	int salary { 75'000 };
};

Employee anEmployee { 'J', 'D', 42, 80'000 };

Employee anEmployee {
 	.firstInitial = 'J',
 	.lastInitial = 'D',
 	.employeeNumber = 42,
 	.salary = 80'000
};
```

- A benefit of using such designated initializers is that it’s much easier to understand what a designated initializer is initializing compared to using the uniform initialization syntax.

- With designated initializers, you can skip initialization of certain members if you are satisfied with their default values. 

```c++
Employee anEmployee {
 	.firstInitial = 'J',
 	.lastInitial = 'D',
 	.salary = 80'000
};
```

## Pointers and Dynamic Memory

### Working with Pointers

### Dynamically Allocated Array

### Null Pointer Constant

## The Use of const

### const as a Qualifier for a Type

### const with Pointers

- To prevent the pointed-to values from being modified (as in the third line), you can add the keyword `const` to the declaration of ip like this:

```c++
const int* ip;
ip = new int[10];
ip[4] = 5; // DOES NOT COMPILE!

int const* ip; // An alternative but semantically equivalent
```

- If you instead want to mark ip itself const (not the values to which it points), you need to write this:

```c++
int const ip { nullptr };
ip = new int[10]; // DOES NOT COMPILE!
ip[4] = 5; // Error: dereferencing a null pointer
```

- Now that ip itself cannot be changed, the compiler requires you to initialize it when you declare it,  either with nullptr as in the preceding code or with newly allocated memory as follows:

```c++
int* const ip { new int[10] };
ip[4] = 5;
```

- *Here is another easy-to-remember rule to figure out complicated variable  declarations: read from right to left. For example,*  `int* const ip` *reads from right to left as “*ip *is a* const *pointer to an* int*.” Further,* `int const* ip` *reads as “*ip *is a pointer to a* const int*,” and* `const int* ip` *reads as “*ip *is a pointer to an* int *constant.”*

### const to Protect Parameters

- In C++, you can cast a non-const variable to a const variable. It offers some degree of protection from other code changing the variable. 

```c++
void mysteryFunction(const string* someString)
{
 	*someString = "Test"; // Will not compile
}
int main()
{
 	string myString { "The string" };
 	mysteryFunction(&myString);
}
```

- You can also use const on primitive-type parameters to prevent accidentally changing them in the body of the function.

```c++
void func(const int param) { /* Not allowed to change param... */ }
```

### const Methods

- A second use of the const keyword is to mark class methods as const, preventing them from modifying data members of the class.

## The constexpr Keyword

- C++ always had the notion of *constant expressions*, which are expressions evaluated at compile time. The following piece of code is not valid in C++:

  ```c++
  const int getArraySize() { return 32; }
  int main()
  {
   	int myArray[getArraySize()]; // Invalid in C++
  }
  ```

- Using the `constexpr` keyword, the getArraySize() function can be redefined to allow it to be called from within a constant expression:

```c++
constexpr int getArraySize() { return 32; }
int main()
{
 	int myArray[getArraySize()]; 		// OK
    int myArray2[getArraySize() + 1];	// OK
}
```

- Declaring a function as constexpr imposes quite a lot of restrictions on what the function can do because the compiler has to be able to evaluate the function at compile time. 
- For example, a constexpr function is allowed to call other constexpr functions but is not allowed to call any nonconstexpr functions. Such a function is not allowed to have any side effects, nor can it throw any exceptions.

- By defining a constexpr constructor, you can create constant-expression variables of user-defined types. 

```c++
class Rect
{
public:
 	constexpr Rect(size_t width, size_t height) : m_width { width }, m_height { height } 
    {
        
    }
 	constexpr size_t getArea() const 
    { 
        return m_width * m_height; 
    }
private:
 	size_t m_width { 0 }, m_height { 0 };
};
```

- Using this class to declare a constexpr object is straightforward.

```c++
constexpr Rect r { 8, 2 };
int myArray[r.getArea()]; // OK
```

## The consteval Keyword

- The constexpr keyword discussed in the previous section specifies that a function could be executed at compile time, but it *does not guarantee* compile-time execution. Take the following constexpr function:

```c++
constexpr double inchToMm(double inch) { return inch * 25.4; }

constexpr double const_inch { 6.0 };
constexpr double mm1 { inchToMm(const_inch) }; // at compile time

double dynamic_inch { 8.0 };
double mm2 { inchToMm(dynamic_inch) }; // at run time
```

- If you really want the guarantee that a function is always evaluated at compile time, you need to use the C++20 consteval keyword to turn a function into a so-called *immediate function*. The `inchToMm()` function can be changed as follows:

```c++
consteval double inchToMm(double inch) { return inch * 25.4; }
```

- Now, the first call to inchToMm() earlier still compiles fine and results in compile-time evaluation. However, the second call now results in a compilation error because it cannot be evaluated at compile time.

## References

- Professional C++ code, including much of the code in this book, uses references extensively. A *reference* in C++ is an *alias* for another variable. 

### Reference Variables

- Reference variables must be initialized as soon as they are created, like this:

```c++
int x { 3 };
int& xRef { x };
```

### Modifying References

- A reference always refers to the same variable to which it is initialized; references cannot be changed once they are created.

```c++
int x { 3 }, y { 4 };
int& xRef { x };
xRef = y; // Changes value of x to 4. Doesn't make xRef refer to y.
```

```c++
int x { 3 }, z { 5 };
int& xRef { x };
int& zRef { z };
zRef = xRef; // Assigns values, not references
```

- The final line does not change zRef. Instead, it sets the value of z to 3, because xRef refers to x, which is 3.

- *Once a reference is initialized to refer to a specific variable, you cannot change the reference to refer to another variable; you can change only the value of the variable the reference refers to.*

### References-to-const

- `const` applied to references is usually easier than `const` applied to pointers for two reasons. First, references are const by default, in that you can’t change to what they refer. So, there is no need to mark them const explicitly. Second, you can’t create a reference to a reference, so there is usually only one level of indirection with references. The only way to get multiple levels of indirection is to create a reference to a pointer.

- You cannot create a reference to an unnamed value, such as an integer literal, unless the reference is to a const value. 

```c++
int& unnamedRef1 { 5 }; // DOES NOT COMPILE
const int& unnamedRef2 { 5 }; // Works as expected
```

### References to Pointers and Pointers to References

- You can create references to any type, including pointer types. Here is an example of a reference to a pointer to int:

```c++
int* intP { nullptr };
int*& ptrRef { intP };
ptrRef = new int;
*ptrRef = 5;
```

- Finally, note that you cannot declare a reference to a reference or a pointer to a reference. 

### Reference Data Members

- The reference data members cannot be initialized inside the body of a class constructor, but they must be initialized in the so-called *constructor initializer*. 

```c++
class MyClass
{
public:
 	MyClass(int& ref) : m_ref { ref } { /* Body of constructor */ }
private:
	int& m_ref;
};
```

### Reference Parameters

- *The recommended way to return objects from a function is to return them by value, instead of using output parameters.*

### Pass-by-Reference-to-const

- The main value in reference-to-const parameters is efficiency. 
- When you pass a value into a function, an entire copy is made. When you pass a reference, you are really just passing a pointer to the original so the computer doesn’t need to make a copy. 
- By passing a reference-to-const, you get the best of both worlds: no copy is made, and the original variable cannot be changed. 

```c++
void printString(const string& myString)
{
 	cout << myString << endl;
}
int main()
{
 	string someString { "Hello World" };
 	printString(someString);
 	printString("Hello World"); // Passing literals works.
}
```

### Pass-by-Reference vs. Pass-by-Value

- Pass-by-reference is required when you want to modify the parameter and see those changes reflected in the variable passed to the function. 
- Pass-by-reference avoids copying the arguments to the function, providing two additional benefits:

  ➤ **Efficiency:** Large objects could take a long time to copy. Pass-by-reference passes only a reference to the object into the function.
  
  ➤ **Support:** Not all classes allow pass-by-value.

- If you want to leverage these benefits but do not want to allow the original objects to be modified, you should mark the parameters const, giving you pass-by-reference-to-const.

### Reference Return Values

- You can also return a reference from a function. Of course, you can use this technique only if the variable to which the returned reference refers to continues to exist following the function termination.

### Deciding Between References and Pointers

- Most of the time, you can use references instead of pointers. References to objects also support so-called *polymorphism*.
- *Prefer references over pointers; that is, use a pointer only if a reference is not possible.*

## const_cast()

- You can use `const_cast()` to add const-ness to a variable or cast away const-ness of a variable. 

- Additionally, the Standard Library provides a helper method called `std::as_const()`, defined in `<utility>`,  which returns a reference-to-const version of its reference parameter. Basically, `as_const(obj)` is equivalent to `const_cast<const T&>(obj)`, where T is the type of obj. 

## Exceptions

- When a piece of code detects an exceptional situation, it *throws* an exception. Another piece of code *catches* the exception and takes appropriate action. 

## Type Aliases

- A *type alias* provides a new name for an existing type declaration. 

```c++
using IntPtr = int*;
```

### typedefs

```c++
typedef int* IntPtr;
```

- *Always prefer type aliases over* typedef*s.*

## Type Inference

- *Type inference* allows the compiler to automatically deduce the type of an expression. There are two keywords for type inference: `auto` and `decltype`.

### The auto Keyword

- The auto keyword has a number of different uses:

  ➤ 	Deducing a function’s return type, as explained earlier in this chapter

  ➤ 	Structured bindings, as explained earlier in this chapter

  ➤ 	Deducing the type of an expression, as discussed in this section

  ➤ 	Deducing the type of non-type template parameters; see Chapter 12

  ➤ 	Abbreviated function template syntax; see Chapter 12

  ➤ 	`decltype(auto)`; see Chapter 12

  ➤ 	Alternative function syntax; see Chapter 12

  ➤ 	Generic lambda expressions; see Chapter 19, “Function Pointers, Function Objects, and Lambda Expressions”

```c++
auto x { 123 }; // x is of type int.
```

### The auto& Syntax

- Using auto to deduce the type of an expression strips away `reference` and `const `qualifiers. 

```c++
const string message { "Test" };
const string& foo() { return message; }
```

```c++
auto f1 { foo() };
```

- Because auto strips away `reference` and `const` qualifiers, f1 is of type string, and thus a *copy* is made! 
- If you want a `reference-to-const`, you can explicitly make it a `reference` and mark it `const`,  as follows:

```c++
const auto& f2 { foo() };
```

- Earlier in this chapter, the `as_const()` utility function is introduced. It returns a `reference-to-const` version of its reference parameter. 
- Be careful when using `as_const()` in combination with auto. Since auto strips away `reference` and `const` qualifiers, the following result variable has type string, not `const string&`, and hence a copy is made:

```c++
string str { "C++" };
auto result { as_const(str) };
```

- *Always keep in mind that* auto *strips away reference and* `const` *qualifiers and thus creates a copy! If you do not want a copy, use* `auto&` *or* `const auto&`*.*

### The auto* Syntax

- The auto keyword can also be used for pointers.

```c++
int i { 123 };
auto p { &i };
```

- However, when working with pointers, I do recommend using the auto* syntax as it more clearly states that pointers are involved, for example:

```c++
auto* p { &i };
```

```c++
const auto p1 { &i };	// int* const
auto const p2 { &i };	// int* const
```

### Copy List vs. Direct List Initialization

- There are two types of initialization that use braced initializer lists:

  ➤ **Copy list initialization:** `T obj = {arg1, arg2, ...};`
  
  ➤ **Direct list initialization:** `T obj {arg1, arg2, ...};`

- In combination with auto type deduction, there is an important difference between copy- and direct list initialization introduced since C++17.

- Since C++17, you have the following results (requires `<initializer_list>`):

```c++
// Copy list initialization
auto a = { 11 }; 			// initializer_list<int>
auto b = { 11, 22 }; 		// initializer_list<int>

// Direct list initialization
auto c { 11 }; 				// int
auto d { 11, 22 }; 			// Error, too many elements.
```

- Note that for copy list initialization, all the elements in the braced initializer must be of the same type. For example, the following does not compile:

```c++
auto b = { 11, 22.33 }; // Compilation error
```

### The decltype Keyword

- The decltype keyword takes an expression as argument and computes the type of that expression, as shown here:

```c++
int x { 123 };
decltype(x) y { 456 };
```

- The difference between auto and decltype is that decltype does not strip reference and const qualifiers. Take, again, a function foo() returning a reference-to-const string. Defining f2 using decltype as follows results in f2 being of type const string&, and thus no copy is made:

```c++
decltype(foo()) f2 { foo() };
```

## The Standard Library

## YOUR FIRST BIGGER C++ PROGRAM
