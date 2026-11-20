# 千刀从手里滑落，插在他身前（as/at 他）
execute on passengers if entity @s[tag=rpg.slm.p.rapier] run data modify entity @s item.components."minecraft:item_model" set value "rpg:empty"
execute positioned ^ ^ ^1.1 run summon minecraft:item_display ~ ~0.7 ~ {Tags:["rpg.slb.fx","rpg.slb.fxnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rpg:saul/rapier"}},item_display:"none",brightness:{sky:15,block:12},view_range:1.5f}
execute as @e[tag=rpg.slb.fxnew] at @s run function rpg:saul_boss/finale/blade
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_life 400
scoreboard players set @e[tag=rpg.slb.fxnew] rpg_sl_kd 0
tag @e[tag=rpg.slb.fxnew] remove rpg.slb.fxnew
playsound minecraft:block.chain.place hostile @a[distance=..24] ~ ~ ~ 1 1.4
particle minecraft:crit ^ ^0.3 ^1.1 0.2 0.1 0.2 0.2 10
