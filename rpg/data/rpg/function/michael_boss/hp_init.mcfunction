tag @s add rpg.mkb.hp
function rpg:michael_boss/refill
execute if entity @s[tag=rpg.mkb.intro] run function rpg:michael/anim/enter/hero
execute if score #pro rpg_mk matches 1 run function rpg:michael/look/solid
tag @s remove rpg.mkb.intro
