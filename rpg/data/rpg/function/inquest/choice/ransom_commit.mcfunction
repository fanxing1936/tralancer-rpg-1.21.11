tag @s add rpg.rite.chooser
execute at @s as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..12,sort=nearest,limit=1,scores={rpg_ex_ransom=1..}] run function rpg:inquest/counter/mammon_paid
tag @s remove rpg.rite.chooser
scoreboard players add @s rpg_ex_xp 3
