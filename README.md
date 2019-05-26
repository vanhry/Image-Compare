##  Description
This app findind images pair with following parameters:
  - duplicate (images which are exactly the same)
  - modification (images which differ by size, blur level and/or noise filters)
  - similar (images of the same scene from another angle

## Usage
```shell
python solution.py --path PATH
```

#### Example of work
![Imgur](https://i.imgur.com/rLrWyGf.png)
#### Known issues
I know that 3 point (similar images) problem will be better to solve with feature matching techniques but in this app I tried to find maybe not so effective but more simplest methods. And this problems were solved with self-made and slightly heuristic algorithms.
Also app is too slow and I'll try to fix it later.