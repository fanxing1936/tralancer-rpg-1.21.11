tag @s add rpg.mkb.hp
function rpg:michael_boss/refill
execute if entity @s[tag=rpg.mkb.intro] run function rpg:michael/anim/enter/hero
tag @s remove rpg.mkb.intro
