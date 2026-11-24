scoreboard players set #roll rpg_ev 0
execute if score #ev rpg_ev matches 1.. run return 0
tag @a remove rpg.ev.host
tag @r[scores={rpg_ob=100},gamemode=!spectator] add rpg.ev.host
execute unless entity @a[tag=rpg.ev.host] run return 0
execute store result score #r rpg_ev run random value 1..6
execute as @a[tag=rpg.ev.host,limit=1] at @s run function rpg:events/try
