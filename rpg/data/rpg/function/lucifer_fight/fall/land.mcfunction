scoreboard players set @s rpg_l2_v 1
function rpg:lucifer_p2/play/jungleabomination_land
scoreboard players operation #id rpg_l2_id = @s rpg_l2_id
execute as @e[type=minecraft:marker,tag=rpg.lu2f.lmark] if score @s rpg_l2_id = #id rpg_l2_id run kill @s
tag @s add rpg.dm.cast
execute as @a[distance=..5.5,gamemode=!spectator,gamemode=!creative] run function rpg:lucifer_fight/fall/hit
tag @s remove rpg.dm.cast
particle block{block_state:{Name:"minecraft:rooted_dirt"}} ~ ~0.3 ~ 3 0.2 3 0.2 120
particle dust_color_transition{from_color:[0.37,0.84,0.55],to_color:[0.0,0.29,0.11],scale:2.4} ~ ~0.6 ~ 3 0.4 3 0.06 60
particle explosion_emitter ~ ~0.5 ~ 0 0 0 0 1
playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 0.6
kill @e[type=minecraft:item_display,tag=rpg.lu2f.fm,distance=..16]
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/shock_ring"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.06f,0f],scale:[0.5f,1f,0.5f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 8
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 9
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
summon minecraft:item_display ~ ~ ~ {Tags:["rpg.lu2f.fx","rpg.lu2f.pnew","rpg.lu2f.anim"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:lucifer_fx/crack"}},brightness:{sky:15,block:15},view_range:2f,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.04f,0f],scale:[6f,1f,6f]}}
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_k 6
scoreboard players set @e[tag=rpg.lu2f.pnew] rpg_l2_t 40
tag @e[tag=rpg.lu2f.pnew] remove rpg.lu2f.pnew
execute positioned ~ ~1 ~ run function rpg:lucifer_fight/fx/debris
