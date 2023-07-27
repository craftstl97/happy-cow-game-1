# Happy Cow Game framework

This is the framework for the happy cow game assignment for AI

- For this framework, cows are to be placed at random
- Input is as follows: Size of grid, grid (see sample_input.txt)
- tiles are: Grass (.), Pond(#), Haystack(@)
- A cow gets one point for being next to a Haystack
- A cow next to a haystack gets an additional 2 points for being next to a pond
- A cow next to or diagonal to a cow gets -3 points
- Conditions do not stack, a cow completely surrounded by cows still only gets -3 points
- Output is as follows: Size of grid, grid, final score (see sample_output.txt)
