# 教皇一刻（as、at 教皇）。
scoreboard players add #h rpg_pf 1
execute if score #h rpg_pf matches 5.. run function rpg:pope_fight/boss/read
execute if score #cd rpg_pf matches 1.. run scoreboard players remove #cd rpg_pf 1
execute if score #tp rpg_pf matches 1.. run scoreboard players remove #tp rpg_pf 1
execute if score #blood rpg_pf matches 1.. run scoreboard players remove #blood rpg_pf 1
execute if score #reclaim rpg_pf matches 1.. run scoreboard players remove #reclaim rpg_pf 1
execute if score #enhance rpg_pf matches 1.. run scoreboard players remove #enhance rpg_pf 1
execute if score #ultcd rpg_pf matches 1.. run scoreboard players remove #ultcd rpg_pf 1
execute if score #stage rpg_pf matches 3 run return 0
execute if score #sk rpg_pf matches 1.. run return run function rpg:pope_fight/boss/skill
execute if score #wave rpg_pf matches 1 run return run function rpg:pope_fight/boss/start_summon
execute if score #tp rpg_pf matches 0 if entity @a[distance=..3,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/boss/start_teleport
execute if score #cd rpg_pf matches 1.. run return 0
execute if score #ultq rpg_pf matches 1 run return run function rpg:pope_fight/boss/start_ult
execute if score #ultcd rpg_pf matches 0 if entity @a[distance=..32,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/boss/start_ult
execute if entity @a[distance=..3.5,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/boss/start_melee
execute if score #blood rpg_pf matches 0 if entity @e[type=minecraft:vindicator,tag=rpg.pf.unit,limit=1] run return run function rpg:pope_fight/boss/start_blood
execute if score #reclaim rpg_pf matches 0 if entity @a[distance=..25,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/boss/start_reclaim
execute if score #enhance rpg_pf matches 0 if entity @e[type=minecraft:vindicator,tag=rpg.pf.unit,distance=..11,limit=1] run return run function rpg:pope_fight/boss/start_enhance
execute if score #pb rpg_pf matches 3.. if entity @a[distance=..25,gamemode=!spectator,gamemode=!creative] run return run function rpg:pope_fight/boss/start_ranged
execute if entity @a[distance=..32,gamemode=!spectator,gamemode=!creative] run function rpg:pope_fight/boss/start_basic
