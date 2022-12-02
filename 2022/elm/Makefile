.PHONY: run w wf test

run:
	elm make src/Day1.elm --output=main.js
	cat src/Day1.example.txt | node ./cli.js example
	cat src/Day1.input.txt | node ./cli.js input

w:
	onchange 'src/*.elm' -- make

wf:
	onchange 'src/*.elm' -- elm-format --yes {{file}}

test:
	elm-test tests/Day1.elm
