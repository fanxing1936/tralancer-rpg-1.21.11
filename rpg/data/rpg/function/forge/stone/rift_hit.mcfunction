damage @s 8 rpg:forge_bonus by @a[tag=rpg.fg.from,limit=1]
execute store result score @s damage_action run data get entity @s Health
function rpg:forge/fx/push
