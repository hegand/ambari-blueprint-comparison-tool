# ambari-blueprint-comparison-tool

Compares two ambari blueprints and generate property level diffs

## Configuration
Install `diff2html-cli` package with `npm`:
```bash
chmod u+x bin/install_diff2html-cli.sh
./bin/install_diff2html-cli.sh
```
Edit `bin/run_example.sh` and change `left.json` and `right.json` paths to match your blueprints paths that you would like to compare.

## How to run
If you configured `bin/run.sh`, you can run the following:
```bash
chmod u+x bin/run.sh
./bin/run.sh
```
If you would like to run without the bash script helper:
```bash
python src/process_blueprints.py -r right.json -l left.json | diff2html -i stdin -s side -F out.html
```