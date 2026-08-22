# 15 行原本各自扫一遍全实体表找 @e[type=minecraft:item,tag=rpg.i.loot_trigger1]；现在由上层一次判定后统一进入。
# 行内容与顺序原样保留。
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~ ~ ~ run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~3 ~ ~ run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~ ~ ~3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~-3 ~ ~ run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~ ~ ~-3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~3 ~ ~3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~3 ~ ~-3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~-3 ~ ~3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~-3 ~ ~-3 run function rpg:loot/trigger
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s positioned ~ ~2 ~ run function rpg:loot/trigger_ominous
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s run playsound minecraft:block.beacon.power_select player @a[distance=..7]
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s run summon firework_rocket ~ ~-0.2 ~ {Life:0,LifeTime:0,FireworksItem:{id:firework_rocket,components:{fireworks:{flight_duration:0,explosions:[{shape:burst,has_twinkle:1b,has_trail:1b,colors:[I;3847130,16383998,1481884]}]}}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s run setblock ~ ~-1 ~ air
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s run setblock ~ ~-1 ~ minecraft:vault[ominous=true]{config:{loot_table:"rpg:loot/loot_ominous",key_item:{components:{"minecraft:lore":[{"extra":[{"color":"white","italic":false,"text":"+------------------+"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"开辟神启的"},{"bold":true,"color":"gold","italic":false,"text":"[钥匙]"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"唤出传奇的"},{"bold":true,"color":"gold","italic":false,"text":"[宝具]"}],"text":""},{"extra":[{"color":"white","italic":false,"text":"+------------------+"}],"text":""}],"minecraft:custom_name":{"extra":[{"bold":true,"color":"gold","italic":false,"text":"[legend]"},{"italic":false,"text":"灾厄试炼之匙"}],"text":""}},count:1,id:"minecraft:ominous_trial_key"}}}
execute as @e[type=minecraft:item,tag=rpg.i.loot_trigger1] at @s run kill
