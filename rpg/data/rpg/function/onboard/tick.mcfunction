scoreboard players enable @a rpg_pro_go
execute as @a[scores={rpg_pro_go=1..}] run function rpg:onboard/pro/req
execute as @a[tag=!rpg.ob,tag=!rpg.pr] unless score @s rpg_ob_v matches 1.. run function rpg:onboard/check
execute as @a[tag=rpg.ob,tag=!rpg.pr] at @s run function rpg:onboard/player
