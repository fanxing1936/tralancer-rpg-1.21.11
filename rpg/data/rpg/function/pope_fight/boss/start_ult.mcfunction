# 大招：血量到线或时钟走完，先到先出。两招轮流。
scoreboard players set #ultq rpg_pf 0
scoreboard players set #ultcd rpg_pf 900
scoreboard players add #ulti rpg_pf 1
execute if score #ulti rpg_pf matches 1 run return run function rpg:pope_fight/boss/start_seals
scoreboard players set #ulti rpg_pf 0
function rpg:pope_fight/boss/start_doom
