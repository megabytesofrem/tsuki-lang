# tsuki-lang
A simple toy language written in Python using Lark. Tsuki is designed to be similar
to Lua syntax wise, however much simpler.

## Features
- [x] Variables that map to Python representations
- [x] Arrays, and tables (dictionaries)
- [x] If statements
- [x] Comments

## Demo
```lua
-- Hello world in Tsuki
echo("Hello world")

-- Checking for conditions with if
manesix = ["Twilight", "Rarity", "Fluttershy", "Applejack", "Rainbow Dash", "Pinkie Pie"]
inwonderbolts = "true"
if find(manesix, "Rainbow Dash") ~= "nil" and inwonderbolts == "true" then 
    echo("Rainbow dash is in the Wonderbolts")
end

-- Tables are cool too!
princesses = {
    "Twilight" -> "is the princess of friendship",
    "Celestia" -> "raises the sun",
    "Luna"     -> "raises the moon"
}

echo("Celestia ")
what = find(princesses, "Celestia")
echo(what)

-- ...and heres a single line if statement!
if what ~= "raises the sun" then echo("Wrong pony") end
```