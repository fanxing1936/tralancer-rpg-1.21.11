execute at @s as @a[distance=..18,gamemode=!spectator,gamemode=!creative] run function rpg:hud/demon/m50
function rpg:lucifer_fight/cancel
scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_sk 6
scoreboard players set @s rpg_l2_t 0
function rpg:lucifer_fight/hold
function rpg:lucifer_p2/play/jungleabomination_projectileattack_start
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~3 ~ 2 2 2 0.04 50
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.6
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/eden_faint"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.03f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 2
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 120
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
