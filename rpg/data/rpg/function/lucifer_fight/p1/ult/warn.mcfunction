execute at @s as @e[tag=rpg.unit.f,distance=..18] run function rpg:hud/demon/m37
function rpg:lucifer_fight/cancel
scoreboard players set @s rpg_l2_st 3
scoreboard players set @s rpg_l2_sk 16
scoreboard players set @s rpg_l2_t 0
function rpg:lucifer_fight/hold
function rpg:lucifer_lord/play/laugh
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.6} ~ ~1 ~ 1.4 1 1.4 0.04 42 force
playsound minecraft:block.trial_spawner.ominous_activate hostile @a[distance=..32] ~ ~ ~ 1 0.65
execute positioned ~ ~3.3 ~ run function rpg:lucifer_fight/p1/ult/crown
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/serpent_crown"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.03f,0f],scale:[0.01f,1f,0.01f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 17
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 52
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
