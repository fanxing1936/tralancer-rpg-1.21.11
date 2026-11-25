# 血月：身边多刷三只
summon minecraft:zombie ~ ~ ~ {Tags:["rpg.pl.new"]}
spreadplayers ~ ~ 2 18 under 330 false @e[type=minecraft:zombie,tag=rpg.pl.new,limit=1]
tag @e[tag=rpg.pl.new] remove rpg.pl.new
summon minecraft:skeleton ~ ~ ~ {Tags:["rpg.pl.new"]}
spreadplayers ~ ~ 2 18 under 330 false @e[type=minecraft:skeleton,tag=rpg.pl.new,limit=1]
tag @e[tag=rpg.pl.new] remove rpg.pl.new
summon minecraft:spider ~ ~ ~ {Tags:["rpg.pl.new"]}
spreadplayers ~ ~ 2 18 under 330 false @e[type=minecraft:spider,tag=rpg.pl.new,limit=1]
tag @e[tag=rpg.pl.new] remove rpg.pl.new
