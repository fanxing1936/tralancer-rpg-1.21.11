scoreboard players set @s rpg_ex_hitcd 5
execute on attacker run scoreboard players add @s rpg_ex_xp 1
tag @s add rpg.rite.subject
execute as @e[type=minecraft:item_display,tag=rpg.rite.anchor,distance=..14] if score @s rpg_rite_id = @e[type=minecraft:vindicator,tag=rpg.rite.subject,limit=1] rpg_rite_id run function rpg:inquest/stability/add2
tag @s remove rpg.rite.subject
