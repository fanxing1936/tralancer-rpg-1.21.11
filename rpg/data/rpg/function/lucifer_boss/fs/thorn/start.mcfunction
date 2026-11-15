scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_t 0
scoreboard players set @s rpg_l2_sk 7
function rpg:lucifer_fight/hold
scoreboard players set @s rpg_dm_cd 30
function rpg:lucifer_p2/play/jungleabomination_vineattack
tellraw @a[distance=..48] ["",{"text":"〖路西法〗","color":"#34975A","bold":true,"italic":false},{"text":"  ","color":"#9C9A94","bold":false,"italic":false},{"text":"荆棘与蒺藜 · ","color":"#E6DFCF","bold":false,"italic":false},{"text":"地必给你长出荆棘和蒺藜来。","color":"#9C9A94","bold":false,"italic":false}]
playsound minecraft:block.rooted_dirt.break hostile @a[distance=..40] ~ ~ ~ 1.4 0.5
tag @e[tag=rpg.unit] remove rpg.lub.thit
