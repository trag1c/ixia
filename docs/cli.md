Ixia exposes a command-line interface akin to the one introduced to the
[`random` module][random-module] in Python 3.13. On top of what the
[`random` CLI][random-cli] offers, Ixia also supports reading a random line from
a file. The interface is available through the `python -m ixia` command:
```
λ python -m ixia
usage: ixia [-h] [-c ITEM [ITEM ...] | -i N | -l LINE | -f N] [input ...]

Connecting secrets' security with random's versatility

positional arguments:
  input                 if no options given, output depends on the input:
                          string or multiple: same as --choice
                          valid path:         same as --line
                          integer:            same as --int/--integer
                          float:              same as --float

optional arguments:
  -h, --help            show this help message and exit
  -c ITEM [ITEM ...], --choice ITEM [ITEM ...]
                        print a random choice
  -i N, --int N, --integer N
                        print a random integer between 1 and N inclusive
  -l LINE, --line LINE  print a random line from a file
  -f N, --float N       print a random floating-point number between 0 and N inclusive
```
## Example usage
```
λ cat example.txt
hello
there
general
kenobi

λ python -m ixia --line example.txt
there

λ python -m ixia --int 20          
9

λ python -m ixia --float 20
14.723129947937718

λ python -m ixia --choice foo bar baz
foo
```
Just like the [`random` CLI][random-cli], Ixia can infer the output type
based on the provided arguments:
```
λ python -m ixia a b c               
a

λ python -m ixia 20   
5

λ python -m ixia 10.0
9.957858462359129

λ python -m ixia example.txt
hello
```


[random-module]: https://docs.python.org/3/library/random.html
[random-cli]: https://docs.python.org/3/library/random.html#command-line-usage