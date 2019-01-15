# Python Space Invaders Project

Having fun with python gaming.

This work was done for a python learning course.

Original work was done by:
 - Lee Robinson https://github.com/leerob/Space_Invaders
 - Cthulhu2 https://github.com/Cthulhu2/Space_Invaders


### How to launch it
```
pip3 install pygame
python3 ./main.py
```

### Change

It was a big refactoring :
- introduce a 'engine' which define
   - a game composed of scene
   - a resource manager
   - few utility on sprite, text, font, graphics
   - a life cycle management of pygame initialization
- decompose original game in:
  - scene (main, round, game over, ...)
  - entities

Next step will be to introduce a way to:
 - exchange event between composant
 - use ECS pattern
 - use finite state machine to manage view state
 - use 'store'/view concept of react pattern


