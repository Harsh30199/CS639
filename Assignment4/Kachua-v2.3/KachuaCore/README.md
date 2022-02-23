**Dependencies**

```bash
pip install antlr4-python3-runtime==4.7.2
pip install networkx
sudo apt-get install python3-tk 
```

**Running an example**

  ```bash
  ./kachua.py ./example/test.tl
  ```
  
**AST Nodes**

- Please refere `ast/kachuaAST.py`

```bash
Kachua v1.1
------------
usage: kachua.py [-h] [-p] [-r] [-O] [-b] [-z] [-t TIMEOUT] [-d PARAMS] progfl

Program Analysis Framework for Turtle.

positional arguments:
  progfl

optional arguments:
  -h, --help            show this help message and exit
  -p, --ir              pretty printing
  -r, --run             execute program
  -O, --opt             optimize
  -b, --bin             load binary IR
  -z, --fuzz            Run fuzzer on a turtle program (seed values with '-d' or '--params' flag needed.)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout Parameter for Analysis (in secs)
  -d PARAMS, --params PARAMS
                        pass variable values to kachua program in python dictionary format
```