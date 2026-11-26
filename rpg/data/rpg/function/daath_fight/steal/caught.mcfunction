function rpg:daath_fight/steal/take
execute at @a[tag=rpg.dt.me,limit=1] run function rpg:daath_fight/steal/fx
execute as @a[tag=rpg.dt.me,limit=1] run effect give @s minecraft:slowness 1 2 true
