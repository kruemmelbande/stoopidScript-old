# StoopidScript

 Its like my stoopid language, except its nothing like it.

### The available commands are

 ```
 var <type> <name> = <value>
 out <value>
 if <condition>{
    <code>
 }
 goto <line>
 ```
### the variable types are:
- int  
- float  
- str
- bool  
- dynamic
    - type can change on the fly
- auto  
    - sets the type according to the initial declaration
- label  
    - if no value is set, it is set to the current line
    - used for goto