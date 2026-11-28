scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_t
scoreboard players set #k rpg_mk_i4 20
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 as @e[tag=rpg.unit.f,distance=6..44] run damage @s 6 minecraft:in_fire by @e[type=minecraft:vindicator,tag=rpg.mkb,tag=!rpg.mk.preview,limit=1,distance=0..]
scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_t
scoreboard players set #k rpg_mk_i4 10
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 run summon minecraft:item_display ~ ~0.1 ~ {Tags:["rpg.mkb.fx","rpg.mkb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:michael_vfx/ring_t","minecraft:custom_model_data":{colors:[16777215]}}},brightness:{sky:15,block:15},teleport_duration:1,interpolation_duration:3,view_range:2f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[12f,1f,12f],right_rotation:[0f,0f,0f,1f]}}
execute if score #m rpg_mk_i4 matches 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_life 22
execute if score #m rpg_mk_i4 matches 0 run scoreboard players set @e[tag=rpg.mkb.fxnew,distance=0..] rpg_mk_kd 20
execute if score #m rpg_mk_i4 matches 0 run tag @e[tag=rpg.mkb.fxnew,distance=0..] remove rpg.mkb.fxnew
execute if score #m rpg_mk_i4 matches 0 run particle minecraft:flame ~ ~0.4 ~ 16 0.3 16 0.02 80
execute if score #m rpg_mk_i4 matches 5 run particle minecraft:dust_color_transition{from_color:[1.0,0.5,0.32],to_color:[1.0,0.2,0.0],scale:1.1} ~ ~0.8 ~ 14 0.4 14 0 40
scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_t
scoreboard players set #k rpg_mk_i4 12
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 run function rpg:michael_boss_i4/seraph/slash
scoreboard players operation #m rpg_mk_i4 = @s rpg_mk_t
scoreboard players set #k rpg_mk_i4 20
scoreboard players operation #m rpg_mk_i4 %= #k rpg_mk_i4
execute if score #m rpg_mk_i4 matches 0 run function rpg:michael_boss_i4/seraph/flames
execute if score #m rpg_mk_i4 matches 10 rotated 30 0 run function rpg:michael_boss_i4/seraph/flames
