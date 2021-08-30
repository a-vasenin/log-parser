# How to get started:
```
chmod +x parser.py
./parser libraries_path [--platform {win, lin, mac}]
```
`libraries_path` - required parameter. May be absolute or relative.  
`--platform` - optional parameter. Value can be one of {win, lin, mac}. If not specified, defaults to 'all' - in this case, runs for all three platforms.
# Examples:
```
python3 parser.py ./libraries
```
or
```
./parser.py libraries --platform win
```
