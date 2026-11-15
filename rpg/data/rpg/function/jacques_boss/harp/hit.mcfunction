scoreboard players set #d rpg_jq 21
function rpg:jacques_boss/line/thin
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit] run damage @s 12 minecraft:magic by @e[type=minecraft:vindicator,tag=rpg.jqb,tag=!rpg.jqb.preview,limit=1]
execute as @e[tag=rpg.unit,tag=rpg.jqb.hit,tag=rpg.jqb.cursed] at @s run function rpg:jacques_boss/curse/pop
tag @e[tag=rpg.unit] remove rpg.jqb.hit
