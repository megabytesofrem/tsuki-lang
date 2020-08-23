# tsuki-lang
A simple toy language written in Python using Lark. Tsuki is designed to be similar
to Lua syntax wise, however much simpler.

## Variables
```lua
-- Tsuki supports Lua style comments too!

-- name is a string in this case, a python str()
name = "charlotte"

-- we can assign a new variable to the value of a variable
hername = name

-- age is an number, which maps to a python int()
age = 19

-- manesix is an array of strings, which maps to a python list()
manesix = ["Twilight", "Rarity", "Fluttershy", "Applejack", "Pinkie Pie", "Spike"]

-- ponies is a table, which maps to a python dict()
-- Tables will be used later on extensively for implementing a Lua style OOP
ponies = {
    "twilight" -> "alicorn",
    "rarity" -> "unicorn",
    "applejack" -> "earth"
}

echo(manesix)
echo(ponies)
```