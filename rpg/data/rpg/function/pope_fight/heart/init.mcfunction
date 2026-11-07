attribute @s minecraft:max_health base set 1000
attribute @s minecraft:scale base set 3.3
attribute @s minecraft:knockback_resistance base set 1
data merge entity @s {Health:1000.0f}
scoreboard players set #last rpg_pf 1000
scoreboard players set #h rpg_pf 0
scoreboard players set #bl rpg_pf 0
scoreboard players set #seq rpg_pf 0
scoreboard players set #walking rpg_pf 0
scoreboard players set #weak rpg_pf 0
scoreboard players set #ba rpg_pf 0
scoreboard players set #ultq rpg_pf 0
scoreboard players set #ulti rpg_pf 0
scoreboard players set #ultcd rpg_pf 1200
scoreboard players set #ultl rpg_pf 750
execute facing entity @a[distance=..48,gamemode=!spectator,gamemode=!creative,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
tp @e[type=minecraft:armor_stand,tag=rpg.pf.rig,limit=1] @s
function rpg:pope_fight/heart/start_rise
